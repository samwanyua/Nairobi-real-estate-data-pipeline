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

