import React, { useEffect, useState } from "react";
import { Navbar } from "../components/Navbar";
import "bootstrap/dist/css/bootstrap.min.css";

interface Reservation {
  id: number;
  first_name: string;
  reservation_date: string;
  reservation_slot: string;
}

export const ReservationsPage: React.FC = () => {
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [refreshing, setRefreshing] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const fetchReservations = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch("/api/bookings?date=");
      if (!response.ok) {
        throw new Error("Failed to fetch reservations");
      }
      const data = await response.json();
      setReservations(data.reservations || []);
    } catch (err: any) {
      setError(err.message || "Failed to fetch reservations");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchReservations();
  }, []);

  const handleRefresh = () => {
    setRefreshing(true);
    fetchReservations();
  };

  // Add delete by booking id functionality
  const handleDelete = async (id: number) => {
    // if (!window.confirm("Delete this reservation?")) return;
    setDeletingId(id);
    setError("");
    try {
      const response = await fetch(`/api/bookingsById/${id}`, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error("Failed to delete reservation");
      }
      setReservations(reservations.filter(r => r.id !== id));
    } catch (err: any) {
      setError(err.message || "Failed to delete reservation");
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="bg-light min-vh-100">
      <div className="container pt-4">
        <Navbar />
      </div>
      <div className="container pt-5">
        <div className="row justify-content-center">
          <div className="col-md-10 col-lg-8 main-content-bg">
            <div className="card shadow-sm" style={{ background: 'transparent', border: 'none' }}>
              <div className="card-body">
                <h3 className="card-title mb-4 text-center">All Upcoming Reservations</h3>
                {error && (
                  <div className="alert alert-danger text-center">{error}</div>
                )}
                <div className="table-responsive">
                  <table className="table table-sm table-bordered table-hover">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Booking Date</th>
                        <th>Booking Time</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {loading ? (
                        <tr>
                          <td colSpan={5} className="text-center">Loading...</td>
                        </tr>
                      ) : reservations.length === 0 ? (
                        <tr>
                          <td colSpan={5} className="text-center">No reservations found.</td>
                        </tr>
                      ) : (
                        reservations.map((r, idx) => (
                          <tr key={r.id}>
                            <td>{idx + 1}</td>
                            <td>{r.first_name}</td>
                            <td>{r.reservation_date}</td>
                            <td>{r.reservation_slot}</td>
                            <td>
                              <a
                                href={`/reservations/edit/${r.id}`}
                                className="btn btn-sm btn-outline-secondary me-2"
                                role="link"
                                aria-label={`Edit reservation ${r.id}`}
                              >
                                Edit
                              </a>
                              <button
                                className="btn btn-sm btn-link p-0"
                                title="Delete"
                                aria-label={`Delete reservation ${r.id}`}
                                style={{ color: "#dc3545", verticalAlign: "middle" }}
                                onClick={() => handleDelete(r.id)}
                                disabled={deletingId === r.id}
                              >
                                {/* Trash SVG icon */}
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width="18"
                                  height="18"
                                  fill="currentColor"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M5.5 5.5a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0v-6a.5.5 0 0 1 .5-.5zm2.5.5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0v-6zm2 .5a.5.5 0 0 1 .5-.5.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0v-6zm-7-2A.5.5 0 0 1 3 4V3a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1a.5.5 0 0 1 .5.5H15a.5.5 0 0 1 0 1h-1.5V14A2 2 0 0 1 11 16H5a2 2 0 0 1-2-2V5.5H1.5a.5.5 0 0 1 0-1H3A.5.5 0 0 1 3.5 4zM5 3h4a1 1 0 0 1 1 1v1H4V4a1 1 0 0 1 1-1zm6 2v9a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5h8z"/>
                                </svg>
                              </button>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
                {/* Refresh button at the bottom and centered */}
                <div className="d-flex justify-content-center mt-4">
                  <button
                    className="btn btn-outline-primary"
                    onClick={handleRefresh}
                    disabled={loading || refreshing}
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
