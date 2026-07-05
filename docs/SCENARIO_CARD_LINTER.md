# Scenario Card Linter

The README promises a 5-minute scenario-card linter. This overlay makes that claim runnable.

Try an accepted action:

```bash
python tools/lint_scenario_card.py examples/scenario_cards/deploy_accept.json
```

Try a fail-closed hold:

```bash
python tools/lint_scenario_card.py examples/scenario_cards/hold_approval_required.json
```

Try a refusal:

```bash
python tools/lint_scenario_card.py examples/scenario_cards/refuse_revoked.json
```

The linter checks basic scenario-card completeness and evaluates the card through the public-eval profile.
