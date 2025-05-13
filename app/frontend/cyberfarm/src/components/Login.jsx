import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import axios from "axios";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/login", {
        username,
        password,
      });
      const user = response.data.user;

      // Store username in localStorage
      localStorage.setItem("username", user.username);

      login(); // Call the login function from AuthContext
      navigate("/"); // Redirect to the home page
    } catch (error) {
      console.error("Login failed:", error);
      alert("Invalid username or password.");
    }
  };

  return (
    <div style={{ backgroundColor: "#d4edda", minHeight: "100vh" }} className="flex items-center justify-center">
      <div style={{ backgroundColor: "#ffffff", padding: "32px", borderRadius: "8px", boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)" }} className="w-full max-w-md">
        <h2 style={{ color: "#6fbf73" }} className="text-2xl font-bold mb-6">Login</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              border: "1px solid #f5e6da",
              borderRadius: "8px",
              marginBottom: "16px",
            }}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              border: "1px solid #f5e6da",
              borderRadius: "8px",
              marginBottom: "16px",
            }}
          />
          <button
            type="submit"
            style={{
              width: "100%",
              backgroundColor: "#6fbf73",
              color: "#ffffff",
              padding: "12px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
            }}
          >
            Login
          </button>
        </form>
        <p style={{ marginTop: "16px", textAlign: "center", color: "#d2b48c" }}>
          Don't have an account?{" "}
          <a href="/register" style={{ color: "#6fbf73", textDecoration: "underline" }}>
            Sign Up
          </a>
        </p>
      </div>
    </div>
  );
}

export default Login;