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
        probe_variable(temporary_R, temporary_1, temporary_2)
        * objects.rgb.RGB.MAX,
        probe_variable(temporary_G, temporary_1, temporary_2)
        * objects.rgb.RGB.MAX,
        probe_variable(temporary_B, temporary_1, temporary_2)
        * objects.rgb.RGB.MAX,
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
