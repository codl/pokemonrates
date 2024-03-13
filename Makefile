.PHONY: lock

lock: requirements.txt dev-requirements.txt ci-requirements.txt

requirements.txt: requirements.in constraints.txt
	pip-compile --allow-unsafe --generate-hashes --resolver backtracking --strip-extras

dev-requirements.txt: dev-requirements.in requirements.txt constraints.txt
	pip-compile --allow-unsafe --generate-hashes --resolver backtracking --strip-extras dev-requirements.in

ci-requirements.txt: ci-requirements.in requirements.txt dev-requirements.txt constraints.txt
	pip-compile --allow-unsafe --generate-hashes --resolver backtracking --strip-extras ci-requirements.in


