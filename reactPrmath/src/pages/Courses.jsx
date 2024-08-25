import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import '../styles/Courses.css';
import LoadingIndicator from "../components/LoadingIndicator";
import userIcon from '../styles/images/username-icon.png';

const Courses = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [userCourses, setUserCourses] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response = await api.get('/courses/');
                const userResponse = await api.get('/api/current_user/');
                const userCourses = userResponse.data.current_courses.map(course => course.id);
                
                const updatedCourses = response.data.map(course => ({
                    ...course,
                    is_active: userCourses.includes(course.id) || course.is_active
                }));

                setCourses(updatedCourses);
                setUserCourses(userCourses);
            } catch (error) {
                console.error('Error fetching courses:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchCourses();
    }, []);

    const handleJoinCourse = async (courseId) => {
        try {
            await api.post(`/courses/join/${courseId}/`);
            const updatedCourses = courses.map(course =>
                course.id === courseId
                    ? { ...course, is_active: true, number_of_students_in_course: course.number_of_students_in_course + 1 }
                    : course
            );
            setCourses(updatedCourses);

            // Update the user's joined courses list
            setUserCourses([...userCourses, courseId]);
        } catch (error) {
            console.error('Error joining course:', error);
        }
    };

    const handleCourseClick = (courseId) => {
        const joinedCourse = userCourses.includes(courseId);
        if (joinedCourse) {
            navigate(`/courses/${courseId}/`);
        }
    };

    if (loading) return <LoadingIndicator />;

    return (
        <div className="courses-container">
            <h1 className="courses-title">Courses</h1>
            <div className="courses-list">
                {courses.map((course) => {
                    const hasJoined = userCourses.includes(course.id);

                    return (
                        <div
                            key={course.id}
                            className={`course-card ${course.is_active ? 'active' : 'inactive'}`}
                            onClick={() => course.is_active && handleCourseClick(course.id)}
                            style={{ cursor: course.is_active ? 'pointer' : 'default', opacity: course.is_active ? 1 : 0.5 }}
                        >
                            <div className="course-info">
                                <h2>{course.name}</h2>
                                <p>Status: <span className={`status ${course.is_active ? 'active-status' : 'inactive-status'}`}>{course.is_active ? "Active" : "Inactive"}</span></p>
                                <p>Score : {course.score}</p>
                                <p>
                                    <img src={userIcon} alt="Number of students" className="student-icon" />
                                    {course.number_of_students_in_course} Students
                                </p>
                            </div>
                            {!hasJoined ? (
                                <button onClick={(e) => { 
                                    e.stopPropagation(); 
                                    handleJoinCourse(course.id); 
                                }} className="join-button">
                                    Join
                                </button>
                            ) : (
                                <button className="join-button joined" disabled>
                                    Joined
                                </button>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Courses;
