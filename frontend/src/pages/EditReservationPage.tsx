import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import { getCSRFToken, getSlots } from '../components/Utils';

interface Reservation {
  id: number;
  first_name: string;
  reservation_date: string;
  reservation_slot: string;
}

const slots = getSlots(); // Should return slots in "HH:MM AM/PM" format

// Convert any "13:30" or "16:30" (24-hour) to "01:30 PM" or "04:30 PM" (12-hour)
function to12Hour(slot: string): string {
  slot = slot.trim();
  // Already in AM/PM format
  if (slot.match(/(AM|PM)$/i)) {
    return slot
      .replace(/\s+am$/i, " AM")
      .replace(/\s+pm$/i, " PM")
      .replace(/^(\d):/, "0$1:"); // pad hour if needed
  }
  // 24-hour format
  const match = slot.match(/^(\d{1,2}):(\d{2})$/);
  if (!match) return slot;
  let [_, h, m] = match;
  let hour = parseInt(h, 10);
  const minute = m;
  const ampm = hour >= 12 ? "PM" : "AM";
  if (hour === 0) hour = 12;
  if (hour > 12) hour -= 12;
  const hourStr = hour < 10 ? "0" + hour : "" + hour;
  return `${hourStr}:${minute} ${ampm}`;
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
        // Normalize slot to match the dropdown values
        const normalized = to12Hour(data.reservation_slot);
        if (slots.includes(normalized)) {
          setSlot(normalized);
        } else {
          // Try to find a slot with same hour/minute (fallback)
          const alt = slots.find(s => to12Hour(s) === normalized);
          setSlot(alt || slots[0] || '');
        }
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
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': await getCSRFToken(),
        },
        body: JSON.stringify({
          first_name: name,
          reservation_date: date,
          reservation_slot: slot,
        }),
      });
      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || data.error || 'Failed to update reservation');
        return;
      }
      setSuccessMsg('Reservation updated successfully!');
      setTimeout(() => navigate('/reservations'), 1200);
    } catch (err: any) {
      setError(err.message || 'Failed to update reservation');
    }
  };

  const handleCancel = (e: React.MouseEvent) => {
    e.preventDefault();
    navigate('/reservations');
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
                    <div className="form-group mt-3">
                      <label htmlFor="date">Reservation Date</label>
                      <input
                        className="form-control"
                        id="date"
                        type="date"
                        value={date}
                        onChange={e => setDate(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group mt-3">
                      <label htmlFor="slot">Reservation Slot</label>
                      <select
                        className="form-control"
                        id="slot"
                        value={slot}
                        onChange={e => setSlot(e.target.value)}
                        required
                      >
                        <option value="" disabled>Select a slot</option>
                        {slots.map(s => (
                          <option key={s} value={s}>{s}</option>
                        ))}
                      </select>
                    </div>
                    <div className="d-flex justify-content-between mt-4">
                      <button type="submit" className="btn btn-primary">
                        Save
                      </button>
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={handleCancel}
                      >
                        Cancel
                      </button>
                    </div>
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
