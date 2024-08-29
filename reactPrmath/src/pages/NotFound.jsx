import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/NotFound.css';

function NotFound() {
    const [torchPosition, setTorchPosition] = useState({ x: 0, y: 0 });
    const navigate = useNavigate();

    useEffect(() => {
        document.title = `PM - Page Not Found`;
        const handleMouseMove = (e) => {
            setTorchPosition({ x: e.pageX, y: e.pageY });
        };
        document.addEventListener('mousemove', handleMouseMove);
        return () => document.removeEventListener('mousemove', handleMouseMove);
    }, []);

    return (
        <div className="notfound-container">
            {/* <div className="torch" style={{ left: `${torchPosition.x}px`, top: `${torchPosition.y}px` }}></div> */}
            <div className="content">
                <h1>404</h1>
                <h2>Page Not Found</h2>
                <p>Sorry, we couldn't find the page you were looking for.</p>
                <button onClick={() => navigate('/')} className="home-button">
                    Go to Home
                </button>
            </div>
        </div>
    );
}

export default NotFound;
