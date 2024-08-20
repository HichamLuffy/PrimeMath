import React, { useState, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Link } from 'react-router-dom';

import '../styles/Layout.css';

function Layout() {
    const location = useLocation();
    const [sidebarWidth, setSidebarWidth] = useState('10%');

    useEffect(() => {
        // Adjust the sidebar width based on the current route
        if (location.pathname === '/') {
            setSidebarWidth('20%');
        } else {
            setSidebarWidth('10%');
        }
    }, [location.pathname]);

    return (
        <div className="layout-container" style={{ '--sidebar-width': sidebarWidth }}>
            <div className="sidebar">
                <h1 className="logo">PRIME MATH</h1>
                <nav>
                    <ul>
                        <li><Link to="/">Menu</Link></li>
                        <li><Link to="/courses">Courses</Link></li>
                        <li><Link to="/dashboard">Dashboard</Link></li>
                        <li><Link to="/profile">Profile</Link></li>
                        <li><Link to="/about">About</Link></li>
                    </ul>
                </nav>
                <div className="upcoming-events">
                    <h2>Upcoming Events</h2>
                    <ul>
                        <li>Discord night 20:30 11/8</li>
                        <li>ALGORITHM session 9:00 11/10</li>
                    </ul>
                </div>
            </div>
            <div className="main-content">
                <Outlet />
            </div>
        </div>
    );
}

export default Layout;
