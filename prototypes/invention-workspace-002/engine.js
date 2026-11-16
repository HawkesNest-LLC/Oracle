'use strict';
// Conservative deterministic index. Source-linked answers require a supported subject AND intent.
const SOURCES=Object.freeze({
core:{title:'Temporal Core approved specification',url:'https://github.com/HawkesNest-LLC/Oracle/blob/c60544ee171ad00412227c7e8f93e733efc2c17b/docs/rendered-reality/JUPITER_STATION_TEMPORAL_CORE_CANON_2397.md',blob:'0fae0104bf528a639dfcdfe6d4d45b59ee10386c'},
order:{title:'November 5 creator order',url:'https://github.com/HawkesNest-LLC/Oracle/blob/c60544ee171ad00412227c7e8f93e733efc2c17b/docs/rendered-reality/fiction/canon/2026-11-05_JUPITER_STATION_CREATOR_ORDER_STORY_IS_CANON.md',blob:'08489e83b212b1ead6645736b2691fc23905c2a0'}});
const PLACES=Object.freeze([
{id:'station',name:'Jupiter Station',x:155,y:80,source:'core',fact:'Jupiter Station operates a Temporal Core for observing resolvable branches, not transporting the station through time.'},
{id:'core',name:'Temporal Core',x:405,y:80,source:'core',fact:'The Core uses causal addressing, observational locks, isolated capture, provenance review and separate records.'},
{id:'avalon',name:'USS Avalon',x:155,y:235,source:'order',fact:'Captain Noah Hawkes commands USS Avalon, registry NCC-75154.'},
{id:'command',name:'Station Command',x:405,y:235,source:'order',fact:'Captain Ashley Hawkes independently commands Jupiter Station.'}]);
const EDGES=Object.freeze([['station','core'],['station','avalon'],['station','command']]);
function result(id){const p=PLACES.find(x=>x.id===id);return {status:'SOURCE_LINKED',text:p.fact,places:[p.id],sources:[p.source]};}
function respond(input){
 const q=String(input||'').toLowerCase().trim().replace(/[^a-z0-9\s-]/g,' ').replace(/\s+/g,' ');
 const unknown=(text='This limited source index cannot support that answer.')=>({status:'UNKNOWN',text,places:[],sources:[]});
 if(!q)return unknown('Ask about Jupiter Station, Avalon, station command or the Temporal Core.');
 // Question scope matters more than entity mentions. Never answer unrelated predicates with a known entity fact.
 if(/\b(diameter|height|width|deck|decks|distance|coordinates|population|dimensions|size|meters|kilometers|residents|how many|color|colour|when|date|year|power|output|weigh|weight|cloaking|cloak|breakfast|eat|food|deploy|activate|attack|borg|address|old|age|medical|history|exact position|position|docking|ports|equipped)\b/.test(q))return unknown();
 const avalon=/\b(avalon|noah|ncc-75154|starship|ship)\b/.test(q);
 const station=/\b(jupiter station|station)\b/.test(q);
 const core=/\b(temporal core|temporal|branch|causal|observational lock)\b/.test(q);
 const ashley=/\b(ashley|station command)\b/.test(q);
 const command=/\b(command|commands|captain|captains|in charge|leads|leader)\b/.test(q);
 if(avalon&&station)return unknown('The question mentions both ship and station. Ask about one at a time.');
 if(/\b(what is|tell me about|explain|describe|show|source|who|does|is|name|registration|registry)\b/.test(q)===false && !/^(avalon|noah|ashley|jupiter station|temporal core|uss avalon)$/.test(q))return unknown();
 if(avalon){if(/\b(who|captain|command|commands|name|registration|registry|source|show|tell me about)\b/.test(q)||/^(avalon|noah|uss avalon)$/.test(q))return result('avalon');return unknown();}
 if(ashley){if(command||/^(ashley|station command)$/.test(q))return result('command');return unknown();}
 if(station&&command)return result('command');
 if(core){if(/\b(what is|tell me about|explain|describe|does|is)\b/.test(q)||/^(temporal core)$/.test(q))return result('core');return unknown();}
 if(station){if(/\b(what is|tell me about|describe)\b/.test(q)||q==='jupiter station')return result('station');return unknown();}
 return unknown();
}
if(typeof module!=='undefined')module.exports={SOURCES,PLACES,EDGES,respond};
