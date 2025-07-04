CREATE TABLE IF NOT EXISTS clean_listings (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    price NUMERIC,
    location TEXT,
    address TEXT,
    description TEXT,
    bedrooms INT,
    bathrooms INT,
    parking INT,
    size_sqm NUMERIC,
    source TEXT,
    page INT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
