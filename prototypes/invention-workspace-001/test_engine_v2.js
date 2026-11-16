const assert=require('node:assert/strict');
const old=require('./engine.js').respond;
const newer=require('./engine_v2.js').respond;
const cases=[
 ['Who commands Avalon?','avalon'],
 ['Who commands Jupiter Station?','command'],
 ['What is the Temporal Core?','core'],
 ['USS Avalon','avalon'],
 ['Jupiter Station','station'],
 ['Who commands the USS Avalon?','avalon'],
 ['Who commands Avalon and Jupiter Station?','UNKNOWN'],
 ['How many decks does Avalon have?','UNKNOWN'],
 ['What is Jupiter Station population?','UNKNOWN'],
 ['How wide is Jupiter Station?','UNKNOWN'],
 ['Where is the mess hall?','UNKNOWN'],
 ['','UNKNOWN'],
 ['Ashley','command'],
 ['Noah','avalon'],
 ['What is the station size?','UNKNOWN'],
 ['Who commands the station?','UNKNOWN']
];
let before=0,after=0;
for(const [q,expected] of cases){
 const ok=r=>expected==='UNKNOWN'?r.status==='UNKNOWN':r.status==='ESTABLISHED'&&r.places.length===1&&r.places[0]===expected;
 const a=old(q),b=newer(q);
 if(ok(a))before++;
 assert.ok(ok(b),`New engine failed ${JSON.stringify(q)}: ${JSON.stringify(b)}`);
 after++;
 console.log(JSON.stringify({q,expected,old:a.places.join(',')||a.status,new:b.places.join(',')||b.status}));
}
console.log(`BASELINE ${before}/${cases.length}; CANDIDATE ${after}/${cases.length}`);