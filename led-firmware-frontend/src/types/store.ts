import { Api } from '@/types/api';
import { LedFirmwareFrontendConfiguration } from '@/types/config';

export interface RootState {
    version: string
    config: LedFirmwareFrontendConfiguration
    api: Api
}

// export interface CIDRDict {
//     [id: string] : CIDR
// }

// export interface PoolDict {
//     [id: string] : Pool
// }

// export interface TokenDict {
//     [id: string]: Token
// }
// export interface SearchState {
//     query: string;
//     search: Object;
// }

// export interface BasicToken {
//     access: string| undefined;
//     refresh: string | undefined;
//     [key: string]: any;
// }
// export interface AuthState {
//     token: BasicToken;
//     username: String;
//     loggedIn: boolean;
// }

// export interface CIDRGet extends CIDR {
//     id : string | ''
// }
// export interface CIDRState {
//     cidrs: CIDRDict;
//     root: Set<string>
//     search: CIDRDict;
// }

// export interface PoolState {
//     pools: PoolDict
// }

// export interface TokenState {
//     tokens: TokenDict
// }
