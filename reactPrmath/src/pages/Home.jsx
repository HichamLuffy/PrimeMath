import React, { useState, useEffect } from "react";
import { fetchCurrentUser, fetchDiscordEvents } from "../api";
import '../styles/Home.css';
import { useNavigate } from 'react-router-dom';
import avatarImage from '../styles/images/username-icon.png';
import LoadingIndicator from '../components/LoadingIndicator';
import { CSSTransition, TransitionGroup } from 'react-transition-group';

function Home() {
    const [userName, setUserName] = useState("");
    const [loading, setLoading] = useState(true);
    const [role, setRole] = useState("");
    const [currentCourses, setCurrentCourses] = useState([]);
    const [completedCourses, setCompletedCourses] = useState([]);
    const [currentProjects, setCurrentProjects] = useState([]);
    const [events, setEvents] = useState([]);
    const [level, setLevel] = useState(1);
    const [levelProgress, setLevelProgress] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        document.title = "Home Page";
        const getUser = async () => {
            try {
                const user = await fetchCurrentUser();
                setUserName(user.username);
                setRole(user.role);
                const inProgressCourses = user.current_courses || [];
                const completedCourses = inProgressCourses.filter(course => course.completion_percentage === 100);
                const ongoingCourses = inProgressCourses.filter(course => course.completion_percentage < 100);
                setCurrentCourses(ongoingCourses);
                setCompletedCourses(completedCourses);
                setCurrentProjects(user.current_projects || []);
                if (user.role === 'student') {
                    setLevel(user.level || 0);
                    setLevelProgress(user.level_progress || 0);
                }

                const discordEvents = await fetchDiscordEvents();
                setEvents(discordEvents);

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

    const handleEventClick = (eventLink) => {
        window.open(eventLink, "_blank");
    };

    if (loading) {
        return <LoadingIndicator />;
    }

    return (
        <div className="home-container">
            <div className="user-info">
                <div className="user-header">
                    <img src={avatarImage} className="avatar" alt="User Avatar" />
                    <div className="user-details">
                        <h2>{userName}</h2>
                        <p>You are: {role}</p>
                        {role === 'student' && (
                            <>
                                <p>Level: {level} - {levelProgress.toFixed(2)}%</p>
                                <div className="level-bar">
                                    <div className="level-bar-bg">
                                        <div className="level-bar-fill" style={{ width: `${levelProgress}%` }}>
                                            <span className="level-progress-text">
                                                {/* {levelProgress.toFixed(2)}% */}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </div>
            <div className="courses-container">
                <div className="current-courses">
                    <h3>Current Courses:</h3>
                    <TransitionGroup component="ul">
                        {currentCourses.map((course) => (
                            <CSSTransition key={course.id} timeout={500} classNames="course-item">
                                <li 
                                    key={course.id} 
                                    className="course-item"
                                    onClick={() => handleCourseClick(course.id)}
                                >
                                    {course.name} - {course.completion_percentage.toFixed(2)}%
                                </li>
                            </CSSTransition>
                        ))}
                    </TransitionGroup>
                </div>
                <div className="completed-courses">
                    <h3>Completed Courses:</h3>
                    <TransitionGroup component="ul">
                        {completedCourses.map((course) => (
                            <CSSTransition key={course.id} timeout={500} classNames="course-item">
                                <li key={course.id} className="course-item">
                                    {course.name} - {course.completion_percentage.toFixed(2)}%
                                </li>
                            </CSSTransition>
                        ))}
                    </TransitionGroup>
                </div>
            </div>
        </div>
    );
}

export default Home;
