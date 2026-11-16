"""Synthetic seven-case before/after benchmark. Run from this directory."""
import json, tempfile, os
from candidate_ledger import connect, append, lookup
from correction_view import lookup_corrected

CASES=[
 ('single_correction',[('CORRECTION',{'text':'corrected','replaces_event_id':'2','source_locator':'synthetic:correction'})],'corrected'),
 ('two_corrections',[('CORRECTION',{'text':'middle','replaces_event_id':'2','source_locator':'synthetic:c1'}),('CORRECTION',{'text':'final','replaces_event_id':'3','source_locator':'synthetic:c2'})],'final'),
 ('unlinked',[('CORRECTION',{'text':'wrong','source_locator':'synthetic:c'})],None),
 ('fork',[('CORRECTION',{'text':'A','replaces_event_id':'2','source_locator':'synthetic:a'}),('CORRECTION',{'text':'B','replaces_event_id':'2','source_locator':'synthetic:b'})],None),
 ('disconnected',[('CORRECTION',{'text':'orphan','replaces_event_id':'999','source_locator':'synthetic:o'})],None),
 ('no_correction',[],'old'),
 ('retraction',[('RETRACTION',{})],None),
]
def run():
 results=[]
 for name,events,expected in CASES:
  with tempfile.TemporaryDirectory() as d:
   db=connect(os.path.join(d,'fixture.db'))
   append(db,'SOURCE','x',{'locator':'synthetic:original'})
   append(db,'CLAIM','x',{'text':'old'})
   for kind,payload in events:append(db,kind,'x',payload)
   before=lookup(db,'x');after=lookup_corrected(db,'x')
   correct_before=(before.get('text')==expected) if expected is not None else before['status'] in ('UNKNOWN','RETRACTED_CANDIDATE')
   correct_after=(after.get('text')==expected) if expected is not None else after['status'] in ('UNKNOWN','RETRACTED_CANDIDATE')
   results.append({'case':name,'expected':expected,'before_status':before['status'],'before_text':before.get('text'),'before_correct':correct_before,'after_status':after['status'],'after_text':after.get('text'),'after_correct':correct_after})
   db.close()
 return {'baseline_correct':sum(r['before_correct'] for r in results),'candidate_correct':sum(r['after_correct'] for r in results),'total':len(results),'cases':results}
if __name__=='__main__':print(json.dumps(run(),indent=2))
