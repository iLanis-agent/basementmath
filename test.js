const E = require('./engine.js');
const cases = require('./expected.json');
const fns = { dampPlan: E.dampPlan, tankPlan: E.tankPlan, costPlan: E.costPlan };
const renders = {
  dampPlan: (r, a) => E.renderDamp(r, a[0], a[1], a[2]),
  tankPlan: (r, a) => E.renderTank(r, a[0], a[1]),
  costPlan: (r, a) => E.renderCost(r, a[0], a[1], a[2])
};
let checks = 0, failed = 0;
for (const c of cases) {
  const got = fns[c.fn](...c.args);
  for (const k of Object.keys(c.result)) {
    checks++;
    if (got[k] !== c.result[k]) { failed++; console.log('FAIL', c.fn, c.args, k, 'expected', c.result[k], 'got', got[k]); }
  }
  if (c.render !== undefined) {
    checks++;
    const g = renders[c.fn](got, c.args);
    if (g !== c.render) { failed++; console.log('FAIL render', c.fn, c.args, '\n exp:', c.render, '\n got:', g); }
  }
}
console.log(cases.length + ' cases, ' + checks + ' checks ' + (failed ? failed + ' FAILED' : 'green'));
process.exit(failed ? 1 : 0);
