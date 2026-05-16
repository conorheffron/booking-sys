import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { getCSRFToken } from '../components/Utils';
import { logoutUser } from '../components/auth';

export const LogoutPage: React.FC = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');

  useEffect(() => {
    let mounted = true;
    const runLogout = async () => {
      try {
        const csrfToken = await getCSRFToken();
        await logoutUser(csrfToken);
        if (mounted) navigate('/', { replace: true });
      } catch (err: any) {
        if (mounted) setError(err.message || 'Logout failed');
      }
    };
    runLogout();
    return () => {
      mounted = false;
    };
  }, [navigate]);

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
                <h3 className="card-title mb-4 text-center">Logout</h3>
                {error ? (
                  <div className="alert alert-danger text-center">{error}</div>
                ) : (
                  <div className="text-center">Signing out…</div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
