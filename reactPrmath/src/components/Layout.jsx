import React, { useState, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Link } from 'react-router-dom';

import '../styles/Layout.css';

function Layout() {
    const location = useLocation();
    const [sidebarWidth, setSidebarWidth] = useState('10%');
    const [activeLink, setActiveLink] = useState(location.pathname);

    useEffect(() => {
        if (location.pathname === '/') {
            setSidebarWidth('20%');
        } else {
            setSidebarWidth('10%');
        }
        setActiveLink(location.pathname);
    }, [location.pathname])

    return (
        <div className="layout-container" style={{ '--sidebar-width': sidebarWidth }}>
            <div className="sidebar">
                <h1 className="logo">PRIME MATH</h1>
                <nav>
                    <ul>
                        <li className={activeLink === '/' ? 'active' : ''}><Link to="/">Menu</Link></li>
                        <li className={activeLink === '/courses' ? 'active' : ''}><Link to="/courses">Courses</Link></li>
                        <li className={activeLink === '/dashboard' ? 'active' : ''}><Link to="/dashboard">Dashboard</Link></li>
                        <li className={activeLink === '/profile' ? 'active' : ''}><Link to="/profile">Profile</Link></li>
                        <li className={activeLink === '/about' ? 'active' : ''}><Link to="/about">About</Link></li>
                    </ul>
                </nav>
            </div>
            <div className="main-content">
                <Outlet />
            </div>
        </div>
    );
}

export default Layout;
