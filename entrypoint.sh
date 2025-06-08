#!/bin/sh

# Start Django backend (runs in background)
cd /app/backend
python manage.py runserver 0.0.0.0:8000 &

# Wait a few seconds to ensure backend is up (optional)
sleep 5

# Start Vite frontend (runs in foreground)
cd /app/frontend
npm run dev -- --host