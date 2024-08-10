import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Login = ({ onLogin }) => {
    const [form, setForm] = useState({
        username: '',
        password: ''
    });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/login/', form);
            alert('Login successful');
            onLogin(response.data);
        } catch (error) {
            alert(error.response.data.error);
        }
    };

    return (
        <div>
        <h2>Login Page</h2>
        <form onSubmit={handleSubmit}>
            <input type="text" name="username" onChange={handleChange} placeholder="Username" />
            <input type="password" name="password" onChange={handleChange} placeholder="Password" />
            <button type="submit">Login</button>
            <Link to="/register">Go to Register</Link>
        </form>
      </div>
        
    );
};

export default Login;