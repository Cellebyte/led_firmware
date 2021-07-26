import apiserver.util
import apiserver.objects.rgb


class HSL:
    def __init__(self, hue, saturation, luminance):
        self.hue = hue
        self.saturation = saturation
        self.luminance = luminance

    def as_rgb(self) -> apiserver.objects.rgb.RGB:
        return apiserver.util.hsl_to_rgb(self)

    def from_rgb(self, value: apiserver.objects.rgb.RGB) -> "HSL":
        hsl = apiserver.util.rgb_to_hsl(value)
        self.hue = hsl.hue
        self.saturation = hsl.saturation
        self.luminance = hsl.luminance

    def as_dict(self) -> dict:
        return {
            'hue': self.hue,
            'saturation': self.saturation,
            'luminance': self.luminance
        }
