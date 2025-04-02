install:
    uv sync

test_updaters:
    uv run .github/scripts/update_libraries.py
    uv run .github/scripts/update_repo_data.py

sass:
    gulp sass

