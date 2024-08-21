import React, { useState, useEffect } from 'react';
import api from '../api';
import '../styles/Courses.css';

const Courses = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [userCourses, setUserCourses] = useState([]);

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
                const response = await api.get('/api/user-courses/');
                setUserCourses(response.data);
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
            // Update the course in the local state
            const updatedCourses = courses.map(course => 
                course.id === courseId 
                    ? { ...course, is_active: true, number_of_students_in_course: course.number_of_students_in_course + 1 }
                    : course
            );
            setCourses(updatedCourses);
            // Add the course to the user's joined courses
            setUserCourses([...userCourses, courseId]);
        } catch (error) {
            console.error('Error joining course:', error);
        }
    };

    const handleCourseClick = (courseId, courseName) => {
        history.push(`/courses/${courseId}/${courseName}`);
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <h1>List of Courses</h1>
            <ul>
                {courses.map((course) => (
                    <li key={course.id}>
                        <span 
                            style={{ cursor: course.is_active ? 'pointer' : 'default', textDecoration: course.is_active ? 'underline' : 'none' }}
                            onClick={course.is_active ? () => handleCourseClick(course.id, course.name) : undefined}
                        >
                            {course.name} - Active: {course.is_active ? "Yes" : "No"} - Students: {course.number_of_students_in_course}
                        </span>
                        {(!userCourses.includes(course.id)) && (
                            <button onClick={() => handleJoinCourse(course.id)} disabled={course.is_active}>
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