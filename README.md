# Basement math

How much moisture a damp basement really holds, how often the tank fills, and what the humming dehumidifier costs a year. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/basementmath/

## The three tools

- **Damp plan** - `dampPlan(roomM2, ceilingM, loadPerM3)`: cubic meters and liters a day.
- **Tank plan** - `tankPlan(tankL, litersDay)`: hours between empties and empties a day.
- **Cost plan** - `costPlan(watts, hoursDay, tariff)`: kWh and cost per year.

## Labeled norms (illustrative references, not rules)

- Moisture load: 0.05 liters per cubic meter a day for a damp basement. Ceiling: 2.2 m. Tank: 4 L.
- Unit: 300 W, 12 hours a day. Tariff: 0.15 per kWh. Your basement, unit and weather decide the real numbers.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (44 cases, 116 checks)

Regenerate the oracle expectations: `python3 oracle.py`
