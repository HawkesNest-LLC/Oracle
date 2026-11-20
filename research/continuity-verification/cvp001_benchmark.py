#!/usr/bin/env python3
"""CVP-001: synthetic finite-observation indistinguishability demo. Python 3 stdlib."""
import hashlib, json
from collections import Counter

SEED = 2397

def observation(history):
    return tuple(history['answers'])

def witness(history):
    return history['origin_receipt']

def run():
    a = {'id':'H_A','answers':['I remember the garden','I chose to stay','I corrected the date'],'origin_receipt':'witness:original:A'}
    b = {'id':'H_B','answers':list(a['answers']),'origin_receipt':'witness:copy:B'}
    c = {'id':'H_C','answers':['I remember the garden','I chose to leave','I corrected the date'],'origin_receipt':'witness:other:C'}
    histories=[a,b,c]
    classes={}
    for h in histories:
        classes.setdefault(observation(h),[]).append(h['id'])
    assert observation(a)==observation(b)
    assert a['id']!=b['id']
    assert witness(a)!=witness(b)
    assert observation(a)!=observation(c)
    assert len(classes)==2
    # Equal prior over A and B: an observation-only classifier cannot exceed 1/2 accuracy.
    posterior={'H_A':0.5,'H_B':0.5}
    assert max(posterior.values())==0.5
    report={'benchmark':'CVP-001','seed':SEED,'synthetic_histories':len(histories),'observation_equivalence_classes':len(classes),'ambiguous_class':['H_A','H_B'],'observation_only_max_accuracy_equal_prior':0.5,'witness_distinguishes_A_B':True,'claims_about_consciousness':'NONE','status':'PASS'}
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':
    run()
