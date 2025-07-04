import psycopg2
import json
from elasticsearch import Elasticsearch, helpers

# PostgreSQL connection config
PG_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'nrbproperties',
    'user': 'postgres',
    'password': 'postgres'
}

# Elasticsearch connection config
ES_HOST = "http://localhost:9200"
ES_INDEX = "nairobi-properties"

def fetch_properties():
    conn = psycopg2.connect(**PG_CONFIG)
    cursor = conn.cursor()
    
    query = """
    SELECT id, title, location, price, bedrooms, bathrooms, size, listing_url
    FROM properties
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    colnames = [desc[0] for desc in cursor.description]
    
    properties = [dict(zip(colnames, row)) for row in rows]
    
    cursor.close()
    conn.close()
    
    return properties

def push_to_elasticsearch(data):
    es = Elasticsearch(ES_HOST)
    
    actions = [
        {
            "_index": ES_INDEX,
            "_id": item["id"],
            "_source": item
        }
        for item in data
    ]
    
    if actions:
        helpers.bulk(es, actions)
        print(f"Pushed {len(actions)} records to Elasticsearch index '{ES_INDEX}'")
    else:
        print("No data to push.")

def main():
    print("Fetching property listings from Postgres...")
    properties = fetch_properties()
    
    print("Indexing properties into Elasticsearch...")
    push_to_elasticsearch(properties)

if __name__ == "__main__":
    main()
