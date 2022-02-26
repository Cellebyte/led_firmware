/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Error } from '../models/Error';
import type { LenObject } from '../models/LenObject';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class LenthService {

    /**
     * Get the length of the led strip
     * @returns LenObject The current length information.
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static getStrip(): CancelablePromise<LenObject | Error> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/lens/',
        });
    }

}