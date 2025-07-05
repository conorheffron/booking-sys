import React, { useState, useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import { getCSRFToken, getSlots } from '../components/Utils';

interface BookingFormData {
  first_name: string;
  reservation_date: string;
  reservation_slot: string;
}

const slots = getSlots();

interface Booking extends BookingFormData {}

export const BookingPage: React.FC = () => {
  // Get today's date in YYYY-MM-DD format
  const getToday = () => {
    const d = new Date();
    return d.toISOString().split('T')[0];
  };

  const [form, setForm] = useState<BookingFormData>({
    first_name: '',
    reservation_date: getToday(), // Default to today
    reservation_slot: '',
  });
  const [formOutMsg, setFormOutMsg] = useState<string>('');
  const [formOutType, setFormOutType] = useState<'success' | 'danger'>('success');
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [fetchError, setFetchError] = useState<string>('');

  // NEW: Hide success message after a few seconds
  useEffect(() => {
    if (formOutMsg && formOutType === 'success') {
      const timer = setTimeout(() => setFormOutMsg(''), 3000);
      return () => clearTimeout(timer);
    }
  }, [formOutMsg, formOutType]);

  // Fetch bookings for the selected form date
  const fetchBookings = async (date: string) => {
    if (!date) {
      setBookings([]);
      return;
    }
    setLoading(true);
    setFetchError('');
    try {
      const url = `/api/bookings?date=${encodeURIComponent(date)}`;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to fetch bookings');
      }
      const data = await response.json();
      setBookings(data.reservations);
    } catch (err: any) {
      setFetchError(err.message || 'Unknown error');
      setBookings([]);
    } finally {
      setLoading(false);
    }
  };

  // Fetch bookings when form.reservation_date changes
  useEffect(() => {
    if (form.reservation_date) {
      fetchBookings(form.reservation_date);
    } else {
      setBookings([]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [form.reservation_date]);

  // On initial mount, ensure bookings for today's date are fetched
  useEffect(() => {
    fetchBookings(getToday());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormOutMsg('');
    try {
      // Use PUT and the new reservation endpoint
      const response = await fetch('/api/reservations', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 
          'X-CSRFToken': await getCSRFToken(), },
        body: JSON.stringify(form),
      });
      if (!response.ok) {
        const errData = await response.json();
        setFormOutType('danger');
        throw new Error(errData.detail || errData.error || 'Failed to submit reservation');
      }
      setFormOutType('success');
      setFormOutMsg('Reservation submitted!');
      // Do not reset form values
      // Refetch bookings for the selected date
      fetchBookings(form.reservation_date);
      // Message will auto-clear if successful
    } catch (err: any) {
      setFormOutType('danger');
      setFormOutMsg(`Error: ${err.message || 'Could not submit reservation.'}`);
    }
  };

  return (
    <div className="bg-light min-vh-100">
      <div className="container pt-4">
        <Navbar />
      </div>

      <div id="bookings" className="container pt-5">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6 main-content-bg">
            <div className="card shadow-sm" style={{ background: 'transparent', border: 'none' }}>
              <div className="card-body">
                <h3 className="card-title mb-4 text-center">Make a Reservation</h3>
                <form id="form" onSubmit={handleSubmit}>
                  {formOutMsg && (
                    <div
                      id="form-out-msg"
                      className={`w-100 mb-3 alert alert-${formOutType} text-center`}
                      role="alert"
                    >
                      {formOutMsg}
                    </div>
                  )}
                  <div className="form-group">
                    <label htmlFor="first_name">Name</label>
                    <input
                      type="text"
                      className="form-control"
                      id="first_name"
                      name="first_name"
                      value={form.first_name}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="form-group mt-3">
                    <label htmlFor="reservation_date">Reservation date</label>
                    <input
                      type="date"
                      className="form-control"
                      id="reservation_date"
                      name="reservation_date"
                      value={form.reservation_date}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="form-group mt-3">
                    <label htmlFor="reservation_slot">Reservation slot</label>
                    <select
                      className="form-control"
                      id="reservation_slot"
                      name="reservation_slot"
                      value={form.reservation_slot}
                      onChange={handleChange}
                      required
                    >
                      <option value="" disabled>Select a slot</option>
                      {slots.map(slot => (
                        <option key={slot} value={slot}>{slot}</option>
                      ))}
                    </select>
                  </div>
                  <div className="d-flex justify-content-center mt-4">
                    <button type="submit" className="btn btn-primary px-5">
                      Reserve
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div id="reservations-by-date" className="container pt-5">
        <div className="row justify-content-center">
          <div className="col-md-10 col-lg-8 main-content-bg">
            <div className="card shadow-sm" style={{ background: 'transparent', border: 'none' }}>
              <div className="card-body">
                <h3 className="card-title mb-4 text-center">
                  {form.reservation_date
                    ? `Bookings for ${form.reservation_date}`
                    : "Bookings by Date"}
                </h3>
                {fetchError && (
                  <div className="alert alert-danger text-center">{fetchError}</div>
                )}
                <div className="table-responsive">
                  <table className="table table-sm table-bordered table-hover">
                    <thead>
                      <tr>
                        <th>First Name</th>
                        <th>Date</th>
                        <th>Slot</th>
                      </tr>
                    </thead>
                    <tbody id="tableData">
                      {loading ? (
                        <tr>
                          <td colSpan={3} className="text-center">Loading...</td>
                        </tr>
                      ) : bookings.length === 0 ? (
                        <tr>
                          <td colSpan={3} className="text-center">No bookings yet.</td>
                        </tr>
                      ) : (
                        bookings.map((b, idx) => (
                          <tr key={idx}>
                            <td>{b.first_name}</td>
                            <td>{b.reservation_date}</td>
                            <td>{b.reservation_slot}</td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
