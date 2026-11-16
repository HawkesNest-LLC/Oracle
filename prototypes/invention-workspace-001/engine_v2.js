'use strict';
const base = typeof module !== 'undefined' && module.exports ? require('./engine.js') : {SOURCES,PLACES,EDGES};
function respond(input){
 const q=String(input??'').trim().toLowerCase();
 const unknown=(reason)=>({status:'UNKNOWN',text:reason,places:[],sources:[]});
 if(!q)return unknown('Ask about Jupiter Station, Avalon, command, or the Temporal Core.');
 if(/\b(diameter|height|width|wide|tall|distance|coordinates|population|dimensions|size|decks?|levels?|length|meters?|kilometers?)\b/.test(q))return unknown('No inspected source establishes that measurement. The schematic is a visual placeholder.');
 const avalon=/\bavalon\b|\bncc-75154\b/.test(q);
 const station=/\bjupiter station\b|\bstation command\b/.test(q);
 const temporal=/\btemporal core\b|\bcausal addressing\b|\bobservation(?:al)? locks?\b/.test(q);
 const explicit=[avalon&&'avalon',station&&'station',temporal&&'core'].filter(Boolean);
 if(explicit.length>1)return unknown('This question mentions multiple subjects. Ask about one location or command at a time.');
 const command=/\b(who|captain|commands?|commanding|leadership|ashley|noah)\b/.test(q);
 let id=null;
 if(avalon)id='avalon';
 else if(station)id=command?'command':'station';
 else if(temporal)id='core';
 else if(/^\s*(?:ashley|captain ashley)\s*[?.!]*$/.test(q))id='command';
 else if(/^\s*(?:noah|captain noah)\s*[?.!]*$/.test(q))id='avalon';
 else if(/^\s*(?:station|core|command)\s*[?.!]*$/.test(q))id={station:'station',core:'core',command:'command'}[q.replace(/[?.!]/g,'').trim()];
 if(!id)return unknown('No indexed evidence supports that answer. No detail has been invented.');
 const p=base.PLACES.find(x=>x.id===id);
 return {status:'ESTABLISHED',text:p.fact,places:[p.id],sources:[p.source]};
}
if(typeof module!=='undefined'&&module.exports)module.exports={...base,respond};
else window.respondV2=respond;