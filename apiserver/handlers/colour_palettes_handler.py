from typing import Optional

import ure
from apiserver.handlers.base_handler import BaseHandler
from apiserver.handlers.colour_palette_handler import ColourPaletteHandler
from apiserver.response import Response
from driver.colour_palettes import ColourPalettes
from errors import EXCEPTION_ERROR
from webserver.http import Request


class ColourPalettesHandler(BaseHandler):
    paths = ["/palettes", "/palettes/"]
    path_regex = ure.compile("/palettes/(\d+)(/.+$)?")
    colour_palette_handler = ColourPaletteHandler()

    def __init__(self, colour_palettes: ColourPalettes) -> None:
        self.colour_palettes = colour_palettes

    def get_palettes(self, palette=None):
        if palette is None:
            return Response.from_dict(self.colour_palettes.as_dict(), 200)
        return None

    def router(self, request: Request) -> Optional[Response]:
        if request.path in self.paths:
            if "GET" == request.method:
                return self.get_palettes()
        elif match := self.path_regex.match(request.path):
            palette = int(match.group(1))
            if match.group(2):
                self.colour_palette_handler.colour_palette = self.colour_palettes[
                    palette
                ]
                request.path = match.group(2)
                return self.colour_palette_handler.router(request)
            elif match.group(1):
                try:
                    if "GET" == request.method:
                        return self.get_palettes(palette=palette)
                except AssertionError as e:
                    return Response.from_dict(*EXCEPTION_ERROR(e))
        return None
