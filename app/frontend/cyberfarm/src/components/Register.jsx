import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Register() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    phone: "",
    role: "farmer",
    latitude: "",
    longitude: "",
  });
  const navigate = useNavigate();

  // Use Geolocation API to get latitude and longitude
  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setFormData((prevData) => ({
          ...prevData,
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        }));
      },
      (error) => {
        console.error("Error fetching geolocation:", error);
        alert("Unable to fetch your location. Please enable location services.");
      }
    );
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("https://cyberfarm.onrender.com/api/register", formData);
      navigate("/login");
    } catch (error) {
      console.error("Registration failed:", error);
      alert("Failed to register. Please try again.");
    }
  };

  return (
    <div style={{ backgroundColor: "#d4edda", minHeight: "100vh" }} className="flex items-center justify-center">
      <div style={{ backgroundColor: "#ffffff", padding: "32px", borderRadius: "8px", boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)" }} className="w-full max-w-md">
        <h2 style={{ color: "#6fbf73" }} className="text-2xl font-bold mb-6">Register</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            onChange={handleChange}
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
            name="password"
            placeholder="Password"
            onChange={handleChange}
            style={{
              width: "100%",
              padding: "12px",
              border: "1px solid #f5e6da",
              borderRadius: "8px",
              marginBottom: "16px",
            }}
          />
          <input
            type="text"
            name="phone"
            placeholder="Phone"
            onChange={handleChange}
            style={{
              width: "100%",
              padding: "12px",
              border: "1px solid #f5e6da",
              borderRadius: "8px",
              marginBottom: "16px",
            }}
          />
          <select
            name="role"
            onChange={handleChange}
            style={{
              width: "100%",
              padding: "12px",
              border: "1px solid #f5e6da",
              borderRadius: "8px",
              marginBottom: "16px",
            }}
          >
            <option value="farmer">Farmer</option>
            <option value="cold truck">Cold Truck</option>
            <option value="storage">Storage</option>
          </select>
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
            Register
          </button>
        </form>
        <p style={{ marginTop: "16px", textAlign: "center", color: "#d2b48c" }}>
          Already have an account?{" "}
          <a href="/login" style={{ color: "#6fbf73", textDecoration: "underline" }}>
            Login
          </a>
        </p>
      </div>
    </div>
  );
}

export default Register;