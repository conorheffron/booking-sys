# Booking System Architecture Documentation

This document provides a comprehensive technical blueprint of the **Booking System** application. It details the system architecture, backend implementation, frontend design, request-response lifecycles, and deployment orchestration.

---

## 1. High-Level System Architecture & Design

The Booking System is designed as a decoupled client-server architecture. It consists of a modern Single Page Application (SPA) frontend and a relational database-backed web API service, coordinated locally through a reverse proxy/dev-proxy configuration and deployed via Docker containers.

### 1.1 Granular System Components Design

The diagram below details the concrete components, files, utility modules, and database structures that interact across boundaries, illustrating the inner layers of both the React frontend and the Django backend:

```mermaid
graph TB
    %% Styling classes
    classDef frontend fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#01579b;
    classDef backend fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20;
    classDef storage fill:#eceff1,stroke:#455a64,stroke-width:2px,color:#263238;
    classDef ext fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100;

    subgraph FE [Frontend System Design - React 19 SPA]
        direction TB
        subgraph FE_Pages [UI Screen Pages]
            BP[BookingPage.tsx<br/><i>Home Screen</i>]
            RP[ReservationsPage.tsx<br/><i>Admin/Public List</i>]
            ERP[EditReservationPage.tsx<br/><i>Secure Editor</i>]
            LP[LoginPage.tsx<br/><i>Authentication Gate</i>]
            LOP[LogoutPage.tsx<br/><i>Session Cleanup</i>]
        end

        subgraph FE_Comp [Reusable Shared Components]
            NAV[Navbar.tsx<br/><i>Unified Navigation</i>]
        end

        subgraph FE_Utils [Utilities & State Handlers]
            AUTH_HELP[auth.ts<br/><i>getAuthStatus, loginUser, logoutUser</i>]
            C_USER[currentUserCache.tsx<br/><i>sessionStorage caching</i>]
            C_VER[appVersionCache.tsx<br/><i>localStorage caching</i>]
            UTIL[Utils.tsx<br/><i>getCSRFToken, getSlots</i>]
        end
    end

    subgraph BE [Backend System Design - Django 5.1 & DRF]
        direction TB
        subgraph BE_Routing [Routing & API Gateways]
            B_URLS[booking-sys/urls.py<br/><i>Root Router</i>]
            H_URLS[hr/urls.py<br/><i>App Specific Router</i>]
            DRF_SPEC[drf-spectacular<br/><i>Swagger & OpenAPI Doc</i>]
        end

        subgraph BE_Controller [Controllers, Wrappers & Forms]
            V_WRAP[views.py<br/><i>DRF @api_view Wrappers</i>]
            V_CLASS[views.py: Views Class<br/><i>API Core Method Handlers</i>]
            V_TEMPL[views.py: Views.edit_reservation<br/><i>Legacy SSR HTML View</i>]
            F_CLASS[forms.py<br/><i>EditReservationForm / ReservationForm</i>]
        end

        subgraph BE_Biz [Business Logic Layer]
            T_UTILS[time_utils.py: TimeUtils<br/><i>TZ Manager & Slot generator</i>]
        end

        subgraph BE_Models [ORM Data Layer]
            M_RES[models.py: Reservation<br/><i>Active Data Model</i>]
        end
    end

    subgraph DB [Storage Tier]
        SQLITE[(SQLite3 Database<br/><i>db.sqlite3</i>)]
    end

    subgraph EXT [External Services]
        METEO[Open-Meteo Weather API<br/><i>Direct REST Fetch</i>]
    end

    %% Apply Styles
    class BP,RP,ERP,LP,LOP FE_Pages;
    class NAV FE_Comp;
    class AUTH_HELP,C_USER,C_VER,UTIL FE_Utils;
    class B_URLS,H_URLS,DRF_SPEC BE_Routing;
    class V_WRAP,V_CLASS,V_TEMPL,F_CLASS BE_Controller;
    class T_UTILS BE_Biz;
    class M_RES BE_Models;
    class SQLITE DB;
    class METEO EXT;

    %% Interactions
    BP -->|Direct HTTPS GET| METEO
    FE_Pages --> NAV
    NAV --> C_USER
    NAV --> C_VER
    NAV --> AUTH_HELP

    BP & ERP & RP -->|Imports| UTIL
    
    %% Proxy Channel
    FE_Pages ====>|JSON API Requests<br/>via Vite DevProxy| B_URLS
    B_URLS --> H_URLS
    H_URLS --> V_WRAP
    V_WRAP --> V_CLASS
    V_CLASS --> T_UTILS
    V_CLASS --> M_RES
    
    %% Server Side Rendered view connection
    V_TEMPL -.->|Imports/Validates| F_CLASS
    
    M_RES -->|Django ORM Queries| SQLITE
```

### 1.2 Physical Infrastructure & Traffic Proxy

```text
+------------------------------------------------------------+
|                       WEB BROWSER                          |
|  +------------------------------------------------------+  |
|  |             React 19 (SPA) Frontend                  |  |
|  |  [BookingPage]  [ReservationsPage]  [EditPage]       |  |
|  +---------------------------+--------------------------+  |
+------------------------------|-----------------------------+
                               | (HTTP/JSON with CSRF & Cookies)
                               v
+------------------------------------------------------------+
|                  VITE DEVELOPMENT SERVER                   |
|  - Acts as a local reverse proxy for development           |
|  - Forwards /api/* and /admin/* requests to backend        |
+------------------------------|-----------------------------+
                               | (Proxied TCP to Port 8000)
                               v
+------------------------------------------------------------+
|                      DJANGO BACKEND                        |
|  +------------------------------------------------------+  |
|  |  Django REST Framework API Router (/api/)            |  |
|  +---------------------------+--------------------------+  |
|  |  Django Admin Interface (/admin)                     |  |
|  +---------------------------+--------------------------+  |
|  |  App "hr" - Reservation Models, Views, and Utils     |  |
|  +---------------------------+--------------------------+  |
+------------------------------|-----------------------------+
                               | (Django ORM Queries)
                               v
+------------------------------------------------------------+
|                     DATABASE LAYER                         |
|  - SQLite3 relational engine (db.sqlite3)                  |
|  - Manages hr_reservation table                            |
+------------------------------------------------------------+
```

---

## 2. UX Flow & State Transitions

The application presents a fluid, responsive user experience. It maps client-side interactions to secure screens, using route guards to intercept unauthenticated requests and gracefully managing input errors with real-time feedback.

### 2.1 UX Screen State Transition Diagram

The following state machine chart details how screens transition during standard operations, emphasizing route guarding and redirection context matching:

```mermaid
stateDiagram-v2
    classDef guest fill:#e1f5fe,stroke:#0288d1,stroke-dasharray: 5 5;
    classDef auth fill:#e8f5e9,stroke:#388e3c;
    classDef err fill:#ffebee,stroke:#c62828;

    [*] --> BookingPage_Guest : Init Browse (/)
    
    state "BookingPage (Home Screen)" as BookingPage_Guest {
        [*] --> FetchWeather : Load Screen
        FetchWeather --> DisplayWeather : Success
        FetchWeather --> WeatherError : Fails (Silent Fallback)
        --
        [*] --> FetchTodayBookings : Load Screen
        FetchTodayBookings --> ShowBookingsList
    }

    BookingPage_Guest --> LoginPage : Click "Login" on Navbar
    BookingPage_Guest --> ReservationsPage : Click "Bookings" on Navbar
    
    state "LoginPage Screen (/login)" as LoginPage {
        [*] --> EnterCredentials
        EnterCredentials --> AuthenticateSession : Submit Form
        AuthenticateSession --> CreateCookie : Success [200 OK]
        AuthenticateSession --> DisplayAuthError : Invalid Credentials [41]
    }
    
    DisplayAuthError --> EnterCredentials : Retry

    state "ReservationsPage (/reservations)" as ReservationsPage {
        [*] --> LoadAllReservations
        LoadAllReservations --> ShowReservationsTable
        ShowReservationsTable --> TriggerDelete : Click "Delete" Button
        ShowReservationsTable --> TriggerClearAll : Click "Clear All" Button
    }

    state "EditReservationPage (/reservations/edit/:id)" as EditReservationPage {
        [*] --> LoadReservationDetail : Fetch booking details
        LoadReservationDetail --> DisplayEditForm
        DisplayEditForm --> ValidateEditSubmit : Submit Edited Form
    }

    %% Guard Checking
    ReservationsPage --> RequireAuthGuard : Click "Edit" Button on Row

    state RequireAuthGuard <<choice>>
    RequireAuthGuard --> EditReservationPage : Authenticated [True]
    RequireAuthGuard --> LoginPage : Unauthenticated [False] <br/><i>(Saves "from" route in location.state)</i>

    LoginPage --> RouteRecovery <<choice>> : Successful Authentication
    RouteRecovery --> EditReservationPage : Redirect to target route <br/><i>(e.g., /reservations/edit/:id)</i>
    RouteRecovery --> BookingPage_Guest : No target saved (Default to /)

    %% Back paths
    EditReservationPage --> ReservationsPage : Submit Success [Redirects with 1.2s delay]
    EditReservationPage --> ReservationsPage : Click "Cancel"

    %% Logout Operation
    ReservationsPage --> LogoutPage : Click "Logout" on Navbar
    LogoutPage --> BookingPage_Guest : Clears session caches & Redirects to Home

    class BookingPage_Guest,ReservationsPage guest;
    class EditReservationPage,LoginPage,RouteRecovery auth;
    class DisplayAuthError,RequireAuthGuard err;
```

### 2.2 Interactive UX Scenario Playbooks

#### Scenario A: The Guest Booking Workflow
1. **Landing**: The user lands on `/` (`BookingPage`). The weather module fetches Dublin meteorological stats dynamically from Open-Meteo.
2. **Date Picking**: Choosing a date triggers an async fetch to retrieve current bookings for that date.
3. **Form Entry**: Fills in the name and picks a 30-minute interval from the dropdown selection list.
4. **Submission**: Click **Reserve**.
   - **Case 1 (Invalid Input - Past Reservation)**: Backend rejects with `400 Bad Request`. An alert banner is shown with the message `Cannot make a reservation for a past date/time.`
   - **Case 2 (Invalid Input - Double Booking)**: Slot is occupied. Backend returns `400 Bad Request` with `Booking Failed: Already Reserved.`
   - **Case 3 (Valid Input)**: Backend creates the slot and responds with `201 Created`. The list of bookings for that date is refreshed, and a success banner is shown which automatically fades after 3 seconds.

#### Scenario B: The Secure Edit Redirect Journey (Route Guarding)
1. **Browse**: User lands on `/reservations`, browsing the list of bookings.
2. **Action**: User clicks the **Edit** link next to a specific reservation row.
3. **Guard Check**: The `RequireAuth` higher-order component intercepts the route, executing a background query (`getAuthStatus()`) to check if the session is authenticated.
4. **Redirect**:
   - The user is not logged in. `RequireAuth` redirects them to `/login` using:
     ```typescript
     <Navigate to="/login" replace state={{ from: location }} />
     ```
5. **Login**: User inputs credentials. Upon validation, the page retrieves the state:
   - It redirects the user straight to the edit route saved in `state.from` (e.g., `/reservations/edit/12`).
6. **Modification**: The user modifies the booking and clicks **Save**. A success message appears, and after 1.2 seconds they are redirected back to the `/reservations` page.

---

## 3. Backend Technical Overview

The backend is built on **Django 5.1** and structured around a main app called `hr`. It serves as a secure RESTful API provider using the **Django REST Framework (DRF)**. API contract specifications and Interactive API documentation are automatically managed via **drf-spectacular**.

### 3.1 Database Models & Relations

The application employs a streamlined relational schema centered around a single core entity representing reservations.

#### Entity-Relationship Schema

```mermaid
erDiagram
    RESERVATION {
        int id PK "AutoField"
        varchar first_name "max_length=30"
        date reservation_date "DateField"
        time reservation_slot "TimeField"
    }
```

- **Reservation Model (`backend/hr/models.py`)**:
  - `id`: Unique AutoField acting as the primary key.
  - `first_name`: A CharField limited to 30 characters representing the client's booking name.
  - `reservation_date`: A DateField representing the date of reservation.
  - `reservation_slot`: A TimeField representing the specific reservation hour (e.g., "14:30:00").

### 3.2 Timezone and Reservation Slot Business Logic

Reservations are governed by precise timezone and scheduling boundaries implemented in `backend/hr/time_utils.py` and validated inside views.

1. **Timezone Context**:
   - `settings.py` sets `TIME_ZONE = "Europe/Dublin"` and `USE_TZ = True`.
   - `TimeUtils.get_current_date_time()` generates an exact localized timestamp. It instantiates a UTC timestamp (`pytz.timezone('UTC')`) and shifts it explicitly to `Europe/London` (which aligns with Dublin's seasonal daylight savings changes) to perform chronological comparison.
2. **Reservation Slots Constraints**:
   - Eligible timeslots range from **09:00 AM to 07:00 PM** at **30-minute intervals** (i.e. `09:00 AM, 09:30 AM, ..., 06:30 PM, 07:00 PM`).
   - `TimeUtils.generate_time_slots` handles the logical matrix calculation to generate standard choice mappings.

### 3.3 Security, Sessions, and Session Synchronization

Security is enforced at multiple layers:

- **CSRF Protection**: All mutating operations (PUT, POST, DELETE) are safeguarded via Django's default `CsrfViewMiddleware`. The frontend issues an initial `GET /api/csrf/` request to capture the CSRF token from the secure cookie and then appends it as an `X-CSRFToken` request header in successive mutating API calls.
- **Granular API Permissions**: Rather than a blanket global authorization block, endpoint execution checks for specific Model Permissions assigned to the authenticated user using `Views._require_api_permission(request, codename)`.
  - To create a booking, users need `hr.add_reservation`.
  - To edit a booking, users need `hr.change_reservation`.
  - To delete a booking, users need `hr.delete_reservation`.
- **System Cleansings**: Only user accounts flagged with administrative access (`is_staff = True` or `is_superuser = True`) are permitted to bulk delete/clear upcoming reservations (`DELETE /api/bookings`).

---

## 4. API Endpoint Registry

All backend services are exposed via standardized JSON endpoints mapped in `backend/hr/urls.py` and documented in Swagger.

| HTTP Method | API Path | Auth Required? | Req. Permission | Payload Body (JSON) | Success Code | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GET** | `/api/csrf/` | No | None | None | `200 OK` | Retrieves CSRF token to bind to security headers. |
| **GET** | `/api/auth/status` | No | None | None | `200 OK` | Returns session authentication status and username. |
| **POST** | `/api/auth/login` | No | None | `{ "username": "...", "password": "..." }` | `200 OK` | Evaluates credentials and sets Django session cookie. |
| **POST** | `/api/auth/logout` | No | None | None | `200 OK` | Destroys the active session cookie. |
| **GET** | `/api/version/` | No | None | None | `200 OK` | Returns current system semantic version string. |
| **GET** | `/api/user/` | No | None | None | `200 OK` | Returns the logged-in user name or `'unknown'`. |
| **GET** | `/api/bookings` | No | None | Query Params: `?date=YYYY-MM-DD` | `200 OK` | Returns list of bookings. If date is blank/omitted, yields future bookings from today. |
| **DELETE** | `/api/bookings` | Yes | Staff/Superuser | None | `200 OK` | Clears all reservations starting from today onward. |
| **GET** | `/api/bookingsById/<id>` | No | None | None | `200 OK` | Fetches details of a specific reservation. |
| **PUT** | `/api/bookingsById/<id>` | Yes | `hr.change_reservation` | `{ "first_name": "...", "reservation_date": "YYYY-MM-DD", "reservation_slot": "HH:MM AM/PM" }` | `200 OK` | Updates an existing booking. Rejects changes to past dates/times or duplicate slots. |
| **DELETE** | `/api/bookingsById/<id>` | Yes | `hr.delete_reservation` | None | `200 OK` | Deletes a reservation. |
| **PUT** | `/api/reservations` | Yes | `hr.add_reservation` | `{ "first_name": "...", "reservation_date": "YYYY-MM-DD", "reservation_slot": "HH:MM AM/PM" }` | `201 Created` | Creates a new reservation. Implements past dates/times and double-booking rejection. |

---

## 5. Frontend Technical Overview

The client-side application is a single-page architecture built with **React 19** and **TypeScript 5**, configured with **Vite 8** for lightning-fast bundling, HMR, and proxy routing during development.

### 5.1 Routing & Navigation State

Frontend URL routing is managed by `react-router-dom` (v7) inside `frontend/src/main.tsx`. Routes are defined as follows:

```text
              [Browser Router (App)]
                        │
         ┌──────────────┼──────────────┬──────────────┐
         ▼              ▼              ▼              ▼
     "/" (Public)   "/reservations"  "/login"      "*" (Fallback)
         │              │              │              │
     [BookingPage]  [Reservations] [LoginPage]    [ErrorPage]
                        │
                        ▼ (Auth Protected Check)
                "/reservations/edit/:id"
                        │
            [RequireAuth Guard HOC]
                        │
                        ▼ (Authorized)
              [EditReservationPage]
```

### 5.2 Local Cache Strategies

To minimize redundant server roundtrips and improve user experience, the frontend implements two caching utilities:

1. **Application Version Cache (`appVersionCache.tsx`)**:
   - Caches the application version returned by `/api/version/` in the browser's `localStorage`.
   - Uses a **Cache Time-To-Live (TTL) of 1 hour** (3,600,000 ms). If the cache expires, it pulls a fresh value from the server.
2. **Current User Cache (`currentUserCache.tsx`)**:
   - Caches the authenticated user's name returned by `/api/user/` in `sessionStorage`.
   - Prevents refetching username strings during component re-renders of the `Navbar` across pages, clearing immediately when the session is closed or when a user logs out.

### 5.3 Third-Party Weather API Integration

To help users select the best reservation times, the `BookingPage` displays a real-time **Dublin Weather Snapshot** by connecting to the public **Open-Meteo API**:
- **Endpoint**: `https://api.open-meteo.com/v1/forecast?latitude=53.3498&longitude=-6.2603&current=temperature_2m,wind_speed_10m,weather_code&timezone=auto`
- **Aesthetic Presentation**: A responsive, linear gradient banner displays temperatures, wind speeds, and mapped description statuses (e.g. "Clear sky", "Partly cloudy", "Rain showers").
- **Network Safety**: Employs an `AbortController` signal bound to the React `useEffect` hook. This cancels the background fetch if the user navigates away before the network request resolves, preventing memory leaks and state updates on unmounted components.

---

## 6. End-to-End System Data Flows

### 6.1 Authentication and Session Setup Flow

This sequence demonstrates how a user establishes an authenticated session to manage bookings.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend as React SPA (LoginPage)
    participant Proxy as Vite Dev Proxy
    participant Backend as Django Server (Views.login)
    participant DB as SQLite3 Database

    User->>Frontend: Enters Username & Password
    Frontend->>Proxy: GET /api/csrf/
    Proxy->>Backend: Forward to csrf_view
    Backend-->>Frontend: JSON: { "csrfToken": "<token>" }
    Frontend->>Proxy: POST /api/auth/login with X-CSRFToken header
    Proxy->>Backend: Forward to login_view
    Backend->>DB: Query user credentials & check password
    DB-->>Backend: User credentials valid
    Backend->>Backend: Create Session & Issue Session ID Cookie
    Backend-->>Frontend: JSON: { "success": true, "username": "..." }
    Frontend->>Frontend: Cache username in sessionStorage
    Frontend->>User: Redirect to index / previous page
```

### 6.2 Creating a Booking Flow

This sequence demonstrates creating a reservation, detailing the validations performed.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend as React SPA (BookingPage)
    participant Proxy as Vite Dev Proxy
    participant Backend as Django Server (save_reservation)
    participant DB as SQLite3 Database

    User->>Frontend: Fills Name, Date, Slot & Clicks "Reserve"
    Frontend->>Proxy: GET /api/csrf/ (Retrieve token)
    Proxy->>Backend: Forward to csrf_view
    Backend-->>Frontend: csrfToken
    Frontend->>Proxy: PUT /api/reservations (X-CSRFToken + JSON Body)
    Proxy->>Backend: Forward to save_reservation_view
    
    rect rgb(240, 240, 240)
        Note over Backend, DB: Validation Phase
        Backend->>Backend: Check user permissions (hr.add_reservation)
        Backend->>Backend: Validate slot is a valid 30-min window
        Backend->>Backend: Validate booking date/time is NOT in the past
        Backend->>DB: Check if slot is already booked for date
        DB-->>Backend: Returns exists check result
    end

    alt Already Booked or Past Date
        Backend-->>Frontend: JSON: { "error": "Booking Failed: Already Reserved." / "Cannot make reservation for past..." } [400 Bad Request]
        Frontend->>User: Display alert with error details
    else Validation Successful
        Backend->>DB: INSERT INTO hr_reservation (first_name, reservation_date, reservation_slot)
        DB-->>Backend: Created row
        Backend-->>Frontend: JSON: { "success": true, "id": 101, ... } [21 Created]
        Frontend->>Frontend: Refetch bookings list for chosen date
        Frontend->>User: Display "Reservation submitted!" success banner
    end
```

---

## 7. Deployment & Development Architecture

The development and containerization workflow uses a unified, deterministic environment.

### 7.1 Multi-Process Container Setup

Local deployments are fully containerized using **Docker** and **Docker Compose**.

- **`Dockerfile` (Single-Stage Custom Build)**:
  - Uses `python:3.14-slim` as the base image.
  - Installs binary dependencies like `default-libmysqlclient-dev` (for potential production MySQL adapters), system compilers, and **Node.js 24**.
  - Installs Python dependencies from `backend/requirements.txt` and Node dependencies from `frontend/package.json` under `/backend` and `/frontend` respectively.
  - Copies all source trees and invokes Django's static compiler `python manage.py collectstatic --noinput` to prepare Django Admin stylesheets.
- **Entrypoint Management (`entrypoint.sh`)**:
  - The container orchestrates two simultaneous servers using process backgrounding:
    1. Starts Django server: `python manage.py runserver 0.0.0.0:8000 &` (Backgrounded).
    2. Delays for 5 seconds to ensure port availability and DB stability.
    3. Starts Vite dev server: `npm run dev -- --host` (Foreground).
  - Port `8000` (Django REST API) and Port `5173` (Vite) are both exposed through Docker Compose to host interfaces.

### 7.2 Testing Framework

The application ensures stability through parallel testing pipelines:

1. **Backend Testing Pipeline**:
   - Utilizes `pytest` (configured in `backend/pytest.ini`).
   - `backend/hr/test_apis.py` runs REST integration tests verifying CRUD endpoints, permissions, validations, and CSRF barriers.
   - `backend/hr/test_forms.py` validates Django form layout checks and default values.
2. **Frontend Testing Pipeline**:
   - Built on `jest` with `jsdom` configuration (`frontend/jest.config.js`).
   - Employs `@testing-library/react` and `@testing-library/jest-dom` for component testing.
   - Core pages and components (e.g. `BookingPage.test.tsx`, `Navbar.test.tsx`, caching modules) are fully covered using mock mockups for fetch endpoints and local storage operations.
