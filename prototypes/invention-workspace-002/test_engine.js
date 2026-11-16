'use strict';
const assert=require('node:assert/strict');
const {respond,PLACES,EDGES,SOURCES}=require('./engine.js');
const cases=[
['Who commands Avalon?','avalon'],['Who commands Jupiter Station?','command'],
['What is the Temporal Core?','core'],['Tell me about Jupiter Station','station'],
['Noah','avalon'],['Ashley','command']
];
for(const [q,id] of cases){const r=respond(q);assert.equal(r.status,'SOURCE_LINKED',q);assert.deepEqual(r.places,[id],q);assert.equal(r.sources.length,1,q)}
for(const q of ['How many decks?','What is its diameter?','What is the population?','Who commands Avalon and Jupiter Station?','Tell me about the Borg','']){
const r=respond(q);assert.equal(r.status,'UNKNOWN',q);assert.equal(r.sources.length,0,q)}
assert.equal(PLACES.length,4);assert.equal(EDGES.length,3);
assert.ok(PLACES.every(p=>SOURCES[p.source].url.startsWith('https://github.com/')));
console.log('PASS: 15 retrieval and source-boundary assertions');
