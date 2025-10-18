# Team Python: Microservice boilerplate

## Project setup

### Prerequisites

- uv (https://docs.astral.sh/uv/)

### Steps

- clone repo
- `uv sync --group code-quality`
- `uv run pre-commit run --all-files`
- `make build`
- `docker-compose up`
