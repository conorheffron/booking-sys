# Booking System Frontend

[![Build and deploy container app to Azure Web App - booking-sys](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/main_booking-sys.yml)

[![Node.js CI](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml/badge.svg)](https://github.com/conorheffron/booking-sys/actions/workflows/node.js.yml)

This is the React + TypeScript frontend for the Booking System, migrated from traditional static assets and templates.

## Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later recommended)
- [npm](https://www.npmjs.com/) (comes with Node.js)

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
```shell
(base) frontend % npm test 

> booking-sys-frontend@1.0.0 test
> jest

 PASS  src/components/__tests__/utils.test.tsx
 PASS  ./test.tsx

Test Suites: 2 passed, 2 total
Tests:       5 passed, 5 total
Snapshots:   0 total
Time:        0.897 s, estimated 1 s
Ran all test suites.
```

```shell

(base) frontend % npm test -- frontend/src/components/__tests__/utils.test.ts

> booking-sys-frontend@1.0.0 test
> jest frontend/src/components/__tests__/utils.test.ts

 PASS  src/components/__tests__/utils.test.tsx
  getCSRFToken
    ✓ should return the CSRF token value if present in the cookie (2 ms)
    ✓ should return an empty string if CSRF token is not present in the cookie (1 ms)
    ✓ should return the first CSRF token if multiple are present (1 ms)
    ✓ should handle cookies with extra spaces (1 ms)

Test Suites: 1 passed, 1 total
Tests:       4 passed, 4 total
Snapshots:   0 total
Time:        0.84 s, estimated 1 s
Ran all test suites matching /frontend\/src\/components\/__tests__\/utils.test.ts/i.
```
