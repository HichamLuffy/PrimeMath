// ProjectDetail.jsx

import React, { useState, useEffect } from 'react';
import api from '../api';
import { useParams } from 'react-router-dom';
import '../styles/ProjectsDetails.css';

const ProjectDetail = () => {
    const { projectId } = useParams();
    const [project, setProject] = useState(null);
    const [loading, setLoading] = useState(true);
    const [selectedAnswers, setSelectedAnswers] = useState({});

    useEffect(() => {
        const fetchProject = async () => {
            try {
                const response = await api.get(`/projects/${projectId}/`);
                setProject(response.data);
            } catch (error) {
                console.error('Error fetching project details:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchProject();
    }, [projectId]);

    const handleAnswerChange = (taskId, answer) => {
        setSelectedAnswers(prev => ({
            ...prev,
            [taskId]: answer
        }));
    };

    const handleSubmit = async (taskId) => {
        const chosen_answer = selectedAnswers[taskId];
        if (!chosen_answer) return;

        try {
            const response = await api.post(`/tasks/submit/${taskId}/`, { chosen_answer });
            if (response.data.is_completed) {
                alert('Correct! The task is marked as completed.');
                setProject(prevProject => ({
                    ...prevProject,
                    tasks: prevProject.tasks.map(task =>
                        task.id === taskId ? { ...task, is_completed: true } : task
                    )
                }));
            } else {
                alert('Incorrect. Try again!');
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (!project) return <div>Project not found</div>;

    return (
        <div className="project-detail-layout">
            <div className="project-detail-header">
                <h1 className="project-title">{project.title}</h1>
                <p className="project-description">{project.description}</p>
                <p className="project-description">Difficulty: {project.difficulty_level}</p>
            </div>
            <div className="task-list">
                {project.tasks.map(task => (
                    <div key={task.id} className="task-item">
                        <h3 className="task-title">{task.title}</h3>
                        <div className="task-details">
                            <span>Difficulty: {task.difficulty_level}</span>
                            <span>Status: {task.is_completed ? 'Completed' : 'Incomplete'}</span>
                        </div>
                        <p className="task-question">{task.question}</p>
                        <ul className="task-options">
                            {Object.entries(task.options).map(([key, value]) => (
                                <li key={key} className="task-option">
                                    <label className="task-option-label">
                                        <input
                                            type="radio"
                                            name={`task-${task.id}`}
                                            value={key}
                                            onChange={() => handleAnswerChange(task.id, key)}
                                            disabled={task.is_completed}
                                            className="task-option-input"
                                        />
                                        {key}: {value}
                                    </label>
                                </li>
                            ))}
                        </ul>
                        {!task.is_completed && (
                            <button className="task-submit-button" onClick={() => handleSubmit(task.id)}>
                                Submit Answer
                            </button>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ProjectDetail;