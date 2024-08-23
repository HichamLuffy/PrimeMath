// Form.jsx
import { useState } from "react";
import api from "../api";
import { useNavigate, Link } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN, USER_NAME, USER_ROLE } from "../constants";
import "../styles/Form.css";
import LoadingIndicator from "./LoadingIndicator";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState(""); // Add email state
    const [role, setRole] = useState("student"); // Add role state
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "SIGN IN" : "Register";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const requestData =
                method === "login"
                    ? { username, password }
                    : { username, password, email, role }; // Include email and role if it's registration

            console.log("Submitting: ", requestData);

            const res = await api.post(route, requestData);
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                localStorage.setItem(USER_NAME, res.data.username);
                localStorage.setItem(USER_ROLE, res.data.role);
                if (res.data.role === "teacher") {
                    navigate("/teacher-dashboard");
                } else {
                    navigate("/");
                }
            } else {
                navigate("/login");
            }
        } catch (error) {
            alert(`Error: ${error.response ? error.response.data : error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{name}</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            {method === "register" && (
                <>
                    <input
                        className="form-input"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                    />
                    <select
                        className="form-input"
                        value={role}
                        onChange={(e) => setRole(e.target.value)}
                    >
                        <option value="student">Student</option>
                        <option value="teacher">Teacher</option>
                    </select>
                </>
            )}
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            {loading && <LoadingIndicator />}
            <button className="form-button" type="submit">
                {name}
            </button>
            {method === "login" ? (
                <p>
                    Don't have an account? <Link to="/register">Click here to register</Link>
                </p>
            ) : (
                <p>
                    Already have an account? <Link to="/login">Click here to login</Link>
                </p>
            )}
        </form>
    );
}

export default Form;