import React, { useState, useEffect } from 'react';
import axios from '../api'; // Assuming you have an axios instance set up
import { fetchCurrentUser } from "../api";
import LoadingIndicator from "../components/LoadingIndicator";
import '../styles/Profile.css'; // Import the CSS file

const Profile = () => {
    const [userInfo, setUserInfo] = useState(null);
    const [editMode, setEditMode] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        age: '',
        current_courses: [],
        current_study: [],
        completed_courses: [],
        social_links: '',
        last_seen: ''
    });
    const [rank, setRank] = useState(null);

    useEffect(() => {
        document.title = `PM - Profile`;
        const fetchUserInfo = async () => {
            try {
                const data = await fetchCurrentUser();
                setUserInfo(data);
                setFormData({
                    username: data.username,
                    email: data.email,
                    age: data.age || '',
                    current_study: data.current_study || [],
                    completed_courses: data.completed_courses || [],
                    social_links: data.social_links || ''
                });

                // Fetch user rank
                const allUsers = await fetchUserList();
                const sortedUsers = allUsers.sort((a, b) => b.level - a.level);
                const userRank = sortedUsers.findIndex(user => user.username === data.username) + 1;
                setRank(userRank);
            } catch (error) {
                console.error("Error fetching user information!", error);
            }
        };

        fetchUserInfo();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        const updateData = { ...formData };
        if (!updateData.password) {
            delete updateData.password;
        }
        try {
            const { data } = await axios.put('/api/update-profile/', updateData);
            setUserInfo(data);
            setEditMode(false);
        } catch (error) {
            console.error("Error updating the profile!", error);
        }
    };

    return (
        <div className="profile-container">
            {userInfo ? (
                <div className="profile-content">
                    <h2 className="profile-header">{userInfo.username}'s Profile</h2>

                    {editMode ? (
                        <form onSubmit={handleFormSubmit} className="profile-form">
                            <div className="form-group">
                                <label>Username:</label>
                                <input
                                    type="text"
                                    name="username"
                                    value={formData.username}
                                    onChange={handleInputChange}
                                />
                            </div>
                            <div className="form-group">
                                <label>Email:</label>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleInputChange}
                                />
                            </div>
                            <div className="form-group">
                                <label>Password:</label>
                                <input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleInputChange}
                                />
                            </div>
                            <div className="form-group">
                                <label>Age:</label>
                                <input
                                    type="number"
                                    name="age"
                                    value={formData.age}
                                    onChange={handleInputChange}
                                />
                            </div>
                            <div className="form-group">
                                <label>Current Study:</label>
                                <input
                                    type="text"
                                    name="current_study"
                                    value={formData.current_study}
                                    onChange={handleInputChange}
                                />
                            </div>
                            <div className="form-group">
                                <label>Social Links:</label>
                                <input
                                    type="text"
                                    name="social_links"
                                    value={formData.social_links}
                                    onChange={handleInputChange}
                                />
                            </div>
                            <button type="submit" className="save-button">Save Changes</button>
                        </form>
                    ) : (
                        <div className="profile-details">
                            <div className="detail-item">
                                <strong>Username:</strong> {userInfo.username}
                            </div>
                            <div className="detail-item">
                                <strong>Role:</strong> {userInfo.role}
                            </div>
                            <div className="detail-item">
                                <strong>Email:</strong> {userInfo.email}
                            </div>
                            <div className="detail-item">
                                <strong>Age:</strong> {userInfo.age || 'N/A'}
                            </div>
                            <div className="detail-item">
                                <strong>Current Study:</strong> {userInfo.current_study}
                            </div>
                            <div className="detail-item">
                                <strong>Level:</strong> {userInfo.level}
                            <div className="level-bar">
                                <div className="level-bar-bg">
                                    <div 
                                        className="level-bar-fill" 
                                        style={{ width: `${userInfo.level_progress}%` }}
                                    ></div>
                                </div>
                                <p>{userInfo.level_progress.toFixed(2)}% to next level</p>
                            </div>
                            </div>
                            
                            <div className="detail-item">
                                <strong>Social Links:</strong> {userInfo.social_links}
                            </div>
                            <div className="detail-item">
                                <strong>Last Seen:</strong> {userInfo.last_seen}
                            </div>
                            <div className="detail-item">
                                <strong>Current Courses:</strong> 
                                <ul>
                                    {userInfo.current_courses.map(course => (
                                        <li key={course.id}>
                                            {course.name} - {course.completion_percentage}% completed
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div className="detail-item">
                                <strong>Progress to next level:</strong> {userInfo.level_progress}%
                            </div>
                            <button onClick={() => setEditMode(true)} className="edit-button">Edit Profile</button>
                        </div>
                    )}
                </div>
            ) : (
                <LoadingIndicator />
            )}
        </div>
    );
};

export default Profile;