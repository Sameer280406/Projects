import React, { useState } from "react";
import axios from "axios";
import { Bar, Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import "./App.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
);

export default function App() {
  const [fileName, setFileName] = useState("");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // 🔥 REAL BACKEND CONNECTION
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setSummary(response.data); // ✅ REAL DATA
    } catch (err) {
      console.error(err);
      setError("Failed to process CSV file. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  // Charts (render only when data exists)
  const barData = summary && {
    labels: ["Flowrate", "Pressure", "Temperature"],
    datasets: [
      {
        label: "Average Values",
        data: [
          summary.avgFlow,
          summary.avgPressure,
          summary.avgTemp,
        ],
        backgroundColor: [
          "rgba(77, 171, 247, 0.7)",
          "rgba(255, 107, 107, 0.7)",
          "rgba(255, 212, 59, 0.7)",
        ],
        borderRadius: 8,
      },
    ],
  };

  const doughnutData = summary && {
    labels: Object.keys(summary.types),
    datasets: [
      {
        data: Object.values(summary.types),
        backgroundColor: [
          "#4dabf7",
          "#ff6b6b",
          "#ffd43b",
          "#63e6be",
          "#845ef7",
          "#ffa94d",
        ],
        borderWidth: 0,
      },
    ],
  };

  return (
    <div className="app">
      {/* HEADER */}
      <header className="topbar">
        <h1>Chemical Equipment Parameter Visualizer</h1>
        <span>Hybrid Web + Desktop Analytics Platform</span>
      </header>

      {/* UPLOAD */}
      <section className="upload-section">
        <label className="upload-box">
          <input type="file" accept=".csv" onChange={handleUpload} />
          <p>📁 Upload CSV Dataset</p>
          {fileName && <small>{fileName}</small>}
        </label>
      </section>

      {/* STATUS */}
      {loading && (
        <p style={{ textAlign: "center" }}>Processing CSV…</p>
      )}
      {error && (
        <p style={{ color: "red", textAlign: "center" }}>
          {error}
        </p>
      )}

      {/* DASHBOARD */}
      {summary && (
        <>
          {/* METRICS */}
          <section className="metrics">
            <Metric title="Total Equipment" value={summary.total} />
            <Metric
              title="Avg Flowrate"
              value={summary.avgFlow}
              unit="m³/s"
            />
            <Metric
              title="Avg Pressure"
              value={summary.avgPressure}
              unit="bar"
            />
            <Metric
              title="Avg Temperature"
              value={summary.avgTemp}
              unit="K"
            />
          </section>

          {/* CHARTS */}
          <section className="charts">
            <div className="chart-card">
              <h3>Average Parameter Analysis</h3>
              <Bar data={barData} />
            </div>

            <div className="chart-card">
              <h3>Equipment Type Distribution</h3>
              <Doughnut data={doughnutData} />
            </div>
          </section>
        </>
      )}

      {/* FOOTER */}
      <footer>
        © 2025 | Designed by Sameer Jagtap
      </footer>
    </div>
  );
}

// 🔹 Metric Card Component
function Metric({ title, value, unit }) {
  return (
    <div className="metric-card">
      <h2>{value}</h2>
      <p>{title}</p>
      {unit && <span>{unit}</span>}
    </div>
  );
}
