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

   ┌────────────┐   ┌───────────────┐   ┌────────────┐
   │ A-List KE  │   │ BuyRentKenya  │   │ Property24 │
   └────┬───────┘   └────┬──────────┘   └────┬──────┘
        ▼                ▼                   ▼
 ┌────────────────────────────────────────────────────────┐
 │ Scrapers (Python + Airflow DAGs scheduled via cron)   │
 └────────────────┬───────────────────────────────────────┘
                  ▼
         ┌──────────────────────┐
         │ Kafka (raw_listings) │ ◄──── JSON scraped data
         └─────────┬────────────┘
                   ▼
     ┌──────────────────────────────────────────────────────────────┐
     │ Spark Structured Streaming (Kafka consumer)                  │
     │ - Cleans, deduplicates, transforms                           │
     │ - Automates parsing, type casting, deduplication, formatting│
     └────┬───────────────────────┬────────────────────────────────┘
          ▼                       ▼
┌──────────────────────┐    ┌───────────────────────────────┐
│ PostgreSQL: raw_db   │    │ PostgreSQL: clean_db           │
│ - raw.property_listings │    │ - clean.property_listings     │
└────────────┬─────────┘    └────────────┬────────────────┘
             ▼                          ▼
 ┌───────────────────────────────┐   ┌──────────────────────────────┐
 │ Airflow Email Task (every 6h) │   │ Kibana + Elasticsearch (📊 UI)│
 │ - Summary of new listings     │   │ - Real-time insights/search  │
 └───────────────────────────────┘   └──────────────────────────────┘
```


##  Tech Stack

| Tool        | Role                                      |
|-------------|-------------------------------------------|
| **Python**           | Scrapers, Email Sender, Kafka Producer       |
|  **PostgreSQL**       | Main relational storage                     |
|  **Apache Kafka**     | Real-time ingestion of scraped listings     |
|  **Apache Spark**      | Structured streaming + data transformation |
|  **Apache Airflow**    | DAG scheduling for scraping & notification  |
|  **SMTP / SendGrid**   | Email delivery of new listings summary      |
|  **Elasticsearch + Kibana** ** | Dashboards and map-based search |

Also integrated with:
-  **Docker Compose** for local orchestration
-  **GitHub Actions** for CI/CD automation

---

## Project Structure
```
Nairobi-real-estate-pipeline/
├── airflow_dags/
│ ├── dags/
│ │ ├── a_list_scraper_dag.py
│ │ ├── buyrentkenya_scraper_dag.py
│ │ ├── db_cleanup_or_reprocess_dag.py
│ │ ├── email_notification_dag.py
│ │ ├── kafka_to_postgres.py
│ │ ├── property24_scraper_dag.py
│ │ └── pycache/
│ └── docker-entrypoint.sh
│
├── kafka_producer/
│ ├── init.py
│ ├── producer/
│ │ ├── Dockerfile
│ │ ├── init.py
│ │ ├── push_to_kafka.py
│ │ └── pycache/
│ └── pycache/
│
├── scraper/
│ ├── a_list_scraper.py
│ ├── buyrentkenya_scraper.py
│ ├── property24_scraper.py
│ ├── init.py
│ └── pycache/
│
├── spark/
│ └── kafka_stream_to_postgres.py # Reads from Kafka → writes to clean_db
│
├── postgres/
│ ├── raw_db/
│ │ └── init.sql # raw.property_listings schema
│ ├── clean_db/
│ │ └── init.sql # clean.property_listings schema
│
├── notification/
│ └── email_notifier.py # Sends property alerts via email
│
├── elasticsearch/
│ ├── pipeline_to_es.py # Push transformed data to Elasticsearch
│ └── dashboards/
│ └── kibana_saved_objects.ndjson # Kibana dashboard config
│
├── env/ # Python virtual environment
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
