import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/LandingPage.css';

const LandingPage = () => {
    return (
        <div className="landing-page">
            <div className="video-background">
                <video autoPlay loop muted>
                    <source src="../styles/videos/video.mp4" type="video/mp4" />
                </video>
            </div>
            <div className="features-section">
                <h2>Website Features</h2>
                <div className="features-cards">
                    <div className="card">
                        <h3>Feature 1</h3>
                        <p>Explanation of the first feature.</p>
                    </div>
                    <div className="card">
                        <h3>Feature 2</h3>
                        <p>Explanation of the second feature.</p>
                    </div>
                    <div className="card">
                        <h3>Feature 3</h3>
                        <p>Explanation of the third feature.</p>
                    </div>
                </div>
            </div>
            <footer className="footer">
                <p>&copy; 2024 My Awesome Website. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default LandingPage;