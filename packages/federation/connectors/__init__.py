"""Space provider connectors for European Space Federation."""

from packages.federation.connectors.cdse import CDSEConnector
from packages.federation.connectors.esa import ESAConnector
from packages.federation.connectors.eumetsat import EUMETSATConnector
from packages.federation.connectors.destine import DestinEConnector
from packages.federation.connectors.gnss import GalileoConnector, EGNOSConnector
from packages.federation.connectors.space_weather import SpaceWeatherConnector
from packages.federation.connectors.ssa import SSAConnector

__all__ = [
    "CDSEConnector",
    "ESAConnector",
    "EUMETSATConnector",
    "DestinEConnector",
    "GalileoConnector",
    "EGNOSConnector",
    "SpaceWeatherConnector",
    "SSAConnector",
]
