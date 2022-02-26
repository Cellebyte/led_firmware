/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Animation } from '../models/Animation';
import type { AnimationObject } from '../models/AnimationObject';
import type { Error } from '../models/Error';
import type { PolyAnimation } from '../models/PolyAnimation';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class AnimationService {

    /**
     * Get the current active animation
     * @returns AnimationObject The current active animation
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static getAnimation(): CancelablePromise<AnimationObject | Error> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/animation/',
        });
    }

    /**
     * Update to the provied animation.
     * @param requestBody
     * @returns Error unexpected error
     * @returns AnimationObject The new animation which got applied.
     * @throws ApiError
     */
    public static putAnimation(
        requestBody?: AnimationObject,
    ): CancelablePromise<Error | AnimationObject> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/animation/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * Get current configuration for the provided animation
     * @param animation The Animation name
     * @returns PolyAnimation Get the configuration for the specified
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static getAnimation1(
        animation: Animation,
    ): CancelablePromise<PolyAnimation | Error> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/animation/{animation}',
            path: {
                'animation': animation,
            },
        });
    }

    /**
     * Update the configuration for the provided animation
     * @param animation The Animation name
     * @param requestBody
     * @returns Error unexpected error
     * @returns PolyAnimation Update the animation settings
     * @throws ApiError
     */
    public static putAnimation1(
        animation: Animation,
        requestBody?: PolyAnimation,
    ): CancelablePromise<Error | PolyAnimation> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/animation/{animation}',
            path: {
                'animation': animation,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}