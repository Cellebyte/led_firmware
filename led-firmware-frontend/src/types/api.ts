/* tslint:disable */
/* eslint-disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface RGB {
  red: number;
  green: number;
  blue: number;
}

export interface ColourPalettes {
  colour_palettes: number[];
  amount: number;
  slots: number;
}

export type ColourPalette = Record<string, RGB>;

export interface AnimationObject {
  animation: Animation;
}

export enum Animation {
  Snake = "snake",
  Normal = "normal",
  Breath = "breath",
  Rainbow = "rainbow",
  Off = "off",
  Manual = "manual",
}

export type SnakeAnimation = NormalAnimation & { length?: number; steps?: number; direction?: AnimationDirection };

export type PolyAnimation = NormalAnimation | SnakeAnimation | BreathAnimation | RainbowAnimation;

export interface RainbowAnimation {
  period?: number;
}

export type BreathAnimation = NormalAnimation & { dim_percentage?: number };

export interface NormalAnimation {
  animation?: Animation;
  colour_selectors?: number[];
  palette_selector?: number;
  current_colour?: RGB;
  change_colour?: boolean;
}

export enum AnimationDirection {
  Up = "up",
  Down = "down",
}

export interface Error {
  code: number;
  error: string;
}

export interface LenObject {
  first: number;
  last: number;
}

export type RequestParams = Omit<RequestInit, "body" | "method"> & {
  secure?: boolean;
};

interface ApiConfig<SecurityDataType> {
  baseUrl?: string;
  baseApiParams?: RequestParams;
  securityWorker?: (securityData: SecurityDataType) => RequestParams;
}

interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D | null;
  error: E | null;
}

enum BodyType {
  Json,
}

class HttpClient<SecurityDataType> {
  public baseUrl: string = "http://leds.example.com";
  private securityData: SecurityDataType = null as any;
  private securityWorker: null | ApiConfig<SecurityDataType>["securityWorker"] = null;

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType) => {
    this.securityData = data;
  };

  private bodyFormatters: Record<BodyType, (input: any) => any> = {
    [BodyType.Json]: JSON.stringify,
  };

  private mergeRequestOptions(params: RequestParams, securityParams?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params,
      ...(securityParams || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params.headers || {}),
        ...((securityParams && securityParams.headers) || {}),
      },
    };
  }

  private safeParseResponse = <T = any, E = any>(response: Response): Promise<HttpResponse<T, E>> => {
    const r = response as HttpResponse<T, E>;
    r.data = null;
    r.error = null;

    return response
      .json()
      .then((data) => {
        if (r.ok) {
          r.data = data;
        } else {
          r.error = data;
        }
        return r;
      })
      .catch((e) => {
        r.error = e;
        return r;
      });
  };

  public request = <T = any, E = any>(
    path: string,
    method: string,
    { secure, ...params }: RequestParams = {},
    body?: any,
    bodyType?: BodyType,
    secureByDefault?: boolean,
  ): Promise<HttpResponse<T>> => {
    const requestUrl = `${this.baseUrl}${path}`;
    const secureOptions =
      (secureByDefault || secure) && this.securityWorker ? this.securityWorker(this.securityData) : {};
    const requestOptions = {
      ...this.mergeRequestOptions(params, secureOptions),
      method,
      body: body ? this.bodyFormatters[bodyType || BodyType.Json](body) : null,
    };

    return fetch(requestUrl, requestOptions).then(async (response) => {
      const data = await this.safeParseResponse<T, E>(response);
      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title LED Firmware API
 * @version 1.0.0
 * @baseUrl http://leds.example.com
 */
export class Api<SecurityDataType = any> extends HttpClient<SecurityDataType> {
  palettes = {
    /**
     * @tags colour_palettes
     * @name get_palettes
     * @summary List all colour palettes available on the MicroController
     * @request GET:/palettes/
     */
    getPalettes: (params?: RequestParams) => this.request<ColourPalettes, Error>(`/palettes/`, "GET", params),

    /**
     * @tags colour_palettes
     * @name get_palette
     * @summary Get all colours from a colour_palette from the MicroController
     * @request GET:/palettes/{pallette_id}/
     */
    getPalette: (pallette_id: number, params?: RequestParams) =>
      this.request<ColourPalette, Error>(`/palettes/${pallette_id}/`, "GET", params),

    /**
     * @tags colours
     * @name post_colours
     * @summary Insert a new colour into the colour_palette
     * @request POST:/palettes/{pallette_id}/colours/
     */
    postColours: (pallette_id: number, data: RGB, params?: RequestParams) =>
      this.request<ColourPalette, Error>(`/palettes/${pallette_id}/colours/`, "POST", params, data),

    /**
     * @tags colours
     * @name delete_colours
     * @summary Delete all colours from a colour_palette from the MicroController
     * @request DELETE:/palettes/{pallette_id}/colours/
     */
    deleteColours: (pallette_id: number, params?: RequestParams) =>
      this.request<ColourPalette, Error>(`/palettes/${pallette_id}/colours/`, "DELETE", params),

    /**
     * @tags colours
     * @name get_colours
     * @summary Get all colours from a colour_palette from the MicroController
     * @request GET:/palettes/{pallette_id}/colours/
     */
    getColours: (pallette_id: number, params?: RequestParams) =>
      this.request<ColourPalette, Error>(`/palettes/${pallette_id}/colours/`, "GET", params),

    /**
     * @tags colours
     * @name post_colour
     * @summary Store a colour into the colour_palette from the MicroController at this slot
     * @request POST:/palettes/{pallette_id}/colours/{colour_id}/
     */
    postColour: (pallette_id: number, colour_id: number, data: RGB, params?: RequestParams) =>
      this.request<RGB, Error>(`/palettes/${pallette_id}/colours/${colour_id}/`, "POST", params, data),

    /**
     * @tags colours
     * @name delete_colour
     * @summary Delete a colour in the colour_palette from the MicroController at this slot
     * @request DELETE:/palettes/{pallette_id}/colours/{colour_id}/
     */
    deleteColour: (pallette_id: number, colour_id: number, params?: RequestParams) =>
      this.request<RGB, Error>(`/palettes/${pallette_id}/colours/${colour_id}/`, "DELETE", params),

    /**
     * @tags colours
     * @name get_colour
     * @summary Get a specific colour from a colour_palette from the MicroController
     * @request GET:/palettes/{pallette_id}/colours/{colour_id}/
     */
    getColour: (pallette_id: number, colour_id: number, params?: RequestParams) =>
      this.request<RGB, Error>(`/palettes/${pallette_id}/colours/${colour_id}/`, "GET", params),
  };
  leds = {
    /**
     * @tags leds
     * @name post_leds
     * @summary Set all Leds with the object provided also sets animation to manual.
     * @request POST:/leds/
     */
    postLeds: (data: RGB, params?: RequestParams) => this.request<RGB, Error>(`/leds/`, "POST", params, data),

    /**
     * @tags leds
     * @name get_leds
     * @summary Get Leds RGB information from led of the strip.
     * @request GET:/leds/{led_id}/
     */
    getLeds: (led_id: number, params?: RequestParams) => this.request<RGB, Error>(`/leds/${led_id}/`, "GET", params),

    /**
     * @tags leds
     * @name post_leds
     * @summary Set Leds of this id with the object provided also sets animation to manual.
     * @request POST:/leds/{led_id}/
     * @originalName postLeds
     * @duplicate
     */
    postLeds2: (led_id: number, data: RGB, params?: RequestParams) =>
      this.request<RGB, Error>(`/leds/${led_id}/`, "POST", params, data),
  };
  lens = {
    /**
     * @tags lenth
     * @name get_strip
     * @summary Get the length of the led strip
     * @request GET:/lens/
     */
    getStrip: (params?: RequestParams) => this.request<LenObject, Error>(`/lens/`, "GET", params),
  };
  gc = {
    /**
     * @tags debug
     * @name gc
     * @summary Trigger manual gc for debugging memory
     * @request GET:/gc/
     */
    gc: (params?: RequestParams) => this.request<object, any>(`/gc/`, "GET", params),
  };
  animation = {
    /**
     * @tags animation
     * @name get_animation
     * @summary Get the current active animation
     * @request GET:/animation/
     */
    getAnimation: (params?: RequestParams) => this.request<AnimationObject, Error>(`/animation/`, "GET", params),

    /**
     * @tags animation
     * @name put_animation
     * @summary Update to the provied animation.
     * @request PUT:/animation/
     */
    putAnimation: (data: AnimationObject, params?: RequestParams) =>
      this.request<AnimationObject, Error>(`/animation/`, "PUT", params, data),

    /**
     * @tags animation
     * @name animationDetail
     * @summary Get current configuration for the provided animation
     * @request GET:/animation/{animation}
     */
    animationDetail: (animation: Animation, params?: RequestParams) =>
      this.request<PolyAnimation, Error>(`/animation/${animation}`, "GET", params),

    /**
     * @tags animation
     * @name animationUpdate
     * @summary Update the configuration for the provided animation
     * @request PUT:/animation/{animation}
     */
    animationUpdate: (animation: Animation, data: PolyAnimation, params?: RequestParams) =>
      this.request<PolyAnimation, Error>(`/animation/${animation}`, "PUT", params, data),
  };
}
