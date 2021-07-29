import apiserver.util
import apiserver.objects.rgb


class HSL:
    def __init__(self, hue, saturation, luminance):
        self.hue = hue
        self.saturation = saturation
        self.luminance = luminance

    def as_rgb(self) -> apiserver.objects.rgb.RGB:
        return apiserver.util.hsl_to_rgb(self)

    def as_dict(self) -> dict:
        return {
            "hue": self.hue,
            "saturation": self.saturation,
            "luminance": self.luminance,
        }

    def __repr__(self) -> str:
        return "HSL({},{},{})".format(self.hue, self.saturation, self.luminance)
