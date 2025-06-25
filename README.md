## Nairobi Real Estate Data Pipeline

A real-time data pipeline that scrapes, processes, stores, and visualizes property listings in Nairobi, Kenya — starting with platforms like **A-List Real Estate**, **BuyRentKenya**, and **Property24**.

---

##  Project Objective

To build a scalable, modular data pipeline that:
- Collects real estate listings from top Kenyan websites
- Cleans and stores listings in a PostgreSQL database
- Sends scheduled email alerts every 6 hours
- Visualizes trends with Elasticsearch and Kibana

📍 **Initial focus is on Nairobi County**, with plans to expand to other towns such as Mombasa, Kisumu, and Eldoret.

---

##  System Architecture

```plaintext
   ┌────────────┐   ┌────────────┐   ┌────────────┐
   │ A-List KE  │   │ BuyRentKenya │ │ Property24 │
   └────┬───────┘   └────┬────────┘   └────┬──────┘
        ▼                ▼                ▼
 ┌────────────────────────────────────────────┐
 │ Scrapers (Python + Airflow scheduled DAGs) │
 └────────────────┬───────────────────────────┘
                  ▼
         ┌─────────────────────┐
         │ Kafka (raw_listings)│ ◄──── JSON property data
         └─────────┬───────────┘
                   ▼
     ┌───────────────────────────────┐
     │ Spark Structured Streaming    │
     │ - Clean + transform data      │
     └────────────┬──────────────────┘
                  ▼
         ┌────────────────────────┐
         │ PostgreSQL (properties)│ ◄──── Final storage
         └─────────┬──────────────┘
                   ▼
      ┌───────────────────────────────┐
      │ Airflow Email Task (6h)       │ ◄──── Summary of new listings
      └───────────────────────────────┘
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
├── airflow/
│   └── dags/
│       ├── a_list_scraper_dag.py
│       ├── buyrentkenya_scraper_dag.py
│       ├── property24_scraper_dag.py
│       └── email_notification_dag.py
│
├── kafka/
│   └── producer/
│       └── push_to_kafka.py
│
├── scraper/
│   ├── a_list_scraper.py
│   ├── buyrentkenya_scraper.py
│   ├── property24_scraper.py
│
├── spark/
│   └── kafka_stream_to_postgres.py
│
├── postgres/
│   ├── schema.sql
│   └── docker-entrypoint.sh
│
├── notification/
│   └── email_notifier.py
│
├── docker-compose.yml
├── .env
├── requirements.txt
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
