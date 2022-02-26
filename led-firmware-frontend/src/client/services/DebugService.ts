/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DebugService {

    /**
     * Trigger manual gc for debugging memory
     * @returns any empty object
     * @throws ApiError
     */
    public static gc(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/gc/',
        });
    }

}