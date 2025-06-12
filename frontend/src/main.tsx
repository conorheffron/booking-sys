import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { BookingPage } from './pages/BookingPage';
import { ReservationsPage } from './pages/ReservationsPage';
import { EditReservationPage } from './pages/EditReservationPage';
import { ErrorPage } from './pages/ErrorPage';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/style.css';

const App: React.FC = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<BookingPage />} />
      <Route path="/reservations" element={<ReservationsPage />} />
      <Route path="/reservations/edit/:id" element={<EditReservationPage />} />
      <Route path="*" element={<ErrorPage message="Page not found." />} />
    </Routes>
  </BrowserRouter>
);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
