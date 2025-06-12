FROM python:3.13-slim AS backend

WORKDIR /app

# Install MySQL and build tools for mysqlclient, plus Node.js for frontend
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      default-libmysqlclient-dev build-essential pkg-config curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --upgrade pip && pip install -r backend/requirements.txt

# Node dependencies
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install

# Copy all source code
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Entrypoint script to run backend, then frontend
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000 5173

ENTRYPOINT ["/entrypoint.sh"]
