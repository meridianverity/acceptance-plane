.PHONY: vectors eval transparency receipt independent manifest schema test qa qa-full release-gate clean

vectors:
	python tools/build_vectors.py

eval: vectors
	python tools/run_public_eval.py --write-results receipts/public_eval_results.json

transparency: eval
	python tools/generate_transparency_bundle.py
	python tools/verify_transparency_bundle.py

receipt: transparency
	python tools/generate_proof_receipt.py
	python tools/verify_proof_receipt.py --verify-manifest

independent: receipt
	python tools/independent_recompute.py

manifest:
	python scripts/verify_manifest.py

schema:
	python tools/validate_schema_examples.py

test:
	python -m pytest -q

release-gate:
	python tools/release_gate.py

qa: manifest eval transparency receipt independent schema test

qa-full:
	python scripts/verify_manifest.py
	python tools/run_public_eval.py
	python tools/verify_transparency_bundle.py
	python tools/verify_proof_receipt.py --verify-manifest
	python tools/independent_recompute.py
	python tools/validate_schema_examples.py
	AP_RELEASE_GATE_ASSUME_QA=1 python tools/release_gate.py
	python tools/verify_release_artifact.py --tree .

clean:
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	find . -name '*.pyc' -delete
	rm -rf .pytest_cache build *.egg-info
