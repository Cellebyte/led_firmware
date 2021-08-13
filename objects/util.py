import objects.hsl
import objects.rgb


def project_into_range(value):
    if value < 0:
        return value + 1
    elif value > 1:
        return value - 1
    else:
        return value


def probe_variable(value, temporary_1, temporary_2):
    if value * 6 < 1:
        return temporary_2 + (temporary_1 - temporary_2)
    elif value * 2 < 1:
        return temporary_1
    elif value * 3 < 2:
        return temporary_2 + (temporary_1 - temporary_2) * (0.666 - value) * 6
    else:
        return temporary_2


def project_onto_circle(value):
    if value < 0:
        return value + 360
    return value


def hsl_to_rgb(value: objects.hsl.HSL) -> objects.rgb.RGB:
    if value.saturation == 0:
        return objects.rgb.RGB(
            value.luminance * objects.rgb.RGB.MAX,
            value.luminance * objects.rgb.RGB.MAX,
            value.luminance * objects.rgb.RGB.MAX,
        )
    temporary_1 = value.luminance * (1.0 + value.saturation)
    if value.luminance >= 0.5:
        temporary_1 = (
            value.luminance + value.saturation - value.luminance * value.saturation
        )
    temporary_2 = 2 * value.luminance - temporary_1
    temporary_hue = value.hue / 360
    temporary_R = project_into_range(temporary_hue + 0.333)
    temporary_G = project_into_range(temporary_hue)
    temporary_B = project_into_range(temporary_hue - 0.333)
    return objects.rgb.RGB(
        probe_variable(temporary_R, temporary_1, temporary_2) * objects.rgb.RGB.MAX,
        probe_variable(temporary_G, temporary_1, temporary_2) * objects.rgb.RGB.MAX,
        probe_variable(temporary_B, temporary_1, temporary_2) * objects.rgb.RGB.MAX,
    )


def rgb_to_hsl(value: objects.rgb.RGB) -> objects.hsl.HSL:
    rgb_percent = value / objects.rgb.RGB(
        objects.rgb.RGB.MAX,
        objects.rgb.RGB.MAX,
        objects.rgb.RGB.MAX,
    )
    rgb_sorted = sorted(rgb_percent.as_vector())
    max = rgb_sorted[2]
    min = rgb_sorted[0]
    luminance = (max + min) / 2
    saturation = 0
    if min != max:
        if luminance <= 0.5:
            saturation = (max - min) / (max + min)
        else:
            saturation = (max - min) / (2.0 - max - min)
    if rgb_percent.red == max:
        hue = (rgb_percent.green - rgb_percent.blue) / (max - min)
    elif rgb_percent.green == max:
        hue = 2.0 + (rgb_percent.blue - rgb_percent.red) / (max - min)
    else:
        hue = 4.0 + (rgb_percent.red - rgb_percent.green) / (max - min)

    return objects.hsl.HSL(
        hue=project_onto_circle(hue * 60),
        saturation=saturation,
        luminance=luminance,
    )


def hsv_to_rgb(hue, sat, val):
    if hue >= 65536:
        hue %= 65536

    hue = (hue * 1530 + 32768) // 65536
    if hue < 510:
        b = 0
        if hue < 255:
            r = 255
            g = hue
        else:
            r = 510 - hue
            g = 255
    elif hue < 1020:
        r = 0
        if hue < 765:
            g = 255
            b = hue - 510
        else:
            g = 1020 - hue
            b = 255
    elif hue < 1530:
        g = 0
        if hue < 1275:
            r = hue - 1020
            b = 255
        else:
            r = 255
            b = 1530 - hue
    else:
        r = 255
        g = 0
        b = 0

    v1 = 1 + val
    s1 = 1 + sat
    s2 = 255 - sat

    r = ((((r * s1) >> 8) + s2) * v1) >> 8
    g = ((((g * s1) >> 8) + s2) * v1) >> 8
    b = ((((b * s1) >> 8) + s2) * v1) >> 8

    return r, g, b


def rgb_to_hsv():
    pass


"""

void RGBtoHSV( float r, float g, float b, float *h, float *s, float *v) {
   float min, max, delta;
   min = MIN( r, g, b );
   max = MAX( r, g, b );
   *v = max;                        // v
   delta = max - min;
   if( max != 0 ) *s = delta / max;
   else {                           // r = g = b = 0
      *s = 0; *h = -1; return;
   }
   if (max == min) {                // hier ist alles Grau
      *h = 0; *s = 0; return;
   }
   if( r == max )
      *h = ( g - b ) / delta;       // zwischen Gelb und Magenta
   else if( g == max )
      *h = 2 + ( b - r ) / delta;   // zwischen Cyan und Gelb
   else
      *h = 4 + ( r - g ) / delta;   // zwischen Magenta und Zyan
      *h *= 60;                     // degrees
   if( *h < 0 )
      *h += 360;
}

void HSVtoRGB( float *r, float *g, float *b, float h, float s, float v) {
   int i;
   float f, p, q, t;
   if( s == 0 ) { // achromatisch (Grau)
      *r = *g = *b = v;
      return;
   }
   h /= 60;           // sector 0 to 5
   i = floor( h );
   f = h - i;         // factorial part of h
   p = v * ( 1 - s );
   q = v * ( 1 - s * f );
   t = v * ( 1 - s * ( 1 - f ) );
   switch( i ) {
      case 0: *r = v; *g = t; *b = p; break;
      case 1: *r = q; *g = v; *b = p; break;
      case 2: *r = p; *g = v; *b = t; break;
      case 3: *r = p; *g = q; *b = v; break;
      case 4: *r = t; *g = p; *b = v; break;
      default:  // case 5:
         *r = v; *g = p; *b = q; break;
   }
}
"""
