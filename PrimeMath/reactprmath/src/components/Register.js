import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Register = ({ onRegister }) => {
    const [form, setForm] = useState({
        username: '',
        email: '',
        password1: '',
        password2: '',
        role: '',
        age: '',
        current_study: '',
        status: '',
        teaching_experience: '',
        certifications: ''
    });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/register/', form);
            alert(response.data.success);
            onRegister();
        } catch (error) {
            alert(error.response.data.error);
        }
    };

    return (
        <div>
        <h2>Register Page</h2>
        <form onSubmit={handleSubmit}>
            {/* Add form fields for all required inputs */}
            <input type="text" name="username" onChange={handleChange} placeholder="Username" />
            <input type="email" name="email" onChange={handleChange} placeholder="Email" />
            <input type="password" name="password1" onChange={handleChange} placeholder="Password" />
            <input type="password" name="password2" onChange={handleChange} placeholder="Confirm Password" />
            <select name="role" onChange={handleChange}>
                <option value="">Select Role</option>
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
            </select>
            {/* Add fields for role-specific data */}
            <button type="submit">Register</button>
        </form>
        <Link to="/login">Go to Login</Link>
      </div>
    );
};

export default Register;