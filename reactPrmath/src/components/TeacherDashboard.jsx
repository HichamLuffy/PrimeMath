// TeacherDashboard.jsx
import React, { useEffect, useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
// import "../styles/TeacherDashboard.css";

function TeacherDashboard() {
    const [teacherProfile, setTeacherProfile] = useState(null);
    const [students, setStudents] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchTeacherData = async () => {
            try {
                const res = await api.get("/teacher-dashboard/");
                setTeacherProfile(res.data.profile);
                setStudents(res.data.students);
            } catch (error) {
                console.error("Error fetching teacher data:", error);
                if (error.response.status === 401) {
                    navigate("/login");
                }
            }
        };

        fetchTeacherData();
    }, [navigate]);

    const handleEditProfile = () => {
        navigate("/edit-teacher-profile");
    };

    return (
        <div className="teacher-dashboard">
            <h1>Teacher Dashboard</h1>
            {teacherProfile && (
                <div className="profile-section">
                    <h2>Your Profile</h2>
                    <p>Experience: {teacherProfile.teaching_experience}</p>
                    <p>Certifications: {teacherProfile.certifications}</p>
                    <button onClick={handleEditProfile}>Edit Profile</button>
                </div>
            )}
            <div className="students-section">
                <h2>Your Students</h2>
                <ul>
                    {students.map((student) => (
                        <li key={student.id}>{student.name}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default TeacherDashboard;
