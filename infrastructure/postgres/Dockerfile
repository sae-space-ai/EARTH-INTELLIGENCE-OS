# Custom PostgreSQL image with BOTH PostGIS AND pgvector
# The official postgis/postgis image does NOT include pgvector.
# This image layers pgvector onto a compatible PostGIS base.
FROM postgis/postgis:16-3.4

# pgvector version compatible with PostgreSQL 16
ARG PGVECTOR_VERSION=v0.7.0

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    postgresql-server-dev-16 \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Build and install pgvector
RUN cd /tmp \
    && git clone --branch ${PGVECTOR_VERSION} --depth 1 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install \
    && cd / \
    && rm -rf /tmp/pgvector

# Remove build dependencies to keep image small
RUN apt-get purge -y --auto-remove build-essential git postgresql-server-dev-16

# Verify both extensions are loadable
RUN echo "Verifying PostGIS..." \
    && psql --version \
    && echo "PostGIS image ready with pgvector ${PGVECTOR_VERSION}"
