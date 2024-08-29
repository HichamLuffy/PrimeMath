import React, { useState, useEffect } from 'react';
import { fetchUserList } from '../api';
import '../styles/Dashboard.css';
import { useNavigate } from 'react-router-dom';
import LoadingIndicator from "../components/LoadingIndicator";

function Dashboard() {
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();

    const handleUsernameClick = (username) => {
        navigate(`/users/${username}`);
    };

    useEffect(() => {
        document.title = `PM - Dashboard`;
        const getUsers = async () => {
            try {
                const data = await fetchUserList();
                console.log("Fetched Users:", data);  // Debugging

                // Sort users by level in descending order
                const sortedUsers = data.sort((a, b) => b.level - a.level);

                // Add ranking to users
                const rankedUsers = sortedUsers.map((user, index) => ({
                    ...user,
                    rank: index + 1,
                }));

                setUsers(rankedUsers);
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        };
    
        getUsers();
    }, []);

    if (users.length === 0) {
        return <LoadingIndicator />;
    }

    return (
        <div className="dashboard">
            <h1>Dashboard Page</h1>
            <ul className="user-list">
                {users.map(user => (
                    <li 
                        key={user.username} 
                        className={`user-card ${user.online ? "online" : "offline"}`}
                        onClick={() => handleUsernameClick(user.username)}
                    >
                        <span className="rank">#{user.rank}</span>
                        <span className="username">{user.username}</span>
                        <span className="level">Level: {user.level}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Dashboard;
