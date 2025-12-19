# Real-Time Air Quality ETL Pipeline

A containerized data engineering pipeline that fetches real-time Air Quality Index (AQI) data, processes it through a messaging queue, and stores cleaned analytics in a relational database.



## 🚀 Overview
This project implements a complete ETL/ELT workflow:
1.  **Ingestion**: A Python Producer fetches data from the World Air Quality Index (WAQI) API and streams it to **Apache Kafka**.
2.  **Orchestration**: **Apache Airflow** manages three distinct DAGs to automate data collection, cleaning, and analysis.
3.  **Processing**: Raw JSON is normalized and filtered (removing outliers and invalid records).
4.  **Storage**: Cleaned events and aggregated metrics are stored in **SQLite**.

## 🛠 Tech Stack
* **Language:** Python 3.8+
* **Orchestration:** Apache Airflow
* **Streaming/Message Broker:** Apache Kafka
* **Database:** SQLite
* **Infrastructure:** Docker & Docker Compose

## 📂 Project Structure
final/
├── airflow/
│   └── dags/                    # Airflow Orchestration
│       ├── job1_ingestion_dag.py     # Trigger for job1
│       ├── job2_clean_store_dag.py      # Trigger for job2
│       └── job3_daily_summary_dag.py     # Trigger for job3
├── src/                         # Core Logic (The "Jobs")
│   ├── job1_producer.py                  # Producer
│   ├── job2_cleaner.py                   # Cleaner
│   └── job3_analytics.py                 # Analytics
│   └── db_utils.py                  # Database connection helper
├── data/                        # Persistent SQLite Storage
│   └── app.db                   # SQLite database file
├── .env                         # API Token (AQI_TOKEN=...)
├── cities.txt                   # Configurable city list
├── docker-compose.yaml          # Infrastructure as Code
└── README.md                    # Project Documentation

## ⚙️ Configuration & Extensibility
The pipeline is designed for high flexibility:
* **Security (`.env`):** Sensitive API tokens are kept out of the source code.
* **Scalability (`cities.txt`):** To monitor new locations, simply add city names to this file. The Producer dynamically reads this list at runtime without requiring code changes.

## 📊 Data Schema
The storage layer follows technical requirements with two primary tables:

| Table | Description | Key Columns |
| :--- | :--- | :--- |
| **`events`** | Cleaned measurement data | `city`, `aqi`, `lat`, `lon`, `timestamp` |
| **`daily_summary`** | Aggregated city metrics | `min_aqi`, `max_aqi`, `avg_aqi`, `air_quality_category` |



## ⚡ Quick Start
1.  **Configure Credentials**: Create a `.env` file in the root directory and add:
    ```env
    AQI_TOKEN=your_api_key_here
    ```
2.  **Set Cities**: Update `cities.txt` with the cities you wish to track.
3.  **Launch Environment**:
    ```bash
    docker compose up -d
    ```
4.  **Orchestrate**:
    * Log in to Airflow at `http://localhost:8080` (User: `airflow` / Pass: `airflow`).
    * Trigger **DAG 1** (Ingestion), **DAG 2** (Cleaning), and **DAG 3** (Analytics) in sequence.

## 🔍 Verification
To verify the successful population of the analytical layer, run:
```bash
docker compose exec airflow-webserver sqlite3 -header -column /opt/airflow/data/app.db "SELECT * FROM daily_summary;"
