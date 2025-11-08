# Booking System Frontend

[![Build and deploy container app to Azure Web App - booking-sys](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml)

[![Node.js CI](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml)

[![Node.js Package](https://github.com/conorheffron/booking-sys/actions/workflows/npm-publish-packages.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/npm-publish-packages.yml)

- See 'booking-sys-frontend' `npmjs package` at https://www.npmjs.com/package/@conorheffron/booking-sys-frontend
- See 'booking-sys-frontend' `GitHub package` at https://github.com/conorheffron/booking-sys/pkgs/npm/booking-sys-frontend

This is the React + TypeScript frontend for the Booking System, migrated from traditional static assets and templates.

## Prerequisites

- [Node.js](https://nodejs.org/) (`v24` (LTS) recommended)
- [npm](https://www.npmjs.com/) (comes with Node.js `11.6.2`)

## Installation

1. Navigate to the frontend directory:
    ```bash
    cd booking-sys/frontend
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

## Running the Development Server

To start the frontend in development mode (with hot reloading):

```bash
npm run dev
```

This will start the app at [http://localhost:5173](http://localhost:5173) (or another port if 5173 is taken).

## Building for Production

To create a production build:

```bash
npm run build
```

The optimized build will be output to the `dist/` folder.

## Preview the Production Build

After building, you can preview the production build locally:

```bash
npm run preview
```

## Project Structure

- `src/` - React source code (components, pages, styles)
- `public/` - Static assets (images, favicon, etc.)

## Environment Variables

If needed, copy `.env.example` to `.env` and update any environment variables.

---

Feel free to open issues or pull requests for improvements!

## Frontend Tests
1. Run all tests.
```shell
(base) frontend % npm run test

> booking-sys-frontend@3.0.2 test
> jest

 PASS  ./test.tsx
 PASS  src/components/__tests__/Utils.test.tsx

Test Suites: 2 passed, 2 total
Tests:       5 passed, 5 total
Snapshots:   0 total
Time:        2.844 s
Ran all test suites.
```
2. Run specific test suite for a compoenent (Utils.ts).
```shell

(base) frontend % npm run test -- frontend/src/components/__tests__/Utils.test.ts

> booking-sys-frontend@3.0.2 test
> jest frontend/src/components/__tests__/Utils.test.ts

 PASS  src/components/__tests__/Utils.test.tsx
  getSlots
    ✓ should return all 30-minute intervals from 09:00 AM to 07:00 PM (inclusive) (4 ms)
    ✓ should return a fresh array each time (1 ms)
  getCSRFToken
    ✓ should fetch CSRF token from /api/csrf/ (4 ms)
    ✓ should throw if response is not as expected (1 ms)

Test Suites: 1 passed, 1 total
Tests:       4 passed, 4 total
Snapshots:   0 total
Time:        1.95 s
Ran all test suites matching /frontend\/src\/components\/__tests__\/Utils.test.ts/i.
```
3. Run specific test by test name or title.
```
npm run test -- -t="calls fetchReservations again when Refresh button is clicked"
```
4. Run all tests with coverage report.
```
npm run test -- --coverage
```
