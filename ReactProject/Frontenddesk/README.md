# Industrial Equipment Data Analytics Dashboard

A full‑stack web application for **uploading, analyzing, and visualizing industrial equipment CSV data** using **Django REST Framework + React**. The system computes statistical summaries, visualizes trends, and maintains historical datasets for engineering and academic analysis.

---

## 🚀 Project Overview

This project enables users to:

- Upload industrial equipment datasets in CSV format
- Automatically compute key statistics (averages, counts, distributions)
- Visualize insights through interactive charts
- Maintain history of recent uploads
- Connect a modern React frontend with a robust Django REST backend

The application is designed with **correctness, clarity, and scalability** in mind rather than superficial UI complexity.

---

## 🧠 Problem Statement

Industrial datasets are often analyzed manually or using disconnected tools. This project demonstrates how **data ingestion, statistical computation, and visualization** can be unified into a single, clean web-based system suitable for:

- Academic labs
- Research prototypes
- Engineering analytics dashboards

---

## 🏗️ System Architecture

```
CSV Upload (Frontend)
        ↓
Django REST API
        ↓
Pandas Data Processing
        ↓
Statistical Summary
        ↓
React Dashboard + Charts
```

Both **web and desktop frontends** can consume the same REST API, ensuring reusability.

---

## ⚙️ Tech Stack

### Backend

- Django
- Django REST Framework
- Pandas
- SQLite (for lightweight persistence)

### Frontend

- React
- Axios
- Chart.js
- Modern CSS (Glassmorphism‑inspired UI)

---

## 📊 Features

### 1️⃣ CSV Upload & Parsing

- Accepts CSV files containing industrial equipment data
- Validates presence of required columns

### 2️⃣ Automatic Statistical Analysis

Computed using Pandas:

- Total equipment count
- Average Flowrate
- Average Pressure
- Average Temperature
- Equipment type distribution

### 3️⃣ Interactive Dashboard

- KPI cards for averages
- Bar & Pie charts for distribution
- Real‑time UI updates after upload

### 4️⃣ Dataset History

- Stores last **5 uploaded datasets**
- Useful for comparison and experimentation

### 5️⃣ API‑Driven Design

- Clean REST endpoints
- Frontend and backend decoupled

---

## 📁 API Endpoints

| Method | Endpoint        | Description                     |
| ------ | --------------- | ------------------------------- |
| POST   | `/api/upload/`  | Upload CSV and generate summary |
| GET    | `/api/latest/`  | Fetch latest dataset summary    |
| GET    | `/api/history/` | Fetch last 5 datasets           |

---

## 📄 Sample CSV Format

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
```

---

## 🧪 Correctness First Philosophy

Special care has been taken to ensure:

- Accurate statistical calculations
- Validation of computed averages
- Immediate correction of mismatched results

This reflects real engineering workflows where **data accuracy is more important than visual polish**.

---

## ▶️ How to Run the Project

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## 🧠 Design Decisions

- **Pandas** for reliability and mathematical correctness
- **REST API** for frontend independence
- **History limit** to avoid database clutter
- **React** for real‑time visualization updates

---

## 🔮 Future Enhancements

- CSV schema validation
- Anomaly detection on sensor values
- Export analytics as PDF reports
- Real‑time sensor data ingestion
- Role‑based dashboards

---

## 🎓 Academic & Internship Relevance

This project demonstrates:

- Full‑stack integration
- Data engineering fundamentals
- API‑driven architecture
- Analytical thinking and correctness validation

It is suitable for **research internships, academic evaluation, and engineering demonstrations**.

---

## 👤 Author

**Sameer Jagtap**
Bachelor of Accounting & Finance (BAF)
Aspiring Full‑Stack & Data Engineering Enthusiast

---

## 📜 License

This project is developed for academic and learning purposes.

---

> "Engineering is not about writing more code, but about producing correct results."
