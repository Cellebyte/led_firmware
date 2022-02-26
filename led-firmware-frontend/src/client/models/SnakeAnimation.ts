/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AnimationDirection } from './AnimationDirection';
import type { NormalAnimation } from './NormalAnimation';

export type SnakeAnimation = (NormalAnimation & {
    length?: number;
    steps?: number;
    direction?: AnimationDirection;
});
