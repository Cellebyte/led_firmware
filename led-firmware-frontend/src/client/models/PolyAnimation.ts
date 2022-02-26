/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { BreathAnimation } from './BreathAnimation';
import type { NormalAnimation } from './NormalAnimation';
import type { RainbowAnimation } from './RainbowAnimation';
import type { SnakeAnimation } from './SnakeAnimation';

export type PolyAnimation = (NormalAnimation | SnakeAnimation | BreathAnimation | RainbowAnimation);
