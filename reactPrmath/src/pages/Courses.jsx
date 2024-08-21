import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import '../styles/Courses.css';

const Courses = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [userCourses, setUserCourses] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response = await api.get('/courses/');
                setCourses(response.data);
            } catch (error) {
                console.error('Error fetching courses:', error);
            } finally {
                setLoading(false);
            }
        };

        const fetchUserCourses = async () => {
            try {
                const response = await api.get('/api/current_user/');
                setUserCourses(response.data.profile.student_profile.current_courses || []);
            } catch (error) {
                console.error('Error fetching user courses:', error);
            }
        };

        fetchCourses();
        fetchUserCourses();
    }, []);

    const handleJoinCourse = async (courseId) => {
        try {
            const response = await api.post(`/courses/join/${courseId}/`);
            const updatedCourses = courses.map(course =>
                course.id === courseId
                    ? { ...course, is_active: true, number_of_students_in_course: course.number_of_students_in_course + 1 }
                    : course
            );
            setCourses(updatedCourses);
            setUserCourses([...userCourses, courseId]);
        } catch (error) {
            console.error('Error joining course:', error);
        }
    };

    const handleCourseClick = (courseId) => {
        navigate(`/courses/${courseId}`);
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <h1>List of Courses</h1>
            <ul>
                {courses.map((course) => (
                    <li key={course.id}>
                        <span
                            style={{ cursor: 'pointer', textDecoration: course.is_active ? 'underline' : 'none' }}
                            onClick={() => handleCourseClick(course.id)}
                        >
                            {course.name} - Active: {course.is_active ? "Yes" : "No"} - Students: {course.number_of_students_in_course}
                        </span>
                        {(!course.is_active) && (
                            <button onClick={() => handleJoinCourse(course.id)}>
                                Join
                            </button>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Courses;
