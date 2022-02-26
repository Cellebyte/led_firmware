/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RGB } from './RGB';

export type NormalAnimation = {
    animation?: 'normal';
    colour_selectors?: Array<number>;
    palette_selector?: number;
    current_colour?: RGB;
    change_colour?: boolean;
};
