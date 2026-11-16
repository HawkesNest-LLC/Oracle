'use strict';
const SOURCES={
core:{title:'Temporal Core creator-approved specification',url:'https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/JUPITER_STATION_TEMPORAL_CORE_CANON_2397.md'},
order:{title:'November 5 creator order',url:'https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/fiction/canon/2026-11-05_JUPITER_STATION_CREATOR_ORDER_STORY_IS_CANON.md'}};
const PLACES=[
{id:'station',name:'Jupiter Station',x:160,y:95,source:'core',fact:'Jupiter Station operates a Temporal Core for observing resolvable branches, not transporting the station through time.'},
{id:'core',name:'Temporal Core',x:400,y:95,source:'core',fact:'The Core uses causal addressing, observational locks, isolated capture, provenance review and separate records.'},
{id:'avalon',name:'USS Avalon',x:160,y:260,source:'order',fact:'Captain Noah Hawkes commands USS Avalon, registry NCC-75154.'},
{id:'command',name:'Station Command',x:400,y:260,source:'order',fact:'Captain Ashley Hawkes independently commands Jupiter Station.'}];
const EDGES=[['station','core'],['station','avalon'],['station','command']];
function respond(input){
const q=String(input||'').trim().toLowerCase();
if(!q)return {status:'UNKNOWN',text:'Ask about Jupiter Station, Avalon, command, or the Temporal Core.',places:[],sources:[]};
if(/diameter|height|width|deck count|how many decks|distance|coordinates|population|dimensions|size of/.test(q))return {status:'UNKNOWN',text:'No inspected source establishes that measurement. The schematic is a visual placeholder.',places:[],sources:[]};
const found=PLACES.filter(p=>p.name.toLowerCase().includes(q)||q.includes(p.name.toLowerCase())||(p.id==='command'&&/ashley|captain|command/.test(q))||(p.id==='avalon'&&/noah|ship/.test(q))||(p.id==='core'&&/temporal|branch/.test(q))||(p.id==='station'&&/jupiter|station/.test(q)));
return found.length?{status:'ESTABLISHED',text:found.map(p=>p.fact).join(' '),places:found.map(p=>p.id),sources:[...new Set(found.map(p=>p.source))]}:{status:'UNKNOWN',text:'No indexed evidence supports that answer. No detail has been invented.',places:[],sources:[]};}
if(typeof module!=='undefined')module.exports={SOURCES,PLACES,EDGES,respond};