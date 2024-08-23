// TeacherProfileForm.jsx
import React, { useState, useEffect } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
// import "../styles/TeacherProfileForm.css";

function TeacherProfileForm() {
    const [teachingExperience, setTeachingExperience] = useState("");
    const [subjectsOfExpertise, setSubjectsOfExpertise] = useState("");
    const [certifications, setCertifications] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfileData = async () => {
            try {
                const res = await api.get("/api/current_user/");
                const profile = res.data;
                if (profile.role !== 'teacher') {
                    alert("You are not authorized to access this page.");
                    navigate("/");
                    return;
                }
                setTeachingExperience(profile.teaching_experience || "");
                setSubjectsOfExpertise(profile.subjects_of_expertise ? profile.subjects_of_expertise.join(", ") : "");
                setCertifications(profile.certifications || "");
            } catch (error) {
                console.error("Error fetching profile data:", error);
                if (error.response.status === 401) {
                    navigate("/login");
                }
            }
        };

        fetchProfileData();
    }, [navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const profileData = {
            teaching_experience: teachingExperience,
            subjects_of_expertise: subjectsOfExpertise.split(",").map(subject => subject.trim()), // Split and trim subjects
            certifications
        };

        try {
            await api.put("/edit-teacher-profile/", profileData);
            alert("Teacher profile updated successfully!");
            navigate("/teacher-dashboard"); // Redirect to teacher dashboard after successful update
        } catch (error) {
            console.error("Error updating teacher profile:", error);
            alert("There was an error updating your profile.");
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>Edit Teacher Profile</h1>
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