import Form from "../components/Form";
import React, { useEffect } from 'react';
function Login() {
    useEffect(() => {
        document.title = `PM - Login`;
    }, []);
    return <Form route="/api/token/" method="login" />
}

export default Login