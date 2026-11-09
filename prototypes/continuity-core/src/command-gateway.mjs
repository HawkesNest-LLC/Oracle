import {createHmac, timingSafeEqual} from 'node:crypto';
const stable=x=>JSON.stringify(x);
const mac=(key,request)=>createHmac('sha256',key).update(stable(request)).digest('hex');
const safe=(a,b)=>typeof a==='string'&&typeof b==='string'&&a.length===b.length&&timingSafeEqual(Buffer.from(a),Buffer.from(b));
/**
 * Development-only authenticated gateway. Keys are injected by the host, never stored in source.
 * The nonce store must be persistent and transactional before this can be used across restarts.
 * Never expose the underlying BridgeStateMachine or AvalonClock mutators to untrusted callers.
 */
export class CommandGateway {
  constructor({captainKey,schedulerKey,nonceStore}={}) {
    if(!captainKey||!schedulerKey||captainKey===schedulerKey)throw Error('Distinct keys required');
    if(!nonceStore||typeof nonceStore.claim!=='function')throw Error('Persistent nonce store required');
    this.keys={captain:captainKey,scheduler:schedulerKey};
    this.nonces=nonceStore;
  }
  static sign(key,request){return mac(key,request);}
  authorize({role,operation,request,signature}) {
    if(!Object.hasOwn(this.keys,role))throw Error('Unknown role');
    const permitted=role==='captain'?['issue','schedule']:['tick','reconcile'];
    if(!permitted.includes(operation))throw Error('Role not permitted');
    if(!request||typeof request.nonce!=='string'||!request.nonce.trim()||typeof request.branch!=='string')throw Error('Invalid request');
    if(!safe(mac(this.keys[role],{role,operation,request}),signature))throw Error('Invalid signature');
    if(!this.nonces.claim(role,request.nonce))throw Error('Replay rejected');
    return {role,operation,branch:request.branch};
  }
}
