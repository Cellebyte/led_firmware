/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ColourPalette } from '../models/ColourPalette';
import type { ColourPalettes } from '../models/ColourPalettes';
import type { Error } from '../models/Error';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ColourPalettesService {

    /**
     * List all colour palettes available on the MicroController
     * @returns ColourPalettes An overview objects of the colour_palettes
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static getPalettes(): CancelablePromise<ColourPalettes | Error> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/palettes/',
        });
    }

    /**
     * Get all colours from a colour_palette from the MicroController
     * @param palletteId The id of the colour_palette
     * @returns ColourPalette An overview
     * @returns Error unexpected error
     * @throws ApiError
     */
    public static getPalettes1(
        palletteId: number,
    ): CancelablePromise<ColourPalette | Error> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/palettes/{pallette_id}/',
            path: {
                'pallette_id': palletteId,
            },
        });
    }

}