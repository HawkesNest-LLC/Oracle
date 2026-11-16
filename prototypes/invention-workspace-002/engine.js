'use strict';
const SOURCES=Object.freeze({
core:{title:'Temporal Core approved specification',url:'https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/JUPITER_STATION_TEMPORAL_CORE_CANON_2397.md'},
order:{title:'November 5 creator order',url:'https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/fiction/canon/2026-11-05_JUPITER_STATION_CREATOR_ORDER_STORY_IS_CANON.md'}});
const PLACES=Object.freeze([
{id:'station',name:'Jupiter Station',x:155,y:80,source:'core',fact:'Jupiter Station operates a Temporal Core for observing resolvable branches, not transporting the station through time.'},
{id:'core',name:'Temporal Core',x:405,y:80,source:'core',fact:'The Core uses causal addressing, observational locks, isolated capture, provenance review and separate records.'},
{id:'avalon',name:'USS Avalon',x:155,y:235,source:'order',fact:'Captain Noah Hawkes commands USS Avalon, registry NCC-75154.'},
{id:'command',name:'Station Command',x:405,y:235,source:'order',fact:'Captain Ashley Hawkes independently commands Jupiter Station.'}]);
const EDGES=Object.freeze([['station','core'],['station','avalon'],['station','command']]);
function result(ids){const places=PLACES.filter(p=>ids.includes(p.id));return {status:'SOURCE_LINKED',text:places.map(p=>p.fact).join(' '),places:places.map(p=>p.id),sources:[...new Set(places.map(p=>p.source))]};}
function respond(input){
const q=String(input||'').toLowerCase().trim().replace(/[^a-z0-9\s-]/g,' ').replace(/\s+/g,' ');
const unknown=(text='This limited source index cannot support that answer.')=>({status:'UNKNOWN',text,places:[],sources:[]});
if(!q)return unknown('Ask about Jupiter Station, Avalon, station command or the Temporal Core.');
if(/\b(diameter|height|width|deck|decks|distance|coordinates|population|dimensions|size|meters|kilometers|residents|how many)\b/.test(q))return unknown('The inspected sources do not establish that measurement. Schematic geometry is illustrative.');
const avalon=/\b(avalon|noah|ncc-75154)\b/.test(q);
const station=/\b(jupiter station|station)\b/.test(q);
const core=/\b(temporal core|temporal|branch|causal)\b/.test(q);
const ashley=/\b(ashley|station command)\b/.test(q);
const command=/\b(command|commands|captain|captains|in charge|leads|leader)\b/.test(q);
if(avalon&&station)return unknown('The question mentions both Avalon and Jupiter Station. Ask about one command at a time.');
if(avalon)return result(['avalon']);
if(ashley)return result(['command']);
if(station&&command)return result(['command']);
if(core)return result(['core']);
if(station)return result(['station']);
return unknown();
}
if(typeof module!=='undefined')module.exports={SOURCES,PLACES,EDGES,respond};
