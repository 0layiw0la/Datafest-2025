import React, { useState, useEffect } from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

axios.defaults.withCredentials = true;

// Fix Leaflet marker icon issue
import markerIconPng from "leaflet/dist/images/marker-icon.png";
import markerShadowPng from "leaflet/dist/images/marker-shadow.png";

const customIcon = L.icon({
  iconUrl: markerIconPng,
  shadowUrl: markerShadowPng,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

// Component to adjust the map bounds
const FitBounds = ({ userLocation, results }) => {
  const map = useMap();

  useEffect(() => {
    if (results.length > 0 || userLocation) {
      const bounds = L.latLngBounds(
        results.map((result) => [parseFloat(result.latitude), parseFloat(result.longitude)])
      );

      // Include the user's location in the bounds
      bounds.extend(userLocation);

      map.fitBounds(bounds, { padding: [50, 50] }); // Add padding for better visibility
    }
  }, [results, userLocation, map]);

  return null;
};

function Home() {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]); // Search results
  const [userLocation, setUserLocation] = useState([0, 0]); // Current user's location
  const [isLocationLoaded, setIsLocationLoaded] = useState(false); // Loading state for location

  // Fetch current user's location
  useEffect(() => {
    const fetchLocation = async () => {
      try {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const location = [position.coords.latitude, position.coords.longitude];
            console.log("User Location:", location); // Debugging
            setUserLocation(location);
            setIsLocationLoaded(true); // Mark location as loaded
          },
          (error) => {
            console.error("Error fetching user location:", error);
            // Fallback to a default location (e.g., New York City)
            setUserLocation([40.7128, -74.006]);
            setIsLocationLoaded(true); // Mark location as loaded
          }
        );
      } catch (error) {
        console.error("Error fetching location:", error);
      }
    };

    fetchLocation();
  }, []);

  // Handle search and fetch results
  const handleSearch = async (e) => {
    e.preventDefault();
    const username = localStorage.getItem("username"); // Retrieve username from localStorage
    if (!username) {
      alert("You must be logged in to perform a search.");
      return;
    }

    try {
      const response = await axios.post("https://cyberfarm.onrender.com/api/home", {
        username, // Send username with the request
        search_role: search,
      });
      console.log("Search Results:", response.data.nearest_users); // Debugging
      setResults(response.data.nearest_users); // Update results

      // Scroll to the results section
      const resultsSection = document.getElementById("results-section");
      if (resultsSection) {
        resultsSection.scrollIntoView({ behavior: "smooth" });
      }
    } catch (error) {
      console.error("Error fetching search results:", error);
      alert("Failed to fetch search results. Please try again.");
    }
  };

  return (
    <div style={{ backgroundColor: "#d4edda", minHeight: "100vh" }} className="flex flex-col items-center">
      {/* Header */}
      <header className="w-full py-4">
        <div className="container ml-16 flex justify-start items-center px-4">
          <h1 style={{ fontSize: "4rem", fontWeight: "bold", color: "#6fbf73" }}>CyberFarm</h1>
        </div>
      </header>

      {/* Search Section */}
      <div className="mt-8 w-full max-w-2xl px-4">
        <form onSubmit={handleSearch} className="flex items-center">
          <input
            type="text"
            placeholder="Search for a role or service (e.g., Farmer, Cold Truck, Storage, Delivery)"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              flexGrow: 1,
              padding: "12px",
              border: "1px solid #f5e6da",
              borderRadius: "8px 0 0 8px",
              backgroundColor: "#ffffff",
              outline: "none",
            }}
          />
          <button
            type="submit"
            style={{
              backgroundColor: "#6fbf73",
              color: "#ffffff",
              padding: "12px 24px",
              borderRadius: "0 8px 8px 0",
              border: "none",
              cursor: "pointer",
            }}
          >
            Search
          </button>
        </form>
      </div>

      {/* Map Section */}
      <div className="mt-12 w-[90%] md:w-full mx-auto md:mx-1 max-w-4xl px-14 md:px-4">
        {isLocationLoaded ? (
          <MapContainer center={userLocation} zoom={13} style={{ height: "400px", width: "100%" }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {/* Fit map bounds to markers */}
            <FitBounds userLocation={userLocation} results={results} />
            {/* Current User's Location */}
            <Marker position={userLocation} icon={customIcon}>
              <Popup>Your Location</Popup>
            </Marker>
            {/* Search Results */}
            {results.map((result, index) => (
              <Marker
                key={index}
                position={[parseFloat(result.latitude), parseFloat(result.longitude)]}
                icon={customIcon}
              >
                <Popup>
                  <strong>{result.username}</strong>
                  <br />
                  Phone: {result.phone}
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        ) : (
          <p>Loading map...</p>
        )}
      </div>

      {/* Results Section */}
      <div id="results-section" className="mt-14 w-full px-4 mb-8">
        <h2 style={{ color: "#6fbf73", fontWeight: "bold", marginBottom: "16px", textAlign: "center", fontSize: "2rem" }}>
          Search Results
        </h2>
        <div
          style={{
            backgroundColor: "#ffffff",
            padding: "16px",
            borderRadius: "8px",
            boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
          }}
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {results.map((result, index) => (
              <div
                key={index}
                style={{
                  padding: "16px",
                  border: "1px solid #f5e6da",
                  borderRadius: "8px",
                  backgroundColor: "#f9f9f9",
                  boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
                }}
              >
                <p><strong>Username:</strong> {result.username}</p>
                <p><strong>Phone:</strong> {result.phone}</p>
                <p><strong>Address:</strong> {result.address || "N/A"}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;