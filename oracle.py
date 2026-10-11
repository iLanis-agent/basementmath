#!/usr/bin/env python3
"""Python mirror of engine.js - regenerates expected.json. Exact float-for-float mirror."""
import json, math, os

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100
def jsnum(x):
    if isinstance(x, float) and x == int(x): return int(x)
    return x
def fmt(x): return repr(jsnum(x))
def pos(nums, msg):
    for n in nums:
        if not (n > 0) or n != n or n == float('inf'): return {"error": msg}
    return None

def dampPlan(roomM2, ceilingM, loadPerM3):
    bad = pos([roomM2, ceilingM, loadPerM3], "area, ceiling and moisture load must be positive")
    if bad: return bad
    volume = roomM2 * ceilingM
    liters = volume * loadPerM3
    return {"volumeM3": jsnum(r1(volume)), "litersDay": jsnum(r2(liters))}

def tankPlan(tankL, litersDay):
    bad = pos([tankL, litersDay], "tank size and daily liters must be positive")
    if bad: return bad
    hours = r1(tankL / (litersDay / 24))
    empties = r2(litersDay / tankL)
    return {"hours": jsnum(hours), "empties": jsnum(empties)}

def costPlan(watts, hoursDay, tariff):
    bad = pos([watts, hoursDay, tariff], "power, hours and tariff must be positive")
    if bad: return bad
    kwh = watts * hoursDay * 365 / 1000
    return {"kwhYear": jsnum(r1(kwh)), "costYear": jsnum(r2(kwh * tariff))}

def plural(n, w): return fmt(n) + " " + w + ("" if n == 1 else "s")

def renderDamp(r, roomM2, ceilingM, loadPerM3):
    return "A " + fmt(roomM2) + " m² basement at " + fmt(ceilingM) + " m is " + fmt(r["volumeM3"]) + " m³ - at a labeled " + fmt(loadPerM3) + " liters per cubic meter a day, about " + fmt(r["litersDay"]) + " liters to pull out daily."

def renderTank(r, tankL, litersDay):
    return "A " + fmt(tankL) + " L tank at " + fmt(litersDay) + " liters a day fills in about " + plural(r["hours"], "hour") + " - about " + fmt(r["empties"]) + (" empty" if r["empties"] == 1 else " empties") + " a day."

def renderCost(r, watts, hoursDay, tariff):
    return "Running " + fmt(watts) + " W for " + plural(hoursDay, "hour") + " a day is " + fmt(r["kwhYear"]) + " kWh a year - about " + fmt(r["costYear"]) + " at your labeled " + fmt(tariff) + " per kWh tariff."

cases = []
damp_args = [(40,2.2,0.05),(30,2.2,0.05),(50,2.4,0.06),(35,2.1,0.04),(60,2.5,0.05),
             (25,2,0.05),(45,2.3,0.055),(55,2.2,0.05),(38,2.2,0.045),(48,2.6,0.05),
             (32,2.1,0.05),(42,2.2,0.06),(0,2.2,0.05),(40,0,0.05),(40,2.2,0)]
for a in damp_args:
    r = dampPlan(*a)
    case = {"fn": "dampPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderDamp(r, a[0], a[1], a[2])
    cases.append(case)
tank_args = [(4,4.4),(5,6),(3,3.5),(6,8.8),(4,2.2),(8,10),(2,1.5),(5,4.8),
             (4,24),(10,5),(3.5,4.2),(7,7.5),(0,4.4),(4,0)]
for a in tank_args:
    r = tankPlan(*a)
    case = {"fn": "tankPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderTank(r, a[0], a[1])
    cases.append(case)
cost_args = [(300,12,0.15),(400,24,0.15),(250,8,0.2),(350,12,0.12),(500,16,0.18),
             (200,6,0.15),(450,10,0.25),(300,1,0.15),(600,20,0.1),(275,14,0.16),
             (320,18,0.14),(380,9,0.22),(0,12,0.15),(300,0,0.15),(300,12,0)]
for a in cost_args:
    r = costPlan(*a)
    case = {"fn": "costPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderCost(r, a[0], a[1], a[2])
    cases.append(case)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected.json")
with open(out, "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(cases), "cases")
