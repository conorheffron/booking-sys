import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

export const ErrorPage: React.FC = () => {
  const location = useLocation();

  return (
    <div className="bg-light min-vh-100">
      <div className="container pt-4">
        <Navbar />
      </div>
      <div className="container pt-5">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6">
            <div className="card text-center shadow-sm">
              <div className="card-body">
                <h1 className="display-4 text-danger mb-4">Page Not Found</h1>
                <p className="lead">
                  The requested URL <code>{location.pathname}</code> was not found on this server.
                </p>
                <Link to="/" className="btn btn-primary mt-3">
                  Return Home
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
