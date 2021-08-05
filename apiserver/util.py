import apiserver.objects.hsl
import apiserver.objects.rgb


def exception_error(e: Exception):
    return ({"error": "{}".format(e)}, 400)


def code_to_message(code):
    if code == 100:
        return "Continue"
    if code == 101:
        return "Switching Protocols"
    if code == 200:
        return "OK"
    if code == 201:
        return "Created"
    if code == 202:
        return "Accepted"
    if code == 203:
        return "Non-Authoritative Information"
    if code == 204:
        return "No Content"
    if code == 205:
        return "Reset Content"
    if code == 300:
        return "Multiple Choices"
    if code == 301:
        return "Moved Permanently"
    if code == 302:
        return "Found"
    if code == 303:
        return "See Other"
    if code == 305:
        return "Use Proxy"
    if code == 306:
        return "(Unused)"
    if code == 307:
        return "Temporary Redirect"
    if code == 308:
        return "Permanent Redirect"
    if code == 400:
        return "Bad Request"
    if code == 401:
        return "Unauthorized"
    if code == 402:
        return "Payment Required"
    if code == 403:
        return "Forbidden"
    if code == 404:
        return "Not Found"
    if code == 405:
        return "Method Not Allowed"
    if code == 406:
        return "Not Acceptable"
    if code == 408:
        return "Request Timeout"
    if code == 409:
        return "Conflict"
    if code == 410:
        return "Gone"
    if code == 411:
        return "Length Required"
    if code == 413:
        return "Payload Too Large"
    if code == 414:
        return "URI Too Long"
    if code == 415:
        return "Unsupported Media Type"
    if code == 417:
        return "Expectation Failed"
    if code == 426:
        return "Upgrade Required"
    if code == 500:
        return "Internal Server Error"
    if code == 501:
        return "Not Implemented"
    if code == 502:
        return "Bad Gateway"
    if code == 503:
        return "Service Unavailable"
    if code == 504:
        return "Gateway Timeout"
    if code == 505:
        return "HTTP Version Not Supported"


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


def hsl_to_rgb(value: apiserver.objects.hsl.HSL) -> apiserver.objects.rgb.RGB:
    if value.saturation == 0:
        return apiserver.objects.rgb.RGB(
            value.luminance * apiserver.objects.rgb.RGB.MAX,
            value.luminance * apiserver.objects.rgb.RGB.MAX,
            value.luminance * apiserver.objects.rgb.RGB.MAX,
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
    return apiserver.objects.rgb.RGB(
        probe_variable(temporary_R, temporary_1, temporary_2)
        * apiserver.objects.rgb.RGB.MAX,
        probe_variable(temporary_G, temporary_1, temporary_2)
        * apiserver.objects.rgb.RGB.MAX,
        probe_variable(temporary_B, temporary_1, temporary_2)
        * apiserver.objects.rgb.RGB.MAX,
    )


def rgb_to_hsl(value: apiserver.objects.rgb.RGB) -> apiserver.objects.hsl.HSL:
    rgb_percent = value / apiserver.objects.rgb.RGB(
        apiserver.objects.rgb.RGB.MAX,
        apiserver.objects.rgb.RGB.MAX,
        apiserver.objects.rgb.RGB.MAX,
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

    return apiserver.objects.hsl.HSL(
        hue=project_onto_circle(hue * 60),
        saturation=saturation,
        luminance=luminance,
    )
