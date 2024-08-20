import React, { useState, useEffect } from 'react';
import api from '../api';
import '../styles/Courses.css';

const Courses = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response = await api.get('/courses/');
                setCourses(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching courses:', error);
            }
        };

        fetchCourses();
    }, []);

    const handleJoinCourse = async (courseId) => {
        try {
            const courseToUpdate = courses.find(course => course.id === courseId);
            if (courseToUpdate) {
                await api.post(`/courses/join/${courseId}/`);

                const updatedCourses = courses.map(course => 
                    course.id === courseId 
                        ? { ...course, is_active: true, number_of_students_in_course: course.number_of_students_in_course + 1 } 
                        : course
                );
                setCourses(updatedCourses);

                if (courseToUpdate.is_active === false) {
                    history.push(`/course/${courseId}/${courseToUpdate.name}`);
                }
            }
        } catch (error) {
            console.error('Error joining course:', error);
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <h1>List of Courses</h1>
            <ul>
                {courses.map((course) => (
                    <li key={course.id}>
                        <span>{course.name} - Active: {course.is_active ? "Yes" : "No"} - Students: {course.number_of_students_in_course}</span>
                        <button onClick={() => handleJoinCourse(course.id)} disabled={course.is_active}>
                            {course.is_active ? "Joined" : "Join"}
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Courses;
