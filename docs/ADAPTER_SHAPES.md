# Adapter Shapes

The hardened package includes shape-only adapter sketches for common enforcement surfaces:

- `adapters/opa/acceptance_policy.rego`
- `adapters/envoy/ext_authz_response_shape.json`
- `adapters/kubernetes/validating_admission_policy.yaml`

These are not product implementations. They show how an Acceptance Plane decision can be projected into policy-as-code, service mesh authorization, and admission control surfaces.

The runnable evaluator remains `tools/run_public_eval.py`.
