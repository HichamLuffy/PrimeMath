import React, { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";

function TeacherProfileForm() {
    const [age, setAge] = useState("");
    const [status, setStatus] = useState("");
    const [teachingExperience, setTeachingExperience] = useState("");
    const [subjectsOfExpertise, setSubjectsOfExpertise] = useState("");
    const [certifications, setCertifications] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const profileData = {
            age,
            status,
            teaching_experience: teachingExperience,
            subjects_of_expertise: subjectsOfExpertise.split(","), // Assuming subjects are comma-separated
            certifications
        };

        try {
            await api.post("/api/teacher-profile/", profileData);
            alert("Teacher profile updated successfully!");
            navigate("/"); // Redirect to home after successful update
        } catch (error) {
            console.error("Error updating teacher profile:", error);
            alert("There was an error updating your profile.");
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>Teacher Profile</h1>
            <input
                className="form-input"
                type="number"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                placeholder="Age"
            />
            <input
                className="form-input"
                type="text"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                placeholder="Status (e.g., Professor, Lecturer)"
            />
            <input
                className="form-input"
                type="number"
                value={teachingExperience}
                onChange={(e) => setTeachingExperience(e.target.value)}
                placeholder="Years of Teaching Experience"
            />
            <input
                className="form-input"
                type="text"
                value={subjectsOfExpertise}
                onChange={(e) => setSubjectsOfExpertise(e.target.value)}
                placeholder="Subjects of Expertise (comma-separated)"
            />
            <textarea
                className="form-input"
                value={certifications}
                onChange={(e) => setCertifications(e.target.value)}
                placeholder="Certifications"
            ></textarea>
            <button className="form-button" type="submit">
                Update Profile
            </button>
        </form>
    );
}

export default TeacherProfileForm;
