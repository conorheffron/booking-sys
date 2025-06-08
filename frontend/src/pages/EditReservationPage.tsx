import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

interface Reservation {
  id: number;
  first_name: string;
  reservation_date: string;
  reservation_slot: string;
}

export const EditReservationPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [name, setName] = useState('');
  const [date, setDate] = useState('');
  const [slot, setSlot] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  // Hardcoded slots
  const slots = [
    '09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM',
    '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM',
    '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM',
    '06:30 PM', '07:00 PM'
  ];

  // Fetch reservation by ID
  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(`/api/bookingsById/${id}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch reservation');
        return res.json();
      })
      .then((data: Reservation) => {
        setName(data.first_name);
        setDate(data.reservation_date);
        setSlot(data.reservation_slot);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg('');
    try {
      const response = await fetch(`/api/bookingsById/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          first_name: name,
          reservation_date: date,
          reservation_slot: slot,
        }),
      });
      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || data.error || 'Failed to update reservation');
        // Stay on edit view, don't change form values
        return;
      }
      setSuccessMsg('Reservation updated successfully!');
      setTimeout(() => navigate('/reservations'), 1200); // Redirect after success
    } catch (err: any) {
      setError(err.message || 'Failed to update reservation');
      // Stay on edit view, don't change form values
    }
  };

  return (
    <div className="bg-light min-vh-100">
      <div className="container pt-4">
        <Navbar />
      </div>
      <div className="container pt-5">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6 main-content-bg">
            <div className="card shadow-sm" style={{ background: 'transparent', border: 'none' }}>
              <div className="card-body">
                <h3 className="card-title mb-4 text-center">
                  Edit Reservation {id ? `#${id}` : ''}
                </h3>
                {loading ? (
                  <div className="text-center">Loading...</div>
                ) : error ? (
                  <div className="alert alert-danger text-center">{error}</div>
                ) : null}
                {!loading && (
                  <form onSubmit={handleSave}>
                    {successMsg && (
                      <div className="alert alert-success text-center">{successMsg}</div>
                    )}
                    <div className="form-group">
                      <label htmlFor="name">Name</label>
                      <input
                        className="form-control"
                        id="name"
                        value={name}
                        onChange={e => setName(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label htmlFor="date">Date</label>
                      <input
                        className="form-control"
                        id="date"
                        type="date"
                        value={date}
                        onChange={e => setDate(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label htmlFor="slot">Slot</label>
                      <select
                        className="form-control"
                        id="slot"
                        value={slot}
                        onChange={e => setSlot(e.target.value)}
                        required
                      >
                        <option value="" disabled>Select a slot</option>
                        {slots.map(option => (
                          <option key={option} value={option}>{option}</option>
                        ))}
                      </select>
                    </div>
                    <button type="submit" className="btn btn-primary btn-block">Save</button>
                  </form>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
