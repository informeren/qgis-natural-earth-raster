"""Plugin entry point."""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Natural Earth Raster class from file natural_earth_raster."""
    from .natural_earth_raster import NaturalEarthRaster
    return NaturalEarthRaster(iface)
