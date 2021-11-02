.PHONY: fix

fix:
	poetry run black python_compiles_lisp tests
	poetry run isort python_compiles_lisp tests
