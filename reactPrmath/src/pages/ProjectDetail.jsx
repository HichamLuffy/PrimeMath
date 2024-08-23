import React, { useState, useEffect } from 'react';
import api from '../api';
import { useParams } from 'react-router-dom';

const ProjectDetail = () => {
    const { projectId } = useParams();
    const [project, setProject] = useState(null);
    const [loading, setLoading] = useState(true);

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

    if (loading) return <div>Loading...</div>;

    if (!project) return <div>Project not found</div>;

    return (
        <div>
            
            <h1>{project.title}</h1>
            <p>{project.description}</p>
            <h2>Tasks</h2>
            <ul>
                {project.tasks.map(task => (
                    <li key={task.id}>
                        <h3>{task.title}</h3>
                        <p>{task.description}</p>
                        <p>{task.question}</p>
                        <ul>
                            {Object.entries(task.options).map(([key, value]) => (
                                <li key={key}>{key}: {value}</li>
                            ))}
                        </ul>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ProjectDetail;