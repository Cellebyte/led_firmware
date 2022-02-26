/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Error } from '../models/Error';
import type { RGB } from '../models/RGB';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class LedsService {

    /**
     * Set all Leds with the object provided also sets animation to manual.
     * @param requestBody
     * @returns Error unexpected error
     * @returns RGB The colour the led strip was set to.
     * @throws ApiError
     */
    public static postLeds(
        requestBody?: RGB,
    ): CancelablePromise<Error | RGB> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/leds/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * Get Leds RGB information from led of the strip.
     * @param ledId The id of the led on the strip
     * @returns RGB The colour the led strip was set to.
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static getLeds(
        ledId: number,
    ): CancelablePromise<RGB | Error> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/leds/{led_id}/',
            path: {
                'led_id': ledId,
            },
        });
    }

    /**
     * Set Leds of this id with the object provided also sets animation to manual.
     * @param ledId The id of the led on the strip
     * @param requestBody
     * @returns Error unexpected error
     * @returns RGB The colour the led strip was set to.
     * @throws ApiError
     */
    public static postLeds1(
        ledId: number,
        requestBody?: RGB,
    ): CancelablePromise<Error | RGB> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/leds/{led_id}/',
            path: {
                'led_id': ledId,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}