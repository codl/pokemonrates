.PHONY: lock

lock: requirements.txt dev-requirements.txt ci-requirements.txt

requirements.txt: requirements.in constraints.txt
	uv pip compile --generate-hashes -o requirements.txt requirements.in

dev-requirements.txt: dev-requirements.in requirements.txt constraints.txt
	uv pip compile --generate-hashes -o dev-requirements.txt dev-requirements.in

ci-requirements.txt: ci-requirements.in requirements.txt dev-requirements.txt constraints.txt
	uv pip compile --generate-hashes -o ci-requirements.txt ci-requirements.in


