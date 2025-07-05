import React, { useState, useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

interface Reservation {
  id: number;
  first_name: string;
  reservation_date: string;
  reservation_slot: string;
}

export const ReservationsPage: React.FC = () => {
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReservations = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/bookings', {
        method: 'GET',
      });
      if (!response.ok) {
        throw new Error('Failed to fetch reservations');
      }
      const data = await response.json();
      setReservations(data.reservations);
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReservations();
  }, []);

  return (
    <div className="bg-light min-vh-100">
      <div className="container pt-4">
        <Navbar />
      </div>
      <div className="container pt-5">
        <div className="row justify-content-center">
          <div className="col-md-12 col-lg-10 main-content-bg">
            <div className="card shadow-sm">
              <div className="card-body" style={{ background: 'transparent' }}>
                <h3 className="card-title mb-4 text-center">All Upcoming Reservations</h3>
                {loading ? (
                  <div className="text-center">Loading...</div>
                ) : error ? (
                  <div className="alert alert-danger text-center">{error}</div>
                ) : (
                  <div className="table-responsive">
                    <table className="table table-sm table-bordered table-hover align-middle">
                      <thead className="thead-light">
                        <tr>
                          <th>#</th>
                          <th>Name</th>
                          <th>Booking Date</th>
                          <th>Booking Time</th>
                          <th>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {reservations.length === 0 && (
                          <tr>
                            <td colSpan={5} className="text-center">
                              No reservations found.
                            </td>
                          </tr>
                        )}
                        {reservations.map(item => (
                          <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.first_name}</td>
                            <td>{item.reservation_date}</td>
                            <td>{item.reservation_slot}</td>
                            <td>
                              <a
                                href={`/reservations/edit/${item.id}`}
                                className="btn btn-sm btn-warning"
                              >
                                Edit
                              </a>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
                <div className="text-center mt-4">
                  <button
                    type="button"
                    className="btn btn-primary"
                    onClick={fetchReservations}
                    disabled={loading}
                  >
                    Refresh
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
