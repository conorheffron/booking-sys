<<<<<<< HEAD
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { BookingPage } from './pages/BookingPage';
import { ReservationsPage } from './pages/ReservationsPage';
import { EditReservationPage } from './pages/EditReservationPage';
import { ErrorPage } from './pages/ErrorPage';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/style.css';

=======
import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { BookingPage } from './pages/BookingPage';
import { ReservationsPage } from './pages/ReservationsPage';
import { EditReservationPage } from './pages/EditReservationPage';
import { LoginPage } from './pages/LoginPage';
import { LogoutPage } from './pages/LogoutPage';
import { ErrorPage } from './pages/ErrorPage';
import { getAuthStatus } from './components/auth';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/style.css';

const RequireAuth: React.FC<{ children: React.ReactElement }> = ({ children }) => {
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    let mounted = true;
    getAuthStatus()
      .then((status) => {
        if (!mounted) {
          return;
        }
        setIsAuthenticated(status.authenticated);
      })
      .catch(() => {
        if (mounted) {
          setIsAuthenticated(false);
        }
      })
      .finally(() => {
        if (mounted) {
          setIsLoading(false);
        }
      });

    return () => {
      mounted = false;
    };
  }, []);

  if (isLoading) {
    return <div className="text-center pt-5">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
};

>>>>>>> origin/main
const App: React.FC = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<BookingPage />} />
      <Route path="/reservations" element={<ReservationsPage />} />
<<<<<<< HEAD
      <Route path="/reservations/edit/:id" element={<EditReservationPage />} />
=======
      <Route
        path="/reservations/edit/:id"
        element={(
          <RequireAuth>
            <EditReservationPage />
          </RequireAuth>
        )}
      />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/logout" element={<LogoutPage />} />
>>>>>>> origin/main
      <Route path="*" element={<ErrorPage message="Page not found." />} />
    </Routes>
  </BrowserRouter>
);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
