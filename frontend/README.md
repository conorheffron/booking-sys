# Booking System Frontend

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
