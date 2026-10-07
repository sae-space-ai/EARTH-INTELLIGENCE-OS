"""European Space Federation package — provider-neutral federation layer."""

from packages.federation.models import (
    AccessPolicy,
    ProviderCapability,
    SpaceDataProvider,
    ExternalMission,
    ExternalSpacecraft,
    ExternalInstrument,
    ExternalCollection,
    ExternalSpaceService,
    ExternalObservationCandidate,
    SpaceEnvironmentObservation,
    CatalogSyncRun,
)
from packages.federation.registry import ProviderRegistry, ConnectorRegistry
from packages.federation.resolver import SpaceCapabilityResolver

__all__ = [
    "AccessPolicy",
    "ProviderCapability",
    "SpaceDataProvider",
    "ExternalMission",
    "ExternalSpacecraft",
    "ExternalInstrument",
    "ExternalCollection",
    "ExternalSpaceService",
    "ExternalObservationCandidate",
    "SpaceEnvironmentObservation",
    "CatalogSyncRun",
    "ProviderRegistry",
    "ConnectorRegistry",
    "SpaceCapabilityResolver",
]
