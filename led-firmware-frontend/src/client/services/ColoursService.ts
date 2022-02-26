/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ColourPalette } from '../models/ColourPalette';
import type { Error } from '../models/Error';
import type { RGB } from '../models/RGB';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ColoursService {

    /**
     * Insert a new colour into the colour_palette
     * @param palletteId The id of the colour_palette
     * @param requestBody
     * @returns Error unexpected error
     * @returns ColourPalette The color stored in the colour_palette with its index
     * @throws ApiError
     */
    public static postColours(
        palletteId: number,
        requestBody?: RGB,
    ): CancelablePromise<Error | ColourPalette> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/palettes/{pallette_id}/colours/',
            path: {
                'pallette_id': palletteId,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * Delete all colours from a colour_palette from the MicroController
     * @param palletteId The id of the colour_palette
     * @returns ColourPalette All deleted colors which were stored in a colour_palette
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static deleteColours(
        palletteId: number,
    ): CancelablePromise<ColourPalette | Error> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/palettes/{pallette_id}/colours/',
            path: {
                'pallette_id': palletteId,
            },
        });
    }

    /**
     * Get all colours from a colour_palette from the MicroController
     * @param palletteId The id of the colour_palette
     * @returns ColourPalette Get all colors stored in a colour_palette
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static getColours(
        palletteId: number,
    ): CancelablePromise<ColourPalette | Error> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/palettes/{pallette_id}/colours/',
            path: {
                'pallette_id': palletteId,
            },
        });
    }

    /**
     * Store a colour into the colour_palette from the MicroController at this slot
     * @param palletteId The id of the colour_palette
     * @param colourId The id of the colour in the colour_palette
     * @param requestBody
     * @returns Error unexpected error
     * @returns RGB The color stored in the colour_palette
     * @throws ApiError
     */
    public static postColours1(
        palletteId: number,
        colourId: number,
        requestBody?: RGB,
    ): CancelablePromise<Error | RGB> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/palettes/{pallette_id}/colours/{colour_id}/',
            path: {
                'pallette_id': palletteId,
                'colour_id': colourId,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * Delete a colour in the colour_palette from the MicroController at this slot
     * @param palletteId The id of the colour_palette
     * @param colourId The id of the colour in the colour_palette
     * @returns RGB The color stored in the colour_palette
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static deleteColours1(
        palletteId: number,
        colourId: number,
    ): CancelablePromise<RGB | Error> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/palettes/{pallette_id}/colours/{colour_id}/',
            path: {
                'pallette_id': palletteId,
                'colour_id': colourId,
            },
        });
    }

    /**
     * Get a specific colour from a colour_palette from the MicroController
     * @param palletteId The id of the colour_palette
     * @param colourId The id of the colour in the colour_palette
     * @returns RGB Get the specific colour of a slot
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static getColours1(
        palletteId: number,
        colourId: number,
    ): CancelablePromise<RGB | Error> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/palettes/{pallette_id}/colours/{colour_id}/',
            path: {
                'pallette_id': palletteId,
                'colour_id': colourId,
            },
        });
    }

}