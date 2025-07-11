## Nairobi Real Estate Data Pipeline 
A real-time data pipeline that scrapes, processes, stores, and visualizes property listings in Nairobi, Kenya — starting with platforms like **A-List Real Estate**, **BuyRentKenya**, and **Property24**.

### Problem Statement
Nairobi’s real estate market is fragmented, opaque, and difficult to track in real time. Most property listings are scattered across various platforms like A-List, BuyRentKenya, and Property24, with:

* No centralized view of new listings or pricing trends

* Manual search effort for buyers, renters, and investors

* Outdated or duplicate listings, making decision-making inefficient

* No automated analytics for agents, developers, or researchers

* Minimal market intelligence for planning, urbanization, or investment

### How This Project Helps to Solve Real Estate Challenges in Nairobi with Data Engineering
This data pipeline automates the collection, cleaning, and delivery of property listing data across multiple major websites in real-time. It aims to:

* Centralize Listings
    * Gathers listings from multiple top real estate websites in Kenya

    * Consolidates data into one source of truth (clean_db)

* Enable Real-Time Monitoring
    * Uses Apache Kafka + Spark to ingest and clean data in real time

    * Keeps data fresh, deduplicated, and structured

* Deliver Automated Insights
    * Sends email summaries every 6 hours with new property listings


* Empower Stakeholders
    * Buyers: Save time browsing scattered sites — get clean, consolidated listings

    * Agents: Monitor competitor listings or trends in real time

    * Analysts/Planners: Gain visibility into property volume, location hotspots, pricing changes

* Scale to Other Use Cases
The architecture is modular, so it can be extended to:

    * Other towns (e.g., Mombasa, Kisumu)

    * Other asset classes (e.g., used cars, rental furniture, etc.)



---

##  Project Objective

To build a scalable, modular data pipeline that:
- Collects real estate listings from top Kenyan websites
- Cleans and stores listings in a PostgreSQL database
- Sends scheduled email alerts every 6 hours
- Visualizes trends with Elasticsearch and Kibana

📍 **Initial focus is on Nairobi County**, with plans to expand to other towns such as Mombasa, Kisumu, and Eldoret.

---
## System Architecture
```
                       ┌──────────────────────────────┐
                       │ Real Estate Websites         │
                       │ - Property24                 │
                       │ - A-List KE                  │
                       │ - BuyRentKenya               │
                       │ - [More in future...]        │
                       └──────────┬───────────────────┘
                                  ▼
                ┌────────────────────────────────────────┐
                │ Scrapers (Python + Airflow DAGs)       │
                │ - One DAG per platform                 │
                │ - Scheduled (e.g., hourly)             │
                └──────────────┬─────────────────────────┘
                               ▼
                 ┌────────────────────────────────────┐
                 │ PostgreSQL: raw_listings table      │
                 │ - Stores raw scraped data           │
                 └──────────────┬──────────────────────┘
                                ▼
         ┌──────────────────────────────────────────────────┐
         │ Spark Batch Job (Manual or Scheduled via Airflow)│
         │ - Cleans, deduplicates, standardizes             │
         │ - Handles multi-source logic                     │
         └───────────────┬──────────────────────────────────┘
                         ▼
           ┌────────────────────────────────────────────┐
           │ PostgreSQL: clean_listings table           │
           │ - Clean, unified schema                    │
           │ - Source-specific normalization handled    │
           └───────────────┬────────────────────────────┘
                           ▼
        ┌──────────────────────────────────────────────┐
        │ Airflow Email Task (Every 6h)                │
        │ - Sends new listings summary                 │
        │ - Optionally filtered by source or location  │
        └────────────────┬─────────────────────────────┘
                         ▼
        ┌──────────────────────────────────────────────┐
        │ Prometheus + Grafana                         │
        │ - Monitors scraping, DAG health, DB growth   │
        └──────────────────────────────────────────────┘


```


##  Tech Stack

| Tool        | Role                                      |
|-------------|-------------------------------------------|
| **Python**           | Scrapers, Email Sender, Kafka Producer       |
|  **PostgreSQL**       | Main relational storage                     |
|  **Apache Spark**      | Structured streaming + data transformation |
|  **Apache Airflow**    | DAG scheduling for scraping & notification  |
|  **SMTP / SendGrid**   | Email delivery of new listings summary      |
|  **Prometheus + Grafana** ** | Metrics monitoring and service dashboards |

Also integrated with:
-  **Docker Compose** for local orchestration
-  **GitHub Actions** for CI/CD automation

---

## Project Structure
```
Nairobi-real-estate-pipeline/
├── airflow_dags/
│   ├── dags/
│   │   ├── property24_scraper_dag.py
│   │   ├── email_notification_dag.py
│   │   └── __pycache__/
│   └── docker-entrypoint.sh
│
├── scraper/
│   ├── property24_scraper.py
│   └── __init__.py
│
├── spark/
│   └── property24_batch_process.py  # Cleans raw → clean_listings
│
├── postgres/
│   └── init.sql  # schema for raw_listings and clean_listings
│
├── notification/
│   └── email_notifier.py
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│
├── docker-compose.yml
├── Dockerfile.airflow
├── requirements.txt
├── LICENSE
└── README.md

```

## Getting Started
1. Clone the repository
```
git clone https://github.com/samwanyua/Nairobi-real-estate-data-pipeline.git
cd Nairobi-real-estate-data-pipeline
```
2. Configure environment variables
Copy and edit the .env file:

```
cp .env.example .env
```
Example .env:

```
POSTGRES_USER=realestate
POSTGRES_PASSWORD=password
POSTGRES_DB=properties
SMTP_USER=your_email@example.com
SMTP_PASS=your_app_password
EMAIL_RECEIVER=receiver@example.com
```
3. Launch services via Docker
```
docker-compose up -d
```
4. Run a scraper manually (optional)
```
python scraper/a_list_scraper.py
```
5. Start the Spark streaming job
```
spark-submit spark/kafka_stream_to_postgres.py
```
