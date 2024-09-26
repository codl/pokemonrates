.PHONY: lock

lock: uv.lock

uv.lock: pyproject.toml
	uv lock
