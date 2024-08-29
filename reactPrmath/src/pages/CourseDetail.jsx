import React, { useState, useEffect } from 'react';
import api from '../api';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import LoadingIndicator from "../components/LoadingIndicator";
import '../styles/CourseDetails.css';

const CourseDetail = () => {
    const { courseId } = useParams();
    const [course, setCourse] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCourseData = async () => {
            try {
                // Fetch course details including projects
                const courseResponse = await api.get(`/courses/${courseId}/`);
                setCourse(courseResponse.data);
            } catch (error) {
                console.error('Error fetching course details:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchCourseData();
    }, [courseId]);
    
    useEffect(() => {
        if (course) {
            document.title = `PM - ${course.name}`;
        }
    }, [course]);

    if (loading) return <LoadingIndicator />;

    if (!course) return <div>Course not found</div>;

    return (
        <div className="course-detail-layout">
            <header className="course-detail-header">
                <h1 className="course-title">{course.name}</h1>
                <div className="course-detail-info">
                    <div className="course-detail-info-item">
                        <p><strong>Active:</strong> {course.is_active ? "Yes" : "No"}</p>
                    </div>
                    <div className="course-detail-info-item">
                        <p><strong>Status:</strong> {course.is_completed ? "Completed" : "Not completed"}</p>
                    </div>
                    <div className="course-detail-info-item">
                        <p><strong>Enrolled Students:</strong> {course.number_of_students_in_course}</p>
                    </div>
                    <div className="course-detail-info-item">
                        <p><strong>Completion Percentage:</strong> {course.completion_percentage.toFixed(2)}%</p>
                    </div>
                </div>
                <div className="course-description">
                    <ReactMarkdown>{course.description}</ReactMarkdown>
                </div>
            </header>

            <section className="projects-section">
                <h2 className="projects-title">Projects</h2>
                {course.projects.length > 0 ? (
                    <ul className="projects-list">
                        {course.projects.map(project => (
                            <li key={project.id} className="project-item">
                                <Link to={`/projects/${project.id}`}>
                                    {project.title}
                                    <p className="project-completion">Completion: {project.completion_percentage.toFixed(2)}%</p>
                                </Link>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p style={{ textAlign: 'center', color: '#A0D995', fontSize: '1.1em' }}>
                        No projects available for this course yet.
                    </p>
                )}
            </section>
        </div>
    );
};

export default CourseDetail;
