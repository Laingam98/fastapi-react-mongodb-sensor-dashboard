// src/App.js
import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import './App.css';

// --- (Chart.js registration, MAX_DATA_POINTS, etc. are all the same) ---
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MAX_DATA_POINTS = 100;

// --- NEW: Helper function to format our new timestamp ---
// This turns "2025-10-27T10:30:05.123Z" into "10:30:05 AM"
const formatTimestamp = (isoString) => {
  if (!isoString) return ""; // Handle cases where data might be missing
  const date = new Date(isoString);
  return date.toLocaleTimeString(); // e.g., "10:30:05 AM"
}

function App() {
  const [sensorData, setSensorData] = useState([]);

  // --- (The useEffect hook is 100% the same) ---
  useEffect(() => {
    // A. Initial data fetch
    async function fetchData() {
      try {
        const response = await fetch("http://127.0.0.1:8000/data/accelerometer");
        const fetchedData = await response.json();
        setSensorData(fetchedData.reverse()); 
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
    fetchData();

    // B. WebSocket connection
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/data");
    ws.onopen = () => console.log("WebSocket connected.");
    ws.onmessage = (event) => {
      const newPoint = JSON.parse(event.data);
      setSensorData(prevData => {
        const updatedData = [...prevData, newPoint];
        return updatedData.length > MAX_DATA_POINTS ? updatedData.slice(1) : updatedData;
      });
    };
    ws.onclose = () => console.log("WebSocket disconnected.");
    ws.onerror = (error) => console.error("WebSocket error:", error);

    // C. Cleanup
    return () => {
      ws.close();
    };
  }, []);

  // --- CHART DATA (Updated labels) ---
  const chartData = {
    // 'labels' are the X-axis points.
    labels: sensorData.map(dataPoint => formatTimestamp(dataPoint.created_at)), // <-- CHANGED
    datasets: [
      {
        label: 'X-Axis',
        data: sensorData.map(dataPoint => dataPoint.x),
        borderColor: 'rgb(255, 99, 132)',
      },
      {
        label: 'Y-Axis',
        data: sensorData.map(dataPoint => dataPoint.y),
        borderColor: 'rgb(53, 162, 235)',
      },
      {
        label: 'Z-Axis',
        data: sensorData.map(dataPoint => dataPoint.z),
        borderColor: 'rgb(75, 192, 192)',
      },
    ],
  };

  // --- (chartOptions is the same) ---
  const chartOptions = {
    responsive: true,
    animation: false,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Live Accelerometer Data' },
    },
    scales: { y: { min: -3000, max: 3000 } }
  };

  // --- HTML (JSX) (Updated table) ---
  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Sensor Dashboard</h1>
      </header>
      
      <main className="dashboard-container">
        
        {/* Card 1: The Chart */}
        <div className="chart-widget widget">
          {sensorData.length > 0 ? (
            <Line options={chartOptions} data={chartData} />
          ) : (
            <p>Loading chart...</p>
          )}
        </div>
        
        {/* Card 2: The Live Data Table */}
        <div className="data-widget widget">
          <h2>Latest Readings</h2>
          <table className="data-table">
            <thead>
              <tr>
                <th>Time</th> {/* <-- CHANGED from ID */}
                <th>X</th>
                <th>Y</th>
                <th>Z</th>
              </tr>
            </thead>
            <tbody>
              {sensorData.slice(-10).reverse().map(point => (
                // We still use 'point.id' for the key, as it's guaranteed unique
                <tr key={point.id}> 
                  <td>{formatTimestamp(point.created_at)}</td> {/* <-- CHANGED from point.id */}
                  <td>{point.x}</td>
                  <td>{point.y}</td>
                  <td>{point.z}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
      </main>
    </div>
  );
}

export default App;