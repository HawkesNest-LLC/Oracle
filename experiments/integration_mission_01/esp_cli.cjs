'use strict';
const fs=require('node:fs');
const esp=require('./esp_sdk.cjs');
const items=JSON.parse(fs.readFileSync(0,'utf8'));
if (!Array.isArray(items)) throw new TypeError('input must be array');
const result=items.map(item=>{
  try { return {ok:true,envelope:esp.validate(item)}; }
  catch(err) { return {ok:false,error:err.message}; }
});
process.stdout.write(JSON.stringify(result)+'\n');
