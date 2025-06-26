CREATE TABLE IF NOT EXISTS raw_listings (
    id SERIAL PRIMARY KEY,
    title TEXT,
    price TEXT,
    location TEXT,
    address TEXT,
    description TEXT,
    bedrooms TEXT,
    bathrooms TEXT,
    parking TEXT,
    size TEXT,
    source TEXT,
    page INT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
