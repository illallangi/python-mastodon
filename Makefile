.PHONY: usage
usage:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  clean       Remove all generated files"
	@echo "  lint        Run ruff format, check and uv sync"
	@echo "  commit      Run cz commit"
	@echo "  build       Build the project"
	@echo
	@echo "  help        Run mastodon-tools help"
	@echo "  version     Run mastodon-tools version"
	@echo "  statuses    Run mastodon-tools statuses"
	@echo "  swims       Run mastodon-tools swims"
	@echo

.PHONY: clean
clean:
	@git clean -Xdf
	@mkdir -p .git/hooks
	@rm -f .git/hooks/*.sample
	@find .git/hooks/ -type f  | while read i; do chmod +x $$i; done

.PHONY: lint
lint:
	@uv run --quiet ruff format src
	@uv run --quiet ruff check src
	@uv sync --quiet

.PHONY: commit
commit: lint
	@uv run --quiet cz commit

.PHONY: build
build: lint
	@uv build


.PHONY: help
help: lint
	@uv run --quiet mastodon-tools --help

.PHONY: version
version: lint
	@uv run --quiet mastodon-tools --version

.PHONY: statuses
statuses: lint
	@uv run --quiet mastodon-tools statuses

.PHONY: statuses.json
statuses.json: lint
	@uv run --quiet mastodon-tools statuses --json | jq > $@

.PHONY: swims
swims: lint
	@uv run --quiet mastodon-tools swims

.PHONY: swims.json
swims.json: lint
	@uv run --quiet mastodon-tools swims --json | jq > $@
