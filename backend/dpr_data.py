"""
Shared demo data for the Raipur–Durg New Railway Line (Route B — AI Optimized).
Used by the API, the PDF/Excel/KML generators so everything stays consistent.
"""

PROJECT = {
    "name": "Raipur - Durg New Railway Line",
    "route": "Route B — AI Optimized",
    "zone": "South East Central Railway",
    "prepared_by": "RailPlan AI Platform",
    "distance_km": 71.8,
    "total_cost_cr": 1298,
    "gauge": "Broad Gauge (1676 mm)",
    "electrified": "Yes (25 kV AC)",
}

# Cost split (₹ Crores)
COST_SPLIT = [
    {"head": "Track & Earthwork",       "amount": 387, "pct": 29.8, "color": "#003087"},
    {"head": "Bridges & Structures",    "amount": 234, "pct": 18.0, "color": "#FF6B00"},
    {"head": "Land Acquisition",        "amount": 312, "pct": 24.0, "color": "#10b981"},
    {"head": "Electrification",         "amount": 187, "pct": 14.4, "color": "#8b5cf6"},
    {"head": "Signalling & Telecom",    "amount": 98,  "pct": 7.5,  "color": "#0ea5e9"},
    {"head": "Miscellaneous",           "amount": 80,  "pct": 6.3,  "color": "#64748b"},
]

ROUTE_COSTS = [
    {"id": "A", "name": "Shortest Path", "cost": 1456, "color": "#2196F3"},
    {"id": "B", "name": "AI Optimized",  "cost": 1298, "color": "#4CAF50"},
    {"id": "C", "name": "Eco-Friendly",  "cost": 1512, "color": "#FF9800"},
]

# Bill of Quantities (Indian Railways standard items)
BOQ = [
    ("1",  "Site clearance and grubbing",                         "Sqm",   "4,28,000", 18,        "0.77"),
    ("2",  "Earthwork in embankment formation",                   "Cum",   "18,60,000", 285,      "53.01"),
    ("3",  "Earthwork in cutting (soil)",                         "Cum",   "9,40,000",  240,      "22.56"),
    ("4",  "Blanketing material (sub-ballast)",                   "Cum",   "2,15,000",  1150,     "24.73"),
    ("5",  "Supply & spreading of ballast (machine crushed)",     "Cum",   "1,72,000",  1980,     "34.06"),
    ("6",  "PSC sleepers (broad gauge)",                          "Nos",   "1,19,000",  2850,     "33.92"),
    ("7",  "60 kg/m, 90 UTS rails",                               "MT",    "9,800",     68000,    "66.64"),
    ("8",  "Laying & linking of track (LWR)",                     "Km",    "143",       42_50_000,"60.78"),
    ("9",  "Major bridges (5 nos, RCC/PSC girders)",              "Nos",   "5",         18_60_00000,"93.00"),
    ("10", "Minor bridges & culverts (9 nos)",                    "Nos",   "9",         3_20_00000, "28.80"),
    ("11", "Road over / under bridges (4 nos)",                   "Nos",   "4",         6_75_00000, "27.00"),
    ("12", "Station buildings (4 stations)",                      "Nos",   "4",         8_50_00000, "34.00"),
    ("13", "Platforms, FOB & passenger amenities",               "LS",    "1",         24_00_00000,"24.00"),
    ("14", "OHE / 25 kV AC electrification",                      "Km",    "143",       1_05_00000, "150.15"),
    ("15", "Traction substations (2 nos)",                        "Nos",   "2",         18_50_00000,"37.00"),
    ("16", "Electronic interlocking & signalling",               "Km",    "71.8",      85_00000,   "61.03"),
    ("17", "Optical fibre & telecom",                             "Km",    "71.8",      18_50000,   "13.28"),
    ("18", "Land acquisition & compensation",                    "Hect",  "215.4",     1_44_84000, "312.00"),
    ("19", "Environmental mitigation & afforestation",           "LS",    "1",         12_00_00000,"12.00"),
    ("20", "Contingencies & general charges",                    "LS",    "1",         84_00_00000,"84.00"),
]

# Bridge schedule
BRIDGES = [
    ("MB-1", "Km 6.4",  "Kharun River",      "4 x 30.5 m", "PSC Girder",  "24.5"),
    ("MB-2", "Km 18.2", "Seonath Tributary", "3 x 24.0 m", "RCC Box",     "16.8"),
    ("MB-3", "Km 34.6", "Amner Nala",        "5 x 30.5 m", "PSC Girder",  "28.2"),
    ("MB-4", "Km 52.1", "Seonath River",     "6 x 45.7 m", "Steel Truss", "78.4"),
    ("MB-5", "Km 64.8", "Tandula Canal",     "2 x 24.0 m", "RCC Box",     "11.6"),
]

# Land use split
LAND_USE = [
    {"type": "Agricultural", "pct": 58, "ha": 124.9, "color": "#16a34a"},
    {"type": "Government",   "pct": 27, "ha": 58.2,  "color": "#003087"},
    {"type": "Forest",       "pct": 10, "ha": 21.5,  "color": "#15803d"},
    {"type": "Built-up",     "pct": 5,  "ha": 10.8,  "color": "#FF6B00"},
]
LAND_SUMMARY = {
    "total_ha": 215.4,
    "villages": ["Dharsiwa", "Mandhar", "Sirsia", "Kurud"],
    "households": 234,
    "compensation_cr": 312,
    "timeline": "18–24 months",
}

# Implementation timeline (Gantt)
TIMELINE = [
    {"phase": "Phase 1: Survey & DPR",            "months": 6,  "start": 0,  "color": "#003087"},
    {"phase": "Phase 2: Land Acquisition",        "months": 18, "start": 6,  "color": "#FF6B00"},
    {"phase": "Phase 3: Civil Construction",      "months": 36, "start": 12, "color": "#10b981"},
    {"phase": "Phase 4: Track Laying",            "months": 12, "start": 48, "color": "#8b5cf6"},
    {"phase": "Phase 5: Electrification",         "months": 8,  "start": 54, "color": "#0ea5e9"},
    {"phase": "Phase 6: Testing & Commissioning", "months": 6,  "start": 62, "color": "#f59e0b"},
]
TIMELINE_TOTAL_MONTHS = 68  # ~7 years (overlapping phases)

# Route survey coordinates (Route B)
SURVEY = [
    ("CH 0+000",   "Raipur Junction",    21.2514, 81.6296, 289),
    ("CH 18+200",  "Abhanpur (jn)",      21.0900, 81.5400, 301),
    ("CH 34+600",  "Amner crossing",     21.1450, 81.3900, 316),
    ("CH 52+100",  "Dharsiwa",           21.1700, 81.3300, 297),
    ("CH 71+800",  "Durg Junction",      21.1900, 81.2833, 291),
]

AI_INSIGHTS = [
    "Route B reduces deforestation by 65% compared to the shortest-path alignment.",
    "Earthwork reduced by 2.3 lakh cum vs Route A, lowering carbon footprint.",
    "Estimated ROI turns positive in 12 years on projected freight + passenger traffic.",
]
