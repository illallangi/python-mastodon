.PHONY: usage
usage:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  clean       Remove all generated files"
	@echo "  ruff        Run ruff format and check"
	@echo "  build       Build the project"
	@echo "  statuses    Run mastodon-tool statuses"
	@echo "  swimmers    Run mastodon-tool swims"
	@echo

.PHONY: clean
clean:
	@git clean -Xdf

.PHONY: ruff
ruff:
	@uv run --quiet ruff format src
	@uv run --quiet ruff check src

.PHONY: sync
sync: ruff
	@uv sync --quiet

.PHONY: commit
commit: sync
	@uv run --quiet cz commit

# Shortcuts to run the mastodon-tools command

.PHONY: help
help: sync
	@uv run --quiet mastodon-tools --help

.PHONY: version
version: sync
	@uv run --quiet mastodon-tools --version

.PHONY: statuses
statuses: sync
	@uv run --quiet mastodon-tools statuses

.PHONY: statuses.json
statuses.json: sync
	@uv run --quiet mastodon-tools statuses --json | jq > $@

.PHONY: swims
swims: sync
	@uv run --quiet mastodon-tools swims

.PHONY: swims.json
swims.json: sync
	@uv run --quiet mastodon-tools swims --json | jq > $@

# PyPi package build and upload

.PHONY: build
build: sync
	@uv build

.PHONY: test-upload
test-upload: build
	@UV_PUBLISH_URL=https://test.pypi.org/legacy/ uv publish
