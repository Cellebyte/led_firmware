import json
from typing import Optional

import ure
from apiserver.handlers.base_handler import BaseHandler
from apiserver.response import Response
from driver.colour_palette import ColourPalette
from errors import EXCEPTION_ERROR
from objects.rgb import RGB
from webserver.http import Request


class ColourPaletteHandler(BaseHandler):
    paths = ["/colours", "/colours/"]
    path_regex = ure.compile("/colours/(\d+)/?")

    @property
    def colour_palette(self) -> ColourPalette:
        return self._colour_palette

    @colour_palette.setter
    def colour_palette(self, value: ColourPalette):
        assert isinstance(value, ColourPalette)
        self._colour_palette = value

    def get_colours(self, slot=None) -> Optional[Response]:
        if slot is None:
            return Response.from_dict(self.colour_palette.as_dict(), 200)
        else:
            colour = self.colour_palette[slot]
            if colour is not None:
                return Response.from_dict(colour.as_dict() if colour else colour, 200)
            return None

    def post_colours(self, body, slot=None):
        colour = RGB.from_dict(json.loads(body))
        if slot is None:
            free_slot = None
            for key in self.colour_palette:
                if self.colour_palette[key] is None:
                    free_slot = key
                    break
            assert (
                free_slot is not None
            ), "The colour Store is full please define a slot to overwrite"
            self.colour_palette[free_slot] = colour
            return Response.from_dict({free_slot: colour.as_dict()}, 201)
        else:
            self.colour_palette[slot] = colour
        return Response.from_dict(colour.as_dict(), 201)
        
        

    def delete_colours(self, slot=None):
        if slot is not None:
            colour = self.colour_palette.delete(slot)
            if colour is not None:
                return Response.from_dict(colour.as_dict(), 200)
            return None
        else:
            return Response.from_dict(
                {
                    slot: self.colour_palette.delete(slot)
                    for slot in self.colour_palette
                    if self.colour_palette[slot]
                },
                200,
            )

    def router(self, request: Request) -> Optional[Response]:
        if request.path in self.paths:
            if "GET" == request.method:
                return self.get_colours()
            elif "POST" == request.method:
                return self.post_colours(request.body)
            elif "DELETE" == request.method:
                return self.delete_colours()
        elif match := self.path_regex.match(request.path):
            try:
                slot = int(match.group(1))
                if "GET" == request.method:
                    return self.get_colours(slot=slot)
                elif "POST" == request.method:
                    return self.post_colours(request.body, slot=slot)
                elif "DELETE" == request.method:
                    return self.delete_colours(slot=slot)
            except AssertionError as e:
                return Response.from_dict(*EXCEPTION_ERROR(e))
        return None
