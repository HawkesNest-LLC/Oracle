export type Status = 'ESTABLISHED' | 'RECONSTRUCTED' | 'PROPOSED' | 'SIMULATED' | 'SUPERSEDED' | 'REJECTED' | 'UNKNOWN';
export type Authority = 'Creator' | 'Editor' | 'AI' | 'Reviewer' | 'Observer';
export interface ESPEnvelope { claimId: string; status: Status; authority: Authority; confidence: number; sources: string[]; revision?: string | null; timestamp?: string; branch?: string; supersedes?: string | null; }
export declare const STATUSES: readonly Status[];
export declare const AUTHORITIES: readonly Authority[];
export declare function validateESP(value: unknown): value is ESPEnvelope;
export declare function getStatus(claim: ESPEnvelope): Status;
export declare function getAuthority(claim: ESPEnvelope): Authority;
export declare function getSources(claim: ESPEnvelope): string[];
export declare function traceRevision(claim: ESPEnvelope, lookup: (id: string) => ESPEnvelope | null): ESPEnvelope[];