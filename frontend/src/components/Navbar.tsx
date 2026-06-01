import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import robotLogo from '../img/robot-logo.png';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import '../css/style.css';
import { getAppVersion } from '../components/appVersionCache';
import { getCurrentUser } from '../components/currentUserCache';

export const Navbar: React.FC = () => {
  const [appVersion, setAppVersion] = useState<string>('…');
  const [currentUser, setCurrentUser] = useState<string>('…');

  useEffect(() => {
    let mounted = true;
    getAppVersion()
      .then(version => { if (mounted) setAppVersion(version); })
      .catch(() => { if (mounted) setAppVersion('unknown'); });
    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    let mounted = true;
    getCurrentUser()
      .then(user => { if (mounted) setCurrentUser(user); })
      .catch(() => { if (mounted) setCurrentUser('unknown'); });
    return () => { mounted = false; };
  }, []);

  return (
    <nav
      className="navbar navbar-expand-lg navbar-light mb-4"
      style={{ backgroundColor: '#D8BFD8', borderRadius: '1rem' }}
    >
      <div className="container-fluid">
        <Link
          className="navbar-brand d-flex align-items-center"
          to="/"
          style={{ color: '#0056b3' }}
        >
          <img
            src={robotLogo}
            alt="Logo"
            style={{ height: 40, width: 'auto', marginRight: 10 }}
          />
          <span className="font-weight-bold text-white">Booking System</span>
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div className="navbar-nav ms-auto">
            <Link className="nav-link text-white" to="/">
              Home
            </Link>
            <Link className="nav-link text-white" to="/reservations">
              Bookings
            </Link>
            <Link className="nav-link text-white" to="/api/docs/" target="_blank" rel="noopener noreferrer">
              Swagger
            </Link>
            <a className="nav-link text-white" target="_blank" rel="noopener noreferrer" href="/admin">
              Django-Admin
            </a>
            <a
              href="https://github.com/conorheffron/booking-sys"
              id="appVersion"
              style={{ marginLeft: '1.5em', textDecoration: 'none' }}
              target="_blank"
              rel="noopener noreferrer"
            >
              Version: {appVersion}
            </a>
            <div className="dropdown" style={{ marginLeft: '1.5em' }}>
              <button
                className="btn btn-sm dropdown-toggle"
                type="button"
                id="userDropdown"
                data-bs-toggle="dropdown"
                aria-expanded="false"
                style={{ backgroundColor: '#9370DB', color: '#fff', border: 'none' }}
              >
                User: {currentUser}
              </button>
              <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                <li>
                  <span className="dropdown-item-text" id="currentUserId">
                    {currentUser}
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};
