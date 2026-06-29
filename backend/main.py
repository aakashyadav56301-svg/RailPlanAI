"""
RailPlan AI — Backend API
FastAPI + SQLite (demo). Pre-populated with 3 demo projects.

Run:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Docs: http://localhost:8000/docs
"""
import os
import sqlite3
import json
from datetime import datetime
from contextlib import closing

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional, List

DB_PATH = os.path.join(os.path.dirname(__file__), "railplan.db")

app = FastAPI(title="RailPlan AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------- DB helpers -----------------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(get_conn()) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                zone TEXT,
                description TEXT,
                status TEXT DEFAULT 'Planning',
                priority TEXT DEFAULT 'Cost',
                start_lat REAL, start_lng REAL,
                end_lat REAL, end_lng REAL,
                length_km REAL,
                cost_cr REAL,
                cost_saved_cr REAL,
                created_at TEXT
            )
            """
        )
        # seed only if empty
        cur = conn.execute("SELECT COUNT(*) AS c FROM projects")
        if cur.fetchone()["c"] == 0:
            seed = [
                ("Raipur-Durg Bypass Line", "South East Central", 
                 "A 38 km broad-gauge bypass to decongest Raipur Junction and improve freight throughput on the Mumbai–Howrah corridor.",
                 "Active", "Cost", 21.2514, 81.6296, 21.1904, 81.2849, 38.4, 1240.0, 312.0),
                ("Nagpur-Amravati New Line", "Central",
                 "Proposed 154 km greenfield line connecting Nagpur and Amravati to boost regional connectivity and cotton freight.",
                 "Planning", "Environment", 21.1458, 79.0882, 20.9374, 77.7796, 154.2, 4820.0, 905.0),
                ("Bilaspur-Korba Link", "South East Central",
                 "Completed 102 km doubling and electrification project serving the Korba coalfields and NTPC power plants.",
                 "Completed", "Time", 22.0797, 82.1391, 22.3595, 82.7501, 102.6, 2980.0, 488.0),
            ]
            now = datetime.utcnow().isoformat()
            conn.executemany(
                """INSERT INTO projects
                   (name, zone, description, status, priority, start_lat, start_lng,
                    end_lat, end_lng, length_km, cost_cr, cost_saved_cr, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [row + (now,) for row in seed],
            )


class ProjectIn(BaseModel):
    name: str
    zone: Optional[str] = "South East Central"
    description: Optional[str] = ""
    status: Optional[str] = "Planning"
    priority: Optional[str] = "Cost"
    start_lat: Optional[float] = None
    start_lng: Optional[float] = None
    end_lat: Optional[float] = None
    end_lng: Optional[float] = None


def row_to_dict(r):
    return {k: r[k] for k in r.keys()}


# ----------------------------- Routes -----------------------------
@app.on_event("startup")
def _startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "RailPlan AI", "time": datetime.utcnow().isoformat()}


@app.post("/api/login")
def login(payload: dict):
    if payload.get("username") == "Engineer" and payload.get("password") == "admin123":
        return {"token": "demo-token-railplan", "user": {"name": "Engineer", "role": "Route Planner"}}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/api/stats")
def stats():
    with closing(get_conn()) as conn:
        rows = conn.execute("SELECT status, cost_saved_cr FROM projects").fetchall()
    total_saved = sum(r["cost_saved_cr"] or 0 for r in rows)
    return {
        "total_projects": 12,
        "routes_analyzed": 47,
        "cost_saved_cr": 2840,
        "dprs_generated": 8,
        "db_projects": len(rows),
        "db_cost_saved_cr": round(total_saved, 1),
    }


@app.get("/api/projects")
def list_projects():
    with closing(get_conn()) as conn:
        rows = conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
    return [row_to_dict(r) for r in rows]


@app.get("/api/projects/{pid}")
def get_project(pid: int):
    with closing(get_conn()) as conn:
        r = conn.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
    if not r:
        raise HTTPException(404, "Project not found")
    return row_to_dict(r)


@app.post("/api/projects")
def create_project(p: ProjectIn):
    # simple mock route metrics
    import math
    length = 0
    cost = 0
    saved = 0
    if None not in (p.start_lat, p.start_lng, p.end_lat, p.end_lng):
        dlat = (p.end_lat - p.start_lat) * 111
        dlng = (p.end_lng - p.start_lng) * 105
        length = round(math.hypot(dlat, dlng) * 1.18, 1)  # winding factor
        cost = round(length * 31.5, 1)
        saved = round(cost * 0.21, 1)
    now = datetime.utcnow().isoformat()
    with closing(get_conn()) as conn, conn:
        cur = conn.execute(
            """INSERT INTO projects
               (name, zone, description, status, priority, start_lat, start_lng,
                end_lat, end_lng, length_km, cost_cr, cost_saved_cr, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p.name, p.zone, p.description, p.status, p.priority, p.start_lat, p.start_lng,
             p.end_lat, p.end_lng, length, cost, saved, now),
        )
        pid = cur.lastrowid
        r = conn.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
    return row_to_dict(r)


@app.get("/api/generate-routes")
def generate_routes(pid: Optional[int] = None):
    """Return 3 demo-optimised alignments (hardcoded realistic data for the
    Raipur–Durg corridor). The frontend animates the 'AI working' sequence."""
    routes = [
        {
            "id": "A", "name": "Shortest Path", "color": "#2196F3", "recommended": False,
            "waypoints": [[21.2514, 81.6296], [21.6833, 81.5667], [21.7167, 81.9500], [21.1900, 81.2833]],
            "wpNames": ["Raipur", "Tilda", "Bhatapara", "Durg"],
            "distance_km": 67.3, "cost_cr": 1456, "bridges_major": 8, "bridges_minor": 14,
            "tunnels": 0, "forest_sqkm": 2.3, "land_ha": 487, "gradient": "1:87", "gradient_status": "warn",
        },
        {
            "id": "B", "name": "AI Optimized", "color": "#4CAF50", "recommended": True,
            "waypoints": [[21.2514, 81.6296], [21.0900, 81.5400], [21.1450, 81.3900], [21.1900, 81.2833]],
            "wpNames": ["Raipur", "Abhanpur", "Dharsiwa", "Durg"],
            "distance_km": 71.8, "cost_cr": 1298, "bridges_major": 5, "bridges_minor": 9,
            "tunnels": 0, "forest_sqkm": 0.8, "land_ha": 423, "gradient": "1:120", "gradient_status": "good",
        },
        {
            "id": "C", "name": "Eco-Friendly", "color": "#FF9800", "recommended": False,
            "waypoints": [[21.2514, 81.6296], [21.3300, 81.4500], [21.2600, 81.3300], [21.1900, 81.2833]],
            "wpNames": ["Raipur", "Mandhar", "Sirsia", "Durg"],
            "distance_km": 79.2, "cost_cr": 1512, "bridges_major": 4, "bridges_minor": 7,
            "tunnels": 0, "forest_sqkm": 0.2, "land_ha": 398, "gradient": "1:135", "gradient_status": "good",
        },
    ]
    return {"project_id": pid, "routes": routes}


# --------------------- Phase 3: DPR data + exports ---------------------
@app.get("/api/dpr-data")
def dpr_data():
    import dpr_data as D
    return {
        "project": D.PROJECT,
        "cost_split": D.COST_SPLIT,
        "route_costs": D.ROUTE_COSTS,
        "boq": [{"sr": r[0], "item": r[1], "unit": r[2], "qty": r[3],
                 "rate": r[4], "amount": float(r[5])} for r in D.BOQ],
        "bridges": [{"no": b[0], "location": b[1], "river": b[2], "span": b[3],
                     "type": b[4], "cost": float(b[5])} for b in D.BRIDGES],
        "land_use": D.LAND_USE,
        "land_summary": D.LAND_SUMMARY,
        "timeline": D.TIMELINE,
        "timeline_total_months": D.TIMELINE_TOTAL_MONTHS,
        "survey": [{"chainage": s[0], "location": s[1], "lat": s[2],
                    "lng": s[3], "rl": s[4]} for s in D.SURVEY],
        "ai_insights": D.AI_INSIGHTS,
    }


@app.get("/api/export/dpr.pdf")
def export_dpr():
    import generators
    pdf = generators.build_dpr_pdf()
    return Response(content=pdf, media_type="application/pdf",
                    headers={"Content-Disposition": 'attachment; filename="RaipurDurg_DPR.pdf"'})


@app.get("/api/export/boq.xlsx")
def export_boq():
    import generators
    data = generators.build_boq_xlsx()
    return Response(content=data,
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": 'attachment; filename="RaipurDurg_BOQ.xlsx"'})


@app.get("/api/export/route.kml")
def export_kml():
    import generators
    return Response(content=generators.build_route_kml(),
                    media_type="application/vnd.google-earth.kml+xml",
                    headers={"Content-Disposition": 'attachment; filename="RaipurDurg_Route.kml"'})


@app.delete("/api/projects/{pid}")
def delete_project(pid: int):
    with closing(get_conn()) as conn, conn:
        conn.execute("DELETE FROM projects WHERE id=?", (pid,))
    return {"deleted": pid}


if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
