import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchUserProfile } from '../api';
import '../styles/UserProfile.css';
import LoadingIndicator from '../components/LoadingIndicator';

function UserProfile() {
    const { username } = useParams();
    const [userProfile, setUserProfile] = useState(null);

    useEffect(() => {
        document.title = `PM - Profile`;
        const getUserProfile = async () => {
            try {
                console.log(`Fetching profile data for username: ${username}`);  // Debugging
                const data = await fetchUserProfile(username);
                console.log("Fetched profile data:", data);  // Debugging
                setUserProfile(data);
            } catch (error) {
                console.error("Error fetching user profile:", error);
            }
        };

        getUserProfile();
    }, [username]);

    
    if (!userProfile) {
        return <LoadingIndicator />;
    }


    return (
        <div className="user-profile">
            <h1>{userProfile.username}'s Profile</h1>
            <p><strong>Role:</strong> {userProfile.role}</p>
            <p><strong>Age:</strong> {userProfile.age}</p>
            <p><strong>Status:</strong> {userProfile.status}</p>
            
            <p><strong>Last Seen:</strong> {userProfile.last_seen}</p>
            <p><strong>Social Links:</strong> {userProfile.social_links}</p>
            {userProfile.role === 'student' && (
                <>
                    <p><strong>Level:</strong> {userProfile.level}</p>
                    <p><strong>Current Study:</strong> {userProfile.current_study}</p>
                    <p><strong>Completed Courses:</strong> {userProfile.completed_courses.join(', ')}</p>
                </>
            )}
            {userProfile.role === 'teacher' && (
                <>
                    <p><strong>Certifications:</strong> {userProfile.certifications}</p>
                    <p><strong>Teaching Experience:</strong> {userProfile.teaching_experience}</p>
                    <p><strong>Courses Taught:</strong> {userProfile.courses_taught.map(course => course.name).join(', ')}</p>
                    <p><strong>Projects Created:</strong> {userProfile.projects_created.map(project => project.title).join(', ')}</p>
                </>
            )}
        </div>
    );
}

export default UserProfile;