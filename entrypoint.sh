#!/bin/sh

# Start Django backend (runs in background)
cd /backend
python manage.py runserver 0.0.0.0:8000 &

# Wait a few seconds to ensure backend is up (optional)
sleep 5

# Start Vite frontend (runs in foreground)
cd /frontend
npm run dev -- --host
