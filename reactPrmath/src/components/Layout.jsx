import React, { useState, useEffect } from 'react';
import { Outlet, useLocation, Link, useNavigate } from 'react-router-dom';
import { FaBars, FaTimes, FaHome, FaBook, FaChartLine, FaUser, FaInfoCircle, FaSignOutAlt } from 'react-icons/fa'; // Added FaSignOutAlt icon
import '../styles/Layout.css';

function Layout() {
    const location = useLocation();
    const navigate = useNavigate();
    const [sidebarWidth, setSidebarWidth] = useState('3%');
    const [activeLink, setActiveLink] = useState(location.pathname);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    useEffect(() => {
        setSidebarWidth(isSidebarOpen ? '15%' : '5%');
        setActiveLink(location.pathname);
    }, [location.pathname, isSidebarOpen]);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    return (
        <div className="layout-container" style={{ '--sidebar-width': sidebarWidth }}>
            <div className={`sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
                <button className="toggle-btn" onClick={toggleSidebar}>
                    {isSidebarOpen ? <FaTimes /> : <FaBars />}
                </button>
                <h1 className="logo">{isSidebarOpen ? 'PRIME MATH' : 'PM'}</h1>
                <nav>
                    <ul>
                        <li className={activeLink === '/' ? 'active' : ''}>
                            <Link to="/"><FaHome />{isSidebarOpen && 'Menu'}</Link>
                        </li>
                        <li className={activeLink === '/courses' ? 'active' : ''}>
                            <Link to="/courses"><FaBook />{isSidebarOpen && 'Courses'}</Link>
                        </li>
                        <li className={activeLink === '/dashboard' ? 'active' : ''}>
                            <Link to="/dashboard"><FaChartLine />{isSidebarOpen && 'Dashboard'}</Link>
                        </li>
                        <li className={activeLink === '/profile' ? 'active' : ''}>
                            <Link to="/profile"><FaUser />{isSidebarOpen && 'Profile'}</Link>
                        </li>
                        <li className={activeLink === '/about' ? 'active' : ''}>
                            <Link to="/about"><FaInfoCircle />{isSidebarOpen && 'About'}</Link>
                        </li>
                    </ul>
                </nav>
                <button className="logout-btn" onClick={handleLogout}>
                    <FaSignOutAlt />{isSidebarOpen && 'Logout'}
                </button>
            </div>
            <div className="main-content">
                <Outlet />
            </div>
        </div>
    );
}

export default Layout;
