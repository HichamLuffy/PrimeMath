import { useState } from "react";
import api from "../api";
import { useNavigate, Link } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN, USER_NAME, USER_ROLE } from "../constants";
import "../styles/Form.css";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [email, setEmail] = useState("");
    const [role, setRole] = useState("student");
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});
    const navigate = useNavigate();

    const name = method === "login" ? "SIGN IN" : "Register";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();
        setErrors({});

        // Validate form inputs
        if (method === "register" && password !== confirmPassword) {
            setErrors({ confirmPassword: "Passwords do not match" });
            setLoading(false);
            return;
        }

        try {
            const requestData =
                method === "login"
                    ? { username, password }
                    : { username, password, email, role };

            const res = await api.post(route, requestData);

            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                localStorage.setItem(USER_NAME, res.data.username);
                localStorage.setItem(USER_ROLE, res.data.role);
                navigate(res.data.role === "teacher" ? "/teacher-dashboard" : "/");
            } else {
                navigate("/login");
            }
        } catch (error) {
            if (error.response && error.response.data) {
                // Handle specific error messages from the backend
                if (method === "login") {
                    // Handle login errors (e.g., invalid username or password)
                    const { username: usernameError, password: passwordError, detail } = error.response.data;
                    setErrors({
                        username: usernameError || (detail && !passwordError ? detail : undefined),
                        password: passwordError || (detail && !usernameError ? detail : undefined)
                    });
                } else {
                    // Handle registration errors
                    setErrors(error.response.data);
                }
            } else {
                alert(`Error: ${error.message}`);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{name}</h1>
            <input
                className={`form-input ${errors.username ? 'input-error' : ''}`}
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            {errors.username && <p className="error-message">{errors.username}</p>}

            {method === "register" && (
                <>
                    <input
                        className={`form-input ${errors.email ? 'input-error' : ''}`}
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                    />
                    {errors.email && <p className="error-message">{errors.email}</p>}

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
                className={`form-input ${errors.password ? 'input-error' : ''}`}
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            {errors.password && <p className="error-message">{errors.password}</p>}

            {method === "register" && (
                <input
                    className={`form-input ${errors.confirmPassword ? 'input-error' : ''}`}
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Confirm Password"
                />
            )}
            {errors.confirmPassword && <p className="error-message">{errors.confirmPassword}</p>}

            {loading && <div>Loading...</div>}
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
