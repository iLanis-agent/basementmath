// Basement math - pure arithmetic engine, runs in browser and node.
(function(root){
"use strict";
function r1(x){ return Math.round(x*10)/10; }
function r2(x){ return Math.round(x*100)/100; }
function pos(nums, msg){
  for (var i=0;i<nums.length;i++){ if (!isFinite(nums[i]) || nums[i] <= 0) return { error: msg }; }
  return null;
}
function dampPlan(roomM2, ceilingM, loadPerM3){
  var bad = pos([roomM2, ceilingM, loadPerM3], "area, ceiling and moisture load must be positive");
  if (bad) return bad;
  var volume = roomM2 * ceilingM;
  var liters = volume * loadPerM3;
  return { volumeM3: r1(volume), litersDay: r2(liters) };
}
function tankPlan(tankL, litersDay){
  var bad = pos([tankL, litersDay], "tank size and daily liters must be positive");
  if (bad) return bad;
  var hours = r1(tankL / (litersDay / 24));
  var empties = r2(litersDay / tankL);
  return { hours: hours, empties: empties };
}
function costPlan(watts, hoursDay, tariff){
  var bad = pos([watts, hoursDay, tariff], "power, hours and tariff must be positive");
  if (bad) return bad;
  var kwh = watts * hoursDay * 365 / 1000;
  return { kwhYear: r1(kwh), costYear: r2(kwh * tariff) };
}
function plural(n, w){ return n + " " + w + (n === 1 ? "" : "s"); }
function renderDamp(r, roomM2, ceilingM, loadPerM3){
  return "A " + roomM2 + " m² basement at " + ceilingM + " m is " + r.volumeM3 + " m³ - at a labeled " + loadPerM3 + " liters per cubic meter a day, about " + r.litersDay + " liters to pull out daily.";
}
function renderTank(r, tankL, litersDay){
  return "A " + tankL + " L tank at " + litersDay + " liters a day fills in about " + plural(r.hours, "hour") + " - about " + r.empties + (r.empties === 1 ? " empty" : " empties") + " a day.";
}
function renderCost(r, watts, hoursDay, tariff){
  return "Running " + watts + " W for " + plural(hoursDay, "hour") + " a day is " + r.kwhYear + " kWh a year - about " + r.costYear + " at your labeled " + tariff + " per kWh tariff.";
}
var api = { dampPlan: dampPlan, tankPlan: tankPlan, costPlan: costPlan,
  renderDamp: renderDamp, renderTank: renderTank, renderCost: renderCost };
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.BasementMath = api;
})(typeof window !== "undefined" ? window : globalThis);
