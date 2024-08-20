import React, { useState, useEffect } from "react";
import { fetchCurrentUser } from "../api";
import '../styles/Home.css';
import { Link, useNavigate } from 'react-router-dom';
import avatarImage from '../styles/images/username-icon.png';
import LoadingIndicator from '../components/LoadingIndicator';

function Home() {
    const [userName, setUserName] = useState("");
    const [loading, setLoading] = useState(true);
    const [role, setRole] = useState("");
    const navigate = useNavigate(); // Ensure useNavigate is called here
    const currentCourse = 'Trigonometry';
    const currentProjects = [
        'Understanding Basic Trigonometric Functions',
        'Solving Right Triangles',
    ];

    useEffect(() => {
        document.title = "Home Page";
        const getUser = async () => {
            try {
                const user = await fetchCurrentUser();
                setUserName(user.username);
                setRole(user.profile.role);
            } catch (error) {
                console.error("Failed to fetch user:", error);
            } finally {
                setLoading(false);
            }
        };

        getUser();
    }, []);

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login'); // Ensure navigate is called here
    };

    if (loading) {
        return <LoadingIndicator />;
    }

    return (
        <div className="home-container">
            {/* Sidebar */}
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
                <div className="user-info">
                    <div className="user-heade">
                        <img src={avatarImage} className="avatar" alt="User Avatar" />
                        <div className="user-details">
                            <h2>{userName}</h2>
                            <p>You are: {role}</p>
                            <p> 5 - 10%</p>
                            <p>Points: 50</p>
                        </div>
                    </div>
                    <div className="current-cour">
                        <h3>Current Course: {currentCourse}</h3>
                        <ul>
                            {currentProjects.map((project, index) => (
                                <li key={index}>{project}</li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className="skills-chart">
                    <h3>Skills</h3>
                {/* Include a radar chart or similar visualization here */}
                </div>
                {loading && <LoadingIndicator />}
                <button onClick={handleLogout} className="logout-button">Logout</button>
            </div>
        </div>
    );
}

export default Home;