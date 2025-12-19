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

The project is organized to separate orchestration logic from core data processing:

* **`airflow/dags/`**: Contains the DAG definitions. These files define the workflow schedule and task dependencies but do not contain business logic.
* **`src/`**: The engine of the pipeline.
    * `job1_producer.py`: Fetches raw data from WAQI API and pushes to Kafka.
    * `job2_cleaner.py`: Consumes Kafka messages, cleans data, and populates the **events** table.
    * `job3_analytics.py`: Performs SQL aggregations to update the **daily_summary** table.
    * `db_utils.py`: Shared utility for database connectivity across all jobs.
* **`data/`**: A mounted volume where the SQLite `app.db` resides, ensuring data persists even if containers are restarted.
* **Root Files**:
    * `.env`: Secure storage for the `AQI_TOKEN`.
    * `cities.txt`: A simple text file to manage the scope of monitored cities.
    * `requirements.txt`: Requirements file.

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
