import json, subprocess, unittest, pathlib, tempfile, sys
from esp_contract import validate, EnvelopeError, missing_claim
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent.parent/'docs/continuity/godedge/continuity_kernel_01'))
from kernel import connect, append, verify

class InteropTests(unittest.TestCase):
    def setUp(self):
        self.good={'claimId':'c-1','status':'PROPOSED','authority':'AI','confidence':0.5,'sources':['github:example']}
    def cases(self):
        cases=[self.good,missing_claim('unknown')]
        for status in ('ESTABLISHED','RECONSTRUCTED','PROPOSED','SIMULATED','SUPERSEDED','REJECTED','UNKNOWN'):
            x={**self.good,'status':status};cases.append(x)
        for authority in ('Creator','Editor','AI','Reviewer','Observer'):
            x={**self.good,'authority':authority};cases.append(x)
        for field,value in [('confidence',True),('confidence',float('inf')),('confidence',-1),('confidence',1.1),('sources',['']),('status','CANONICAL'),('authority','AI-OWNER'),('claimId',' ')]:
            x={**self.good,field:value};cases.append(x)
        cases.extend([{**self.good,'status':'ESTABLISHED','sources':[]},{**self.good,'extra':1},{k:v for k,v in self.good.items() if k!='sources'},None,[]])
        return cases
    def test_python_node_agree(self):
        cases=self.cases()
        # JSON has no Infinity; exclude it from cross-language wire test, test separately.
        cases=[c for c in cases if not isinstance(c,dict) or c.get('confidence')!=float('inf')]
        p=subprocess.run(['node',str(ROOT/'esp_cli.cjs')],input=json.dumps(cases),text=True,capture_output=True,check=True)
        node=json.loads(p.stdout)
        for item,result in zip(cases,node):
            try:
                py=validate(item)
                self.assertTrue(result['ok'],repr(item))
                self.assertEqual(py,result['envelope'])
            except (EnvelopeError,TypeError):
                self.assertFalse(result['ok'],repr(item))
    def test_nonfinite_rejected(self):
        with self.assertRaises(EnvelopeError):validate({**self.good,'confidence':float('inf')})
    def test_kernel_readonly_adapter(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('adapter',ROOT/'kernel_adapter.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            path=str(pathlib.Path(tmp)/'events.sqlite')
            c=connect(path)
            append(c,'SOURCE','c-1',{'locator':'github:example'})
            append(c,'CLAIM','c-1',{'status':'CANDIDATE','attribution':'AI','text':'draft'})
            before=c.execute('SELECT COUNT(*) FROM events').fetchone()[0]
            env=module.read_claim(c,'c-1')
            self.assertEqual(env['status'],'UNKNOWN')
            self.assertEqual(env['sources'],['github:example'])
            self.assertEqual(c.execute('SELECT COUNT(*) FROM events').fetchone()[0],before)
            self.assertTrue(verify(c))
            self.assertEqual(module.read_claim(c,'absent')['status'],'UNKNOWN')
            c.close()
            c2=connect(path)
            self.assertEqual(module.read_claim(c2,'c-1'),env)
            c2.close()
if __name__=='__main__':unittest.main()
