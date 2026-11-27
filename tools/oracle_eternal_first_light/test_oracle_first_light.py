"""Exercise the same CLI used by a human and workflow."""
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

BASE=Path(__file__).resolve().parent
RUNNER=BASE/"oracle_first_light.py"

class CLI(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.base=Path(t.name)
        self.state=self.base/"state"
    def cli(self,mode,runner=RUNNER,state=None):
        argv=[sys.executable,str(runner),mode]
        if mode!="source":
            argv+=["--state",str(state or self.state)]
        return subprocess.run(argv,capture_output=True,text=True,cwd=self.base)
    def ok(self,mode):
        ans=self.cli(mode)
        self.assertEqual(ans.returncode,0,ans.stderr)
        return json.loads(ans.stdout)
    def held(self,mode,needle,runner=RUNNER,state=None):
        ans=self.cli(mode,runner,state)
        self.assertEqual(ans.returncode,2)
        self.assertEqual(json.loads(ans.stderr)["result"],"HELD")
        self.assertIn(needle,ans.stderr)
        self.assertEqual(ans.stdout,"")
    def test_read_pin_and_real_source_matches(self):
        evidence=self.ok("source")
        self.assertEqual(evidence["repository"],"HawkesNest-LLC/Oracle")
        self.assertEqual(evidence["rows"][-2][1:],[24,2,2,10])
        self.assertEqual(evidence["bytes"],5390)
    def test_actual_first_run_cold_reread_and_second_run_dedup(self):
        a=self.ok("run")
        b=self.ok("review")
        c=self.ok("run")
        d=self.ok("review")
        self.assertEqual((a["result"],c["result"]),("CREATED","ALREADY_PRESENT"))
        self.assertEqual((b["receipt_count"],d["receipt_count"]),(1,2))
        self.assertEqual(d["artifact_count"],1)
        self.assertEqual(a["artifact_id"],c["artifact_id"])
        self.assertEqual(b["files"],d["files"])
        self.assertNotEqual(a["receipt_id"],c["receipt_id"])
        self.assertFalse(c["published"])
        self.assertFalse(c["production_activated"])
        self.assertEqual(d["human_review"],"PENDING")
    def test_changed_public_input_stops_before_stage(self):
        p=self.base/"cloned"
        p.mkdir()
        local=p/RUNNER.name
        shutil.copyfile(RUNNER,local)
        source=p/"sources"
        source.mkdir()
        (source/"nvid-r003-note.md").write_text("A different source; not allowlisted")
        self.held("run","failed byte pin",runner=local)
        self.assertFalse(self.state.exists())
    def test_tampered_artifact_detected_not_repaired(self):
        a=self.ok("run")
        path=self.state/"review"/a["artifact_id"]/"research-memo.md"
        path.write_text("local tamper canary")
        self.held("review","expected bytes")
        self.held("run","expected bytes")
        self.assertEqual(path.read_text(),"local tamper canary")
        with sqlite3.connect(self.state/"ledger.sqlite3") as conn:
            self.assertEqual(conn.execute("select count(*) from receipt").fetchone()[0],1)
    def test_reuses_complete_orphan_but_never_partial_temp(self):
        a=self.ok("run")
        orphan=self.base/"recovery"
        old=self.state/"review"/a["artifact_id"]
        new=orphan/"review"/a["artifact_id"]
        new.mkdir(parents=True)
        shutil.copyfile(old/"research-memo.md",new/"research-memo.md")
        (new/".first-light-stage-crashed-process").write_text("partial")
        b=self.cli("run",state=orphan)
        self.assertEqual(b.returncode,0,b.stderr)
        r=json.loads(b.stdout)
        self.assertEqual((r["result"],r["artifact_id"]),("CREATED",a["artifact_id"]))
        self.assertEqual((new/"mobile-brief.md").read_bytes(),(old/"mobile-brief.md").read_bytes())
        self.assertEqual((new/".first-light-stage-crashed-process").read_text(),"partial")

    def test_invalid_receipt_detected_by_cold_read(self):
        self.ok("run")
        with sqlite3.connect(self.state/"ledger.sqlite3") as conn:
            conn.execute("update receipt set body='{}'")
        self.held("review","receipt differs")
    def test_pause_no_ledger_write(self):
        self.state.mkdir()
        (self.state/"PAUSE").touch()
        self.held("run","PAUSE")
        self.assertFalse((self.state/"ledger.sqlite3").exists())
    def test_symlink_outputs_not_followed(self):
        a=self.ok("run")
        path=self.state/"review"/a["artifact_id"]/"research-memo.md"
        copy=self.base/"elsewhere"
        path.rename(copy)
        path.symlink_to(copy)
        self.held("review","ordinary local file")
        self.assertTrue(path.is_symlink())
    def test_missing_state_read_only(self):
        self.held("review","no persisted review state")
        self.assertFalse(self.state.exists())

if __name__=="__main__":
    unittest.main()
