import React, { useState, useEffect } from 'react';
import api from '../api';
import { useParams, Link } from 'react-router-dom';

const CourseDetail = () => {
    const { courseId } = useParams();
    const [course, setCourse] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCourse = async () => {
            try {
                const response = await api.get(`/courses/${courseId}/`);
                setCourse(response.data);
            } catch (error) {
                console.error('Error fetching course details:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchCourse();
    }, [courseId]);

    if (loading) return <div>Loading...</div>;

    if (!course) return <div>Course not found</div>;

    return (
        <div>
            <h1>{course.name}</h1>
            <p>{course.description}</p>
            <p>Active: {course.is_active ? "Yes" : "No"}</p>
            <p>Students Enrolled: {course.number_of_students_in_course}</p>
            <p>Created On: {new Date(course.date_created).toLocaleDateString()}</p>
            <p>Last Updated: {new Date(course.date_updated).toLocaleDateString()}</p>
            <h2>Projects</h2>
            <ul>
                {course.projects.map(project => (
                    <li key={project.id}>
                        <Link to={`/projects/${project.id}`}>{project.title}</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CourseDetail;