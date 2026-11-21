(() => {
'use strict';
const key='cc90_state_v1';
const sources={
 'cc-order':{id:'cc-order',title:'Executive Build Order CC-90-001',uri:'https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md'},
 'assessment':{id:'assessment',title:'Nov 2 candidate assessment',uri:'https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-02_CONTINUITY_AWARE_SIMULATION_RUNTIME_ASSESSMENT.md'}
};
const claims=[
 {id:'arrival_event',statement:'Original primary source establishing the exact circumstances of the fictional Captain\'s 2371 arrival has not been loaded.',status:'UNKNOWN',authority:'Reviewer',confidence:0,sources:[],era:'2371'},
 {id:'arrival_hypothesis',statement:'A candidate engineering example says Noah arrived aboard Voyager in 2371. The original scene has not been verified.',status:'PROPOSED',authority:'AI',confidence:.3,sources:['assessment'],era:'2371'},
 {id:'demo_scope',statement:'The first demonstration is Voyager Sickbay, a corridor, and an Avalon 2397 placeholder.',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],era:'2371'},
 {id:'biobed_geometry',statement:'Biobeds and console are required blockout elements, not authenticated original scene geometry.',status:'RECONSTRUCTED',authority:'AI',confidence:.9,sources:['cc-order'],era:'2371'},
 {id:'branch_separation',statement:'Simulation cannot promote itself into Creator-approved canon.',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],era:'2371'},
 {id:'avalon_placeholder',statement:'Avalon Bridge 2397 is a placeholder, not a complete reconstructed bridge.',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],era:'2397'}
];
const locations={
 'voyager-sickbay':{label:'Voyager · Sickbay',short:'Sickbay',era:'2371'},
 'voyager-corridor':{label:'Voyager · Corridor',short:'Corridor',era:'2371'},
 'avalon-bridge':{label:'Avalon · Bridge',short:'Bridge',era:'2397'}
};
const defaultState=()=>({era:'2371',location:'voyager-sickbay',mode:'replay',visited:['voyager-sickbay'],tab:'claims',events:[],branchId:'sim-local'});
let state=defaultState();
try{const saved=JSON.parse(localStorage.getItem(key)||'null');if(saved&&locations[saved.location]&&['replay','simulation'].includes(saved.mode)){state={...defaultState(),...saved};if(!Array.isArray(state.visited))state.visited=['voyager-sickbay'];if(!Array.isArray(state.events))state.events=[];}}catch{}
const $=(id)=>document.getElementById(id);
const escapeHTML=(s)=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function persist(){try{localStorage.setItem(key,JSON.stringify(state));$('save-indicator').textContent='Saved locally · '+new Date().toLocaleTimeString();}catch{$('save-indicator').textContent='Storage unavailable';}}
function visit(location){if(!locations[location])return;state.location=location;state.era=locations[location].era;if(!state.visited.includes(location))state.visited.push(location);if(state.mode==='simulation'){state.events.push({id:Date.now().toString(36),action:'visit',location,era:state.era,at:new Date().toISOString(),status:'SIMULATED'});state.events=state.events.slice(-100);}persist();render();}
function fixture(label,small,klass,action){const b=document.createElement('button');b.type='button';b.className='fixture '+klass;b.innerHTML=escapeHTML(label)+'<small>'+escapeHTML(small)+'</small>';b.addEventListener('click',action);return b;}
function room(){const el=$('room');el.replaceChildren();const loc=state.location;
 if(loc==='voyager-sickbay'){
  el.append(fixture('BIOBED 01','RECONSTRUCTED','biobed a',()=>showClaim('biobed_geometry')));
  el.append(fixture('BIOBED 02','RECONSTRUCTED','biobed b',()=>showClaim('biobed_geometry')));
  el.append(fixture('OBSERVATION','BLOCKOUT','observation',()=>showClaim('demo_scope')));
  el.append(fixture('CONTINUITY','EVIDENCE CONSOLE','console',()=>showClaim('arrival_event')));
  el.append(fixture('CORRIDOR','EXIT','door',()=>visit('voyager-corridor')));
 }else if(loc==='voyager-corridor'){
  el.append(fixture('SICKBAY','RETURN','corridor-door',()=>visit('voyager-sickbay')));
 }else{
  el.append(fixture('AVALON','BRIDGE PLACEHOLDER','bridge-console',()=>showClaim('avalon_placeholder')));
  el.append(fixture('COMMAND','2397','captain-chair',()=>showClaim('avalon_placeholder')));
 }
}
function render(){document.body.classList.toggle('simulation',state.mode==='simulation');const loc=locations[state.location];$('scene-title').textContent=loc.label;$('scene-subtitle').textContent=loc.era+' · '+(state.mode==='replay'?'Home branch · Canon Replay':'Isolated local simulation');$('state-location').textContent=loc.short;$('state-era').textContent=loc.era;$('state-visited').textContent=state.visited.length;
 document.querySelectorAll('[data-era]').forEach(b=>b.classList.toggle('active',b.dataset.era===state.era));document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===state.mode));document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('active',b.dataset.tab===state.tab));
 $('move-back').disabled=state.location!=='voyager-sickbay';$('move-forward').disabled=state.location!=='voyager-corridor';room();renderDetails();}
function showClaim(id){state.tab='claims';persist();render();const element=document.querySelector('[data-claim="'+id+'"]');if(element){element.open=true;element.scrollIntoView({behavior:'smooth',block:'nearest'});}}
function renderDetails(){const target=$('details');target.replaceChildren();if(state.tab==='claims'){
 const relevant=claims.filter(c=>c.era===state.era);for(const c of relevant){const details=document.createElement('details');details.className='claim';details.dataset.claim=c.id;const src=c.sources.map(s=>sources[s]).filter(Boolean);
 details.innerHTML='<summary class="claim-title"><strong>'+escapeHTML(c.id.replaceAll('_',' '))+'</strong><span class="tag '+c.status+'">'+c.status+'</span></summary><p>'+escapeHTML(c.statement)+'</p><div class="source-details">Authority: '+escapeHTML(c.authority)+' · Confidence: '+Math.round(c.confidence*100)+'%<p>Sources: '+(src.length?src.map(s=>'<a href="'+escapeHTML(s.uri)+'" target="_blank" rel="noopener noreferrer">'+escapeHTML(s.title)+'</a>').join('<br>'):'None inspected')+'</p></div>';
 target.append(details);}
 }else if(state.tab==='graph'){
 target.innerHTML='<p class="footnote">A dependency graph for the demonstration. Impact markers identify review targets, never automatically rewrite them.</p><div class="graph-row"><span class="graph-node">demo_scope</span><span class="graph-arrow">→ supports →</span><span class="graph-node">biobed_geometry</span></div><div class="graph-row"><span class="graph-node">demo_scope</span><span class="graph-arrow">→ depends →</span><span class="graph-node">avalon_placeholder</span></div><div class="graph-row"><span class="graph-node">arrival_hypothesis</span><span class="graph-arrow">⇢ review ⇢</span><span class="graph-node">arrival_event</span></div><p class="footnote">Correction propagation is an explicit review signal, not silent canon mutation.</p>';
 }else{
 if(state.events.length===0)target.innerHTML='<p class="footnote">No simulated visits yet. Switch to Simulation and enter a room to append a local event. Canon Replay stays read-only.</p>';
 else state.events.slice().reverse().forEach(e=>{const d=document.createElement('div');d.className='event';d.innerHTML='<strong>SIMULATED</strong> '+escapeHTML(e.action)+' · '+escapeHTML(locations[e.location]?.short||e.location)+'<br><small>'+escapeHTML(e.at)+'</small>';target.append(d);});
 }}
 document.querySelectorAll('[data-era]').forEach(b=>b.addEventListener('click',()=>visit(b.dataset.era==='2371'?'voyager-sickbay':'avalon-bridge')));
 document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{state.mode=b.dataset.mode;persist();render();}));
 document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{state.tab=b.dataset.tab;persist();render();}));
 $('inspect-console').addEventListener('click',()=>showClaim('arrival_event'));
 $('move-back').addEventListener('click',()=>visit('voyager-corridor'));
 $('move-forward').addEventListener('click',()=>visit('voyager-sickbay'));
 $('reset').addEventListener('click',()=>{state=defaultState();persist();render();});
 render();persist();
})();