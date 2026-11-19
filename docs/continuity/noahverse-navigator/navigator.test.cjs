'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(__dirname+'/navigator.js','utf8');
const nodes=new Map();
function node(tag='div'){return {tagName:tag,children:[],textContent:'',value:'',disabled:false,append(...v){this.children.push(...v)},replaceChildren(...v){this.children=v},addEventListener(type,cb){this['on'+type]=cb},set href(v){this._href=v},get href(){return this._href}}}
const document={getElementById(id){if(!nodes.has(id))nodes.set(id,node());return nodes.get(id)},createElement:node,createTextNode(value){return {textContent:value}}};
const window={};
vm.runInNewContext(source,{window,document},{filename:'navigator.js'});
const app=window.NavigatorTest;
const cases=[['Take me to Jupiter Station','LOAD_WORLD'],['Who commands the station?','QUERY_COMMAND'],['Show corrections','SHOW_CORRECTIONS'],['Show Cold Ledger','SHOW_COLD_LEDGER'],['Show timeline','SHOW_TIMELINE'],['Show sources','SHOW_SOURCES'],['nonsense','UNKNOWN'],['','EMPTY']];
let count=0;
for(const [input,expected] of cases){assert.equal(app.execute(input),expected,input);count++}
assert.equal(app.sources.length,3);count++;
assert.equal(app.corrections.length,3);count++;
assert.ok(app.corrections.some(c=>c.status==='UNRESOLVED'));count++;
app.execute('Who commands the station?');assert.match(document.getElementById('reply').textContent,/Ashley commands Jupiter Station/);count++;
app.execute('Show sources');assert.equal(document.getElementById('panel').children.length,3);count++;
app.execute('Show corrections');assert.equal(document.getElementById('panel').children.length,3);count++;
app.execute('Show Cold Ledger');assert.match(document.getElementById('panel').children[0].textContent,/unresolved conflicts/);count++;
assert.ok(!source.includes('innerHTML'));count++;
console.log('PASS '+count+' navigator deterministic DOM/route assertions');
