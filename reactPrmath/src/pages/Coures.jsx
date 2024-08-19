import React, { useState, useEffect } from 'react';

const Coures = () => {
    const [courses, setCourses] = useState([]);

    useEffect(() => {
        // Fetch the list of courses from the database
        const fetchCourses = async () => {
            try {
                const response = await fetch('/api/courses'); // Replace with your API endpoint
                const data = await response.json();
                setCourses(data);
            } catch (error) {
                console.error('Error fetching courses:', error);
            }
        };

        fetchCourses();
    }, []);

    return (
        <div>
            <h1>List of Courses</h1>
            <ul>
                {courses.map((course) => (
                    <li key={course.id}>{course.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default Coures;