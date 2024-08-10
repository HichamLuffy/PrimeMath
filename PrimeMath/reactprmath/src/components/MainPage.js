import React from 'react';

const MainPage = ({ user, onLogout }) => {
    return (
        <div>
            <h1>Welcome, {user.username}</h1>
            <p>Role: {user.role}</p>
            <button onClick={onLogout}>Logout</button>
        </div>
    );
};

export default MainPage;