import React, { useState, useEffect } from 'react';
import { fetchUserList } from '../api';
import '../styles/Dashboard.css';

function Dashboard() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const getUsers = async () => {
            try {
                const data = await fetchUserList();
                setUsers(data);
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        };

        getUsers();
    }, []);

    return (
        <div className="dashboard">
            <h1>Dashboard Page</h1>
            <ul className="user-list">
                {users.map(user => (
                    <li key={user.username} className={user.online ? "online" : "offline"}>
                        {user.username} - Score: {user.score}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Dashboard;
