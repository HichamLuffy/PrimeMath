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
    const [points, setPoints] = useState(0);
    const [currentCourses, setCurrentCourses] = useState([]);
    const [currentProjects, setCurrentProjects] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        document.title = "Home Page";
        const getUser = async () => {
            try {
                const user = await fetchCurrentUser();
                setUserName(user.username);
                setRole(user.role);
                setPoints(user.points);
                setCurrentCourses(user.current_courses || []);
                setCurrentProjects(user.current_projects || []);
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
        navigate('/login');
    };

    const handleCourseClick = (courseId) => {
        navigate(`/courses/${courseId}`);
    };

    if (loading) {
        return <LoadingIndicator />;
    }

    return (
        <div className="home-container">
            <div className="main-content">
                <div className="user-info">
                    <div className="user-header">
                        <img src={avatarImage} className="avatar" alt="User Avatar" />
                        <div className="user-details">
                            <h2>{userName}</h2>
                            <p>You are: {role}</p>
                            <p>Points: {points}</p>
                        </div>
                    </div>
                    <div className="current-course">
                        <h3>Current Courses:</h3>
                        <ul>
                            {currentCourses.map((course) => (
                                <li 
                                key={course.id} 
                                className="course-item"
                                onClick={() => handleCourseClick(course.id)}
                                >
                                    {course.name}
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div className="current-projects">
                        <h3>Current Projects:</h3>
                        <ul>
                            {currentProjects.map((project) => (
                                <li key={project.id} className="project-item">{project.title}</li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className="skills-chart">
                    <h3>Skills</h3>
                    {/* Include a radar chart or similar visualization here */}
                </div>
                <button onClick={handleLogout} className="logout-button">Logout</button>
            </div>
        </div>
    );
}

export default Home;
