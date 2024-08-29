import React, { useEffect } from 'react';
import '../styles/About.css'; // Assuming you have a CSS file for styling

function About() {
    useEffect(() => {
        document.title = 'PM - About';
    }, []);
    return (
        <div className="about-container">
            <h1>PM - About</h1>
            <p>
                Welcome to <strong>Prime Math</strong>, an innovative platform designed for programmers who want to enhance their math skills. Our platform combines a dynamic leveling system with engaging courses and projects to help you advance your knowledge and expertise.
            </p>
            <h2>How It Works</h2>
            <ul>
                <li>
                    <strong>Courses:</strong> Start by visiting the <a href="/courses">Courses</a> page. Join a course, and once you complete it with a score of at least 60%, you'll unlock the next level of the course.
                </li>
                <li>
                    <strong>Projects:</strong> Within each course, you'll find various projects. Completing these projects will earn you points and contribute to your overall level progress.
                </li>
                <li>
                    <strong>Level System:</strong> The platform features a level system where your progress is tracked based on your course and project completion.
                </li>
                <li>
                    <strong>Teachers:</strong> Teachers are available to help you with your learning journey. Feel free to reach out to them for guidance and support.
                </li>
            </ul>
            <h2>Level Calculation Algorithm</h2>
            <p>
                The level calculation is based on your overall performance. Here’s a simple breakdown:
            </p>
            <ul>
                <li>
                    <strong>Points:</strong> You earn points for completing courses and projects. The more you achieve, the more points you gather.
                </li>
                <li>
                    <strong>Bonuses:</strong> You receive additional bonus points based on how well you complete your courses and projects. These bonuses contribute to your total progress score.
                </li>
                <li>
                    <strong>Level:</strong> Your level increases as your total progress score rises. As you earn more points and bonuses, you advance to higher levels.
                </li>
                <li>
                    <strong>Progress to Next Level:</strong> Your progress towards the next level is calculated based on how close you are to reaching the next milestone in the level system.
                </li>
            </ul>
            <h2>Profile Management</h2>
            <p>
                On your <a href="/profile">Profile</a> page, you can update your username, password, and email. You can also add your social media accounts to keep your profile up-to-date.
            </p>
            <h2>Rules and Guidelines</h2>
            <ul>
                <li>Ensure you complete each course with a minimum score of 60% to progress to the next course.</li>
                <li>Regularly update your profile to keep your information current.</li>
                <li>Reach out to teachers for assistance whenever needed.</li>
            </ul>
        </div>
    );
}

export default About;
