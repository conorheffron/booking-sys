# Booking System Frontend (SPA)

[![Build and deploy container app to Azure Web App - booking-sys](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml)
[![Node.js CI](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml)
[![Node.js Package](https://github.com/conorheffron/booking-sys/actions/workflows/npm-publish-packages.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/npm-publish-packages.yml)
[![NPM Version](https://img.shields.io/npm/v/@conorheffron/booking-sys-frontend.svg)](https://www.npmjs.com/package/@conorheffron/booking-sys-frontend)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This is the decoupled, modern **React 19 + TypeScript 5 + Vite 8** Single Page Application (SPA) frontend for the Booking System. This client-side package was successfully migrated from legacy server-side templates to a highly interactive, responsive user experience utilizing **Bootstrap 5.3**.

- **NPM Package**: [@conorheffron/booking-sys-frontend](https://www.npmjs.com/package/@conorheffron/booking-sys-frontend)
- **GitHub Repository**: [conorheffron/booking-sys (Frontend Workspace)](https://github.com/conorheffron/booking-sys/tree/main/frontend)
- **GitHub Package**: [booking-sys-frontend (GitHub Container Registry)](https://github.com/conorheffron/booking-sys/pkgs/npm/booking-sys-frontend)

---

## 🏛️ Frontend System Architecture

The frontend is fully modularized. It interfaces with the backend web services through session-based REST APIs, enforcing client-side route protection and maintaining persistent user/version caches.

### Client-Side Component Structure & Data Flows

```mermaid
graph TD
    %% Styling
    classDef page fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#01579b;
    classDef comp fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px,color:#4a148c;
    classDef util fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20;
    classDef api fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#b71c1c;

    subgraph Router [Router & Authentication Guards]
        BrowserRouter[BrowserRouter]
        RequireAuth[RequireAuth Guard <br/><i>Route Guard HOC</i>]
    end

    subgraph Pages [UI Screen Controllers]
        BP[BookingPage.tsx<br/><i>Home / Scheduler</i>]
        RP[ReservationsPage.tsx<br/><i>Booking Manager</i>]
        ERP[EditReservationPage.tsx<br/><i>Secure Editor</i>]
        LP[LoginPage.tsx<br/><i>Login Gate</i>]
    end

    subgraph Reusable_UI [Visual Components]
        NAV[Navbar.tsx<br/><i>Header Navigation</i>]
    end

    subgraph Cache_State [State & Cache Stores]
        C_USER[currentUserCache.tsx<br/><i>sessionStorage</i>]
        C_VER[appVersionCache.tsx<br/><i>localStorage: 1h Expiry</i>]
        AUTH[auth.ts<br/><i>getAuthStatus, loginUser, logoutUser</i>]
        UTIL[Utils.tsx<br/><i>getCSRFToken, getSlots</i>]
    end

    subgraph External_API [Data Feeds]
        METEO[Open-Meteo Weather API]
        BACKEND[Django API /api/*]
    end

    class BP,RP,ERP,LP page;
    class NAV require_ui;
    class C_USER,C_VER,AUTH,UTIL util;
    class METEO,BACKEND api;

    %% Routing Flow
    BrowserRouter --> BP
    BrowserRouter --> RP
    BrowserRouter --> LP
    BrowserRouter -->|Secured path| RequireAuth
    RequireAuth --> ERP

    %% Component Interlocks
    Pages --> NAV
    NAV --> C_USER
    NAV --> C_VER
    NAV --> AUTH

    %% Data Interactions
    BP -->|Async Fetch with AbortController| METEO
    BP & ERP & RP -->|CSRF & Choice Arrays| UTIL
    AUTH & UTIL & Pages -->|HTTP JSON requests| BACKEND
```

---

## 🛠️ Features

1. **Reactive Booking Interface (`BookingPage`)**:
   - Selecting a date automatically initiates queries to view scheduled slots.
   - Selects from dynamically compiled 30-minute intervals between **09:00 AM and 07:00 PM**.
2. **Third-Party Weather Snippet**:
   - Live Dublin weather (temperature, wind speeds, descriptions) fetched from **Open-Meteo API**.
   - Employs React hook `AbortController` cancellation to eliminate memory leaks upon component unmounting.
3. **Session-Level Local Caching**:
   - **Current User Cache**: Stores active credentials in `sessionStorage` to prevent repeating user API reads.
   - **System Version Cache**: Stores application semantic release strings inside `localStorage` with a **1-hour TTL (Time-To-Live)** expiry configuration.
4. **Security Enforcement**:
   - Transparent CSRF pipeline fetching and loading validation cookies on demand.
   - Dynamic `RequireAuth` context checking to shield sensitive pages.

---

## 📋 Prerequisites

- **Node.js**: `v24` (LTS) or later is recommended.
- **npm**: `v11` or higher.

---

## 🚀 Installation & Setup

1. **Navigate to the frontend folder**:
    ```bash
    cd frontend
    ```

2. **Install all packages**:
    ```bash
    npm install
    ```

3. **Launch the Hot-Reloading Development Server**:
    ```bash
    npm run dev
    ```
    This launches the SPA locally at [http://localhost:5173](http://localhost:5173). 

4. **API Proxy Configuration**:
   During development, the SPA proxies modifying requests to the local backend dynamically. This is configured in `vite.config.ts`:
   ```typescript
   proxy: {
     '/api': 'http://0.0.0.0:8000',
     '/admin': 'http://0.0.0.0:8000',
     '/static/admin': 'http://0.0.0.0:8000',
   }
   ```

---

## 📦 Production Bundling

To compile and optimize the client application assets for production deployments:

```bash
npm run build
```
The compressed, code-split bundles are output directly into the `dist/` workspace folder.

### Previewing the Production Build Locally
To run a local web server displaying the pre-built static application assets:
```bash
npm run preview
```

---

## 🧪 Frontend Test Suites

The test suite is built on **Jest** combined with **JSDOM** (`@testing-library/react`) to simulate a high-fidelity web browser environment.

### 1. Execute All Tests
```bash
npm run test
```
*Expected Output Structure:*
```text
 PASS  test.tsx
 PASS  src/components/__tests__/Utils.test.tsx
 PASS  src/components/__tests__/appVersionCache.test.tsx
 PASS  src/components/__tests__/Navbar.test.tsx

Test Suites: 4 passed, 4 total
Tests:       12 passed, 12 total
Snapshots:   0 total
Time:        3.12 s
Ran all test suites.
```

### 2. Execute a Specific Test Suite (e.g., Utils)
```bash
npm run test -- src/components/__tests__/Utils.test.tsx
```

### 3. Target Specific Tests by Title / Regular Expression
```bash
npm run test -- -t="should fetch CSRF token from /api/csrf/"
```

### 4. Run Tests and Generate Coverage Metrics
```bash
npm run test -- --coverage
```
This generates a detailed code-coverage chart under the local `coverage/` folder.
