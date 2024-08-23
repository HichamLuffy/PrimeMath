import react from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import Courses from "./pages/Courses"
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import About from './pages/about';
import Layout from "./components/Layout";
import CourseDetail from "./pages/CourseDetail"
import TeacherProfileForm from "./components/TeacherProfileForm"
import TeacherDashboard from "./components/TeacherDashboard"
import ProjectDetail from "./pages/ProjectDetail"

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}


function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Wrap the / route with Layout */}
        <Route element={<Layout />}>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
          <Route path="/home" element={<Home />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/courses/:courseId" element={<CourseDetail />} />
          <Route path="/projects/:projectId" component={ProjectDetail} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/about" element={<About />} />
        </Route>
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="/teacher-profile-form" element={<TeacherProfileForm />} />
        <Route path="*" element={<NotFound />} />
        {/* Protected Routes */}
        <Route
            path="dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route
            path="teacher-dashboard"
            element={
              <ProtectedRoute>
                <TeacherDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="edit-teacher-profile"
            element={
              <ProtectedRoute>
                <TeacherProfileForm />
              </ProtectedRoute>
            }
          />
      </Routes>
    </BrowserRouter>
  );
}

export default App