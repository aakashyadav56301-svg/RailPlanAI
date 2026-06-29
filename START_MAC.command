#!/bin/bash
# ============================================================
#  RailPlan AI — One-click start for Mac
#  Is file ko double-click karo (ya Terminal mein chalao).
#  Backend + Frontend dono start ho jayenge aur browser khulega.
# ============================================================

# Is script ke folder mein jao (chahe kahin se bhi chalao)
cd "$(dirname "$0")"

echo "==============================================="
echo "   🚆  RailPlan AI  —  starting up..."
echo "==============================================="

# Python check
if ! command -v python3 &> /dev/null; then
  echo "❌ python3 nahi mila."
  echo "   Install karo:  xcode-select --install"
  echo "   ya python.org se download karo, fir dobara try karo."
  read -p "Press Enter to close..."
  exit 1
fi

# ---- Backend setup ----
echo ""
echo "📦 Backend dependencies install kar rahe hain (pehli baar thoda time lagega)..."
cd backend
python3 -m pip install -q -r requirements.txt 2>/dev/null

echo "🚀 Backend start (port 8000)..."
python3 -m uvicorn main:app --port 8000 > /tmp/railplan_backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# ---- Frontend ----
echo "🌐 Frontend start (port 5500)..."
python3 -m http.server 5500 > /tmp/railplan_frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 3
echo ""
echo "==============================================="
echo "   ✅  RailPlan AI chal raha hai!"
echo ""
echo "   Browser mein kholo:  http://localhost:5500"
echo "   Login:  Engineer  /  admin123"
echo "==============================================="
echo ""
echo "   Band karne ke liye yahan  Ctrl + C  dabao."
echo ""

# Browser auto-open
open "http://localhost:5500"

# Jab Ctrl+C dabe to dono band kar do
trap "echo ''; echo 'Band kar rahe hain...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT
wait
