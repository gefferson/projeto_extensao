#
# The Python Imaging Library
# $Id$
#
# GRIB stub adapter
#
# Copyright (c) 1996-2003 by Fredrik Lundh
#
# See the README file for information on usage and redistribution.
#

from PIL import Image, ImageFile

_handler = None

##
# Install application-specific GRIB image handler.
#
# @param handler Handler object.

def register_handler(handler):
    global _handler
    _handler = handler

# --------------------------------------------------------------------
# Image adapter

def _accept(prefix):
    return prefix[0:4] == "GRIB" and prefix[7] == chr(1)

class GribStubImageFile(ImageFile.StubImageFile):

    format = "GRIB"
    format_description = "GRIB"

    def _open(self):

        offset = self.fp.tell()

        if not _accept(self.fp.read(8)):
            raise SyntaxError("Not a GRIB file")

        self.fp.seek(offset)

        # make something up
        self.mode = "F"
        self.size = 1, 1

        loader = self._load()
        if loader:
            loader.open(self)

    def _load(self):
        return _handler

def _save(im, fp, filename):
    if _handler is None or not hasattr("_handler", "save"):
        raise IOError("GRIB save handler not installed")
    _handler.save(im, fp, filename)


# --------------------------------------------------------------------
# Registry

Image.register_open(GribStubImageFile.format, GribStubImageFile, _accept)
Image.register_save(GribStubImageFile.format, _save)

Image.register_extension(GribStubImageFile.format, ".grib")
