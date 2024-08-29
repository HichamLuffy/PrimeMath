import React, { useState, useEffect } from 'react';
import api from '../api';
import { useParams } from 'react-router-dom';
import '../styles/ProjectsDetails.css';
import ReactMarkdown from 'react-markdown';
import LoadingIndicator from "../components/LoadingIndicator";

const ProjectDetail = () => {
    const { projectId } = useParams();
    const [project, setProject] = useState(null);
    const [loading, setLoading] = useState(true);
    const [selectedAnswers, setSelectedAnswers] = useState({});
    const [feedback, setFeedback] = useState({}); // State to store feedback messages for each task

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
                setFeedback(prevFeedback => ({
                    ...prevFeedback,
                    [taskId]: 'Correct! The task is marked as completed.'
                }));
                setProject(prevProject => ({
                    ...prevProject,
                    tasks: prevProject.tasks.map(task =>
                        task.id === taskId ? { ...task, is_completed: true } : task
                    )
                }));
            } else {
                setFeedback(prevFeedback => ({
                    ...prevFeedback,
                    [taskId]: 'Incorrect. Try again!'
                }));
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
            setFeedback(prevFeedback => ({
                ...prevFeedback,
                [taskId]: 'An error occurred. Please try again later.'
            }));
        }
    };

    if (loading) return <LoadingIndicator />;
    if (!project) return (
        <div className="notfound-project">
            <div className="content">
                <h2>Project Not Found</h2>
                <p>Sorry, we couldn't find the project you were looking for.</p>
                <p>or you don't have access to it yet </p>
                <button onClick={() => navigate('/')} className="home-button">
                    Go to Home
                </button>
            </div>
        </div>
    );

    return (
        <div className="project-detail-layout">
            <div className="project-detail-header">
                <h1 className="project-title">{project.title}</h1>
                <p className="project-description"><ReactMarkdown>{project.description}</ReactMarkdown></p>
                <p className="project-completion">Completion: {project.completion_percentage}%</p>
            </div>
            <div className="task-list">
                {project.tasks.map(task => (
                    <div key={task.id} className={`task-item ${task.is_completed ? 'completed' : ''}`}>
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
                            <>
                                <button className="task-submit-button" onClick={() => handleSubmit(task.id)}>
                                    Submit Answer
                                </button>
                                {feedback[task.id] && (
                                    <p className={`feedback-message ${feedback[task.id].includes('Correct') ? 'correct' : 'incorrect'}`}>
                                        {feedback[task.id]}
                                    </p>
                                )}
                            </>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ProjectDetail;
