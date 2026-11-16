'use strict';
(function(){
const $=id=>document.getElementById(id), ns='http://www.w3.org/2000/svg';
const map=$('map'),chips=$('chips'),sheet=$('sheet');
function el(name,attrs={},parent){const n=document.createElementNS(ns,name);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,v);if(parent)parent.append(n);return n}
function show(r,title='Evidence'){
$('sheet-title').textContent=title;$('status').textContent=r.status;$('detail').textContent=r.text;
$('sources').replaceChildren();
for(const id of r.sources){const a=document.createElement('a');a.href=SOURCES[id].url;a.target='_blank';a.rel='noopener noreferrer';a.textContent='View source: '+SOURCES[id].title;$('sources').append(a)}
sheet.hidden=false;
for(const g of map.querySelectorAll('[data-place]'))g.classList.toggle('selected',r.places.includes(g.dataset.place));
$('answer').textContent=r.status+': '+r.text;
}
function ask(q){const r=respond(q);show(r,'Query evidence');return r}
for(const [a,b] of EDGES){const p=PLACES.find(x=>x.id===a),q=PLACES.find(x=>x.id===b);el('line',{x1:p.x,y1:p.y,x2:q.x,y2:q.y,class:'link'},map)}
for(const p of PLACES){
const g=el('g',{class:'hit',role:'button',tabindex:'0','data-place':p.id,'aria-label':'Inspect '+p.name},map);
el('rect',{x:p.x-105,y:p.y-28,width:210,height:56,rx:12,class:'node'},g);
const t=el('text',{x:p.x,y:p.y+5},g);t.textContent=p.name;
const open=()=>{const r={status:'SOURCE_LINKED',text:p.fact,places:[p.id],sources:[p.source]};show(r,p.name)};
g.addEventListener('click',open);g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}});
const b=document.createElement('button');b.type='button';b.textContent=p.name;b.addEventListener('click',open);chips.append(b);
}
$('composer').addEventListener('submit',e=>{e.preventDefault();ask($('query').value)});
$('close').addEventListener('click',()=>{sheet.hidden=true;$('query').focus()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')sheet.hidden=true});
window.workspace002={ask};
})();
