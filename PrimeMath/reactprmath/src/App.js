import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import MainPage from './components/MainPage';

const App = () => {
    // const [user, setUser] = useState(null);
    // const [page, setPage] = useState('login');

    // const handleRegister = () => {
    //     setPage('login');
    // };

    // const handleLogin = (userData) => {
    //     setUser(userData);
    //     setPage('main');
    // };

    // const handleLogout = () => {
    //     setUser(null);
    //     setPage('login');
    // };

    return (
      <Router>
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/main" element={<MainPage />} />
        </Routes>
      </Router>
    );
};

export default App;
