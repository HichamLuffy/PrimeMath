import Form from "../components/Form";
import React, { useEffect } from 'react';
function Register() {
    useEffect(() => {
        document.title = `PM - Register`;
    }, []);
    return <Form route="/api/user/register/" method="register" />
}

export default Register