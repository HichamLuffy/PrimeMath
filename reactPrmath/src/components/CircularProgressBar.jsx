import React from "react";
import '../styles/Home.css';

const CircularProgressBar = ({ level, progress }) => {
    const strokeDasharray = `${progress}, 100`;

    return (
        <div className="circular-progress">
            <svg className="circular-svg">
                <circle className="circle-bg" cx="50" cy="50" r="45" />
                <circle
                    className="circle-progress"
                    cx="50"
                    cy="50"
                    r="45"
                    style={{ strokeDasharray }}
                />
            </svg>
            <div className="level-number">
                <span>Lv {level}</span>
            </div>
        </div>
    );
};

export default CircularProgressBar;
