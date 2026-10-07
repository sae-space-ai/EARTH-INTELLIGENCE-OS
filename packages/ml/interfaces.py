"""ML interfaces — future foundation model contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class LatentRepresentation(BaseModel):
    """Embedding/latent vector from foundation model.

    Target dimensionality: 256 (configurable per model).
    """

    embedding: list[float] = Field(min_length=1)
    embedding_dim: int = Field(ge=1)
    model_version_id: UUID
    modalities: list[str] = Field(default_factory=list)
    quality_metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __init__(self, **data: Any) -> None:
        """Validate embedding dimension matches declared dim."""
        super().__init__(**data)
        if len(self.embedding) != self.embedding_dim:
            raise ValueError(
                f"Embedding length {len(self.embedding)} != declared dim {self.embedding_dim}"
            )


# Future interface contracts (not yet implemented)
# These define the API surface for Phase 3+ foundation model integration.

async def encode(observation_id: UUID, model_version_id: UUID) -> LatentRepresentation:
    """Generate embedding from observation using specified model.

    Args:
        observation_id: Source observation.
        model_version_id: Model version to use.

    Returns:
        Latent representation.

    Note:
        Not implemented in Phase 0. Interface defined for Phase 3.
    """
    raise NotImplementedError("Foundation model encoding available in Phase 3+")


async def analyze(embeddings: list[LatentRepresentation]) -> dict[str, Any]:
    """Run analysis on set of embeddings.

    Args:
        embeddings: Input embeddings.

    Returns:
        Analysis results.

    Note:
        Not implemented in Phase 0. Interface defined for Phase 3+.
    """
    raise NotImplementedError("Foundation model analysis available in Phase 3+")
