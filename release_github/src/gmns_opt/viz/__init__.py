"""Visualization / explanation layer. GUI4GMNS is the intended rich front end; this module ships a
dependency-light GeoJSON export so any web map (kepler.gl, GUI4GMNS, Leaflet) can render link solutions."""
from .export import export_geojson

__all__ = ["export_geojson"]
