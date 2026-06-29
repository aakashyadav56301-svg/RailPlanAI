# 🚆 RailPlan AI — Railway Route Planning Platform (DEMO)

AI-Powered Railway Route Planning Platform for Indian Railways engineers.
Built for **visual impact** and a smooth, enterprise-grade demo experience.

**Stack:** React 18 + Tailwind CSS + Leaflet.js + Recharts (frontend) ·
FastAPI + SQLite (backend).

---

## ⚡ Quick Start

The frontend is a **single self-contained `index.html`** (React, Tailwind, Leaflet and
Recharts via CDN, app code precompiled & inlined — no build step, no Babel). It works fully
on mock data; the backend only adds real PDF/Excel/KML downloads.

### Easiest (Mac): one-click
Double-click **`START_MAC.command`** — it installs backend deps, starts the API + a local
web server, and opens the browser. (First time: right-click → Open to bypass Gatekeeper.)

### Manual — frontend only (zero install)
```bash
cd RailPlanAI
python3 -m http.server 5500
# open http://localhost:5500   (don't open the file directly with file://)
```

### Manual — with backend (for real PDF / Excel / KML downloads)
Terminal 1:
```bash
cd RailPlanAI/backend
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --port 8000
```
Terminal 2:
```bash
cd RailPlanAI
python3 -m http.server 5500
```
Then open **http://localhost:5500**.

**Demo login:** `Engineer` / `admin123`

> ⚠️ Always use `http://localhost:5500` (not `file://...`), and don't run VS Code's
> "Live Server" — use the `python3 -m http.server` command above. Internet must be on
> (React/Leaflet/Recharts load from CDN).

### ✅ Tested
Verified end-to-end in a headless Chrome: login → dashboard → AI route generation →
GIS map → new-project wizard → DPR workspace (all 4 tabs + compare popup), and real
**BOQ.xlsx + DPR.pdf downloads** with the backend running — **zero runtime errors**.

---

## 🧭 Modules

1. **Login** — railway-bridge CSS-art hero, animated train, demo credentials shown.
2. **Dashboard** — live stat cards (12 projects · 47 routes · ₹2,840 Cr saved · 8 DPRs),
   Recharts trend + priority mix, recent-projects table with status badges, AI Insights panel.
3. **New Project** — 3-step wizard with progress bar; Step 2 is an interactive Leaflet map
   to click Start (A) + End (B); on submit → animated route-generation loader → GIS viewer.
4. **GIS Map Viewer** — Leaflet centred on Raipur (21.2514, 81.6296) with toggle layers:
   Satellite, Elevation Heatmap, Rivers, Forest, Existing Railways, Villages — plus a live
   status bar (coordinates · zoom · scale).
5. **AI Route Generation (Phase 2)** — click **🤖 Generate Routes** (Dashboard, a
   Route Analysis card, or a project's detail modal) to launch:
   - a **full-screen "AI is working" overlay** with 7 steps appearing one-by-one with
     spinners → checkmarks (Loading GIS data → … → Generating 3 optimal routes) and a
     train progress bar;
   - **3 routes drawn on Leaflet** with a staggered reveal (A Shortest=blue,
     B AI-Optimized=green ★recommended, C Eco-Friendly=orange), click to select;
   - **3 comparison cards** (Route B glows green with "🤖 AI Recommended" + "BEST VALUE");
   - a **color-coded comparison table** (green=best, red=worst per parameter);
   - a **Recharts elevation profile** of all 3 routes with the steep section on Route A
     highlighted in red (Route B is smoothest);
   - a right-hand **mini analysis panel** (Terrain / Hydrology / Forest / Cost Saving).

   Backed by `GET /api/generate-routes` (falls back to identical hardcoded mock data).
6. **DPR Workspace (Phase 3)** — open from the sidebar (📄). A tabbed workspace for
   Route B (AI Optimized):
   - **Cost Breakdown** — Recharts donut of the 6 cost heads (₹1,298 Cr total), a bar
     chart comparing all 3 routes, and a 20-line **Bill of Quantities** table with a
     **Download BOQ (Excel)** button (real `.xlsx`).
   - **Land Acquisition** — summary cards (215.4 ha, 234 households, ₹312 Cr, 18–24 months),
     a land-use pie (Agri 58% / Govt 27% / Forest 10% / Built-up 5%) and the 4 affected
     villages (Dharsiwa, Mandhar, Sirsia, Kurud).
   - **Project Timeline** — Gantt-style bars + table for the 6 phases (~7 years).
   - **DPR Document** — cover-page preview, "Generate DPR" (3s animation →
     "DPR Generated Successfully ✅") → **Download PDF** (real 6-page reportlab PDF with
     cover, 11 sections, survey/bridge/BOQ/schedule tables).
   - **Right rail** — AI Insights (deforestation −65%, earthwork −2.3 lakh cum, ROI in 12y)
     and **Export Options**: DPR (PDF), BOQ (Excel), Route (KML for Google Earth),
     Share Project Link.
   - **"Compare with Traditional Method"** popup — 18 months/50 engineers vs 4 hours/2
     engineers, **94% faster**.
7. **Route Analysis** — supporting module (cards link into Generate Routes / Map / Details).

### Exports (backend)
`GET /api/export/dpr.pdf` · `GET /api/export/boq.xlsx` · `GET /api/export/route.kml` —
generated with **reportlab** + **openpyxl**. The frontend downloads from the backend when
running, and **gracefully falls back** to a client-generated CSV/KML if the API is offline
(the PDF requires the backend). Install deps with the updated `requirements.txt`.

## 🗄 Database
SQLite, auto-created and seeded on first run with the 3 demo projects:
*Raipur-Durg Bypass Line* (Active), *Nagpur-Amravati New Line* (Planning),
*Bilaspur-Korba Link* (Completed).

## 🎨 Design
Indian Railways palette — Navy `#003087` + Orange `#FF6B00`. Dark sidebar + light
content, smooth page/element animations, railway-themed loading messages,
and Indian number formatting (₹ Crores, km).

> Demo note: numbers and geospatial features are realistic mock data.
