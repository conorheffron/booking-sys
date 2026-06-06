import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { getCSRFToken } from '../components/Utils';
import { loginUser } from '../components/auth';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fromPath = location.state?.from?.pathname || '/reservations';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      const csrfToken = await getCSRFToken();
      await loginUser(username, password, csrfToken);
      navigate(fromPath, { replace: true });
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-light min-vh-100">
      <div className="container pt-4">
        <Navbar />
      </div>
      <div className="container pt-5">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-4 main-content-bg">
            <div className="card shadow-sm" style={{ background: 'transparent', border: 'none' }}>
              <div className="card-body">
                <h3 className="card-title mb-4 text-center">Login</h3>
                {error && <div className="alert alert-danger text-center">{error}</div>}
                <form onSubmit={handleSubmit}>
                  <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                      id="username"
                      className="form-control"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      required
                    />
                  </div>
                  <div className="form-group mt-3">
                    <label htmlFor="password">Password</label>
                    <input
                      id="password"
                      type="password"
                      className="form-control"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                  </div>
                  <div className="d-flex justify-content-center mt-4">
                    <button type="submit" className="btn btn-primary px-5" disabled={isSubmitting}>
                      {isSubmitting ? 'Signing in…' : 'Login'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
