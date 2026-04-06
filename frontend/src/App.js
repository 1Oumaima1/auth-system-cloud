// src/App.js
import { AnimatePresence } from "framer-motion";
import { Route, BrowserRouter as Router, Routes, useLocation } from "react-router-dom";

// Import de tes composants
import AdminDashboard from "./comportement/AdminDashboard";
import Login from "./comportement/Login";
import Signup from "./comportement/Signup";
import UserDashboard from "./comportement/UserDashboard";

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/user" element={<UserDashboard />} />
        <Route path="/" element={<Login />} />
      </Routes>
    </AnimatePresence>
  );
}

function App() {
  return (
    <div className="min-h-screen">
      <Router>
        <AnimatedRoutes />
      </Router>
    </div>
  );
}

export default App;
