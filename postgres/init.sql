-- Create raw_listings: store all unprocessed scraped data
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
    scraped_at TIMESTAMP,  -- added explicitly passed timestamp
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- index for faster joins/grouping
CREATE INDEX IF NOT EXISTS idx_raw_source_page ON raw_listings (source, page);

-- Create clean_listings: stores processed/validated data from Spark
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
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scraped_at TIMESTAMP  -- retain original source timestamp
);

 -- index for analytics
CREATE INDEX IF NOT EXISTS idx_clean_location ON clean_listings (location);
CREATE INDEX IF NOT EXISTS idx_clean_price ON clean_listings (price);
