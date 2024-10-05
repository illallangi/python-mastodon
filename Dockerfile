# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ARG VERSION=0.0.dev1

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
ADD pyproject.toml pyproject.toml
ADD uv.lock uv.lock
RUN uv sync --frozen --no-install-project --no-dev && \
    rm -rf ~/.cache

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN uv sync --frozen --no-dev && \
    rm -rf ~/.cache


# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Set the entrypoint to the `mastodon-tools` command
ENTRYPOINT ["mastodon-tools"]

# Run the `mastodon-tools` command by default
CMD ["--help"]
