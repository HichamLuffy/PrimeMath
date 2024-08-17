import React, { useEffect } from 'react';
import '../styles/NotFound.css';

function NotFound() {
    useEffect(() => {
        const torch = document.querySelector('.torch');
        document.addEventListener('mousemove', (e) => {
            torch.style.left = `${e.pageX}px`;
            torch.style.top = `${e.pageY}px`;
        });
    }, []);

    return (
        <div className="notfound-page">
            <div className="text">
                <h1>404</h1>
                <h2>Uh, Ohh</h2>
                <h3>Sorry we can't find what you are looking for 'cuz it's so dark in here</h3>
            </div>
            <div className="torch"></div>
        </div>
    );
}

export default NotFound;
