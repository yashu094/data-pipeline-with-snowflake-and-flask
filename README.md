# Multilingual Translation API with Snowflake and Flask

## Project Overview
This project involves creating a backend API to manage multilingual translation data, utilizing Snowflake for data storage and Flask for API development. The system enables retrieval, insertion, and analysis of translation data.

## System Architecture
- **Snowflake**: Stores multilingual data in a `multilingual_data` table.
- **Flask API**: Exposes endpoints to interact with the database.
- **Caching**: `Flask-Caching` reduces query load on Snowflake.

## Database Schema
### Snowflake Table Schema:
The database schema for storing multilingual translation data is as follows:
```sql
CREATE TABLE multilingual_data (
    TALK_ID INT PRIMARY KEY,
    NATIVE_LANG VARCHAR,
    TRANSCRIPT VARCHAR,
    SPEAKER_1 VARCHAR,
    RECORDED_DATE DATE,
    TITLE VARCHAR,
    VIEWS INT,
    DURATION INT
);
API Endpoints
1. GET /translations
Description: Fetch translations based on the language parameter.
Parameters:
language: The language of the translation to retrieve.
Response: List of translations in the requested language.
2. POST /translations
Description: Insert new translation data into Snowflake.
Body:
json
Copy code
{
    "TALK_ID": 1,
    "NATIVE_LANG": "English",
    "TRANSCRIPT": "This is a sample translation",
    "SPEAKER_1": "Speaker Name",
    "RECORDED_DATE": "2024-12-01",
    "TITLE": "Sample Title",
    "VIEWS": 1000,
    "DURATION": 300
}
Response: A success message upon data insertion.
3. GET /analytics
Description: Retrieve analytics on frequently translated languages or high-usage periods.
Parameters:
type: The type of analytics to retrieve. Options:
language: Number of translations per language.
period: Number of translations per recorded date.
Response: A summary of translation analytics.
Implementation Highlights
Caching: The GET /translations endpoint uses caching to improve performance and reduce redundant database access.
SQL Queries: Optimized SQL queries for:
Retrieving translations by language.
Fetching translation analytics by language or recorded date.
Optimization Techniques
Caching: Caching is used to reduce frequent database queries and improve response time. The GET /translations endpoint caches the response for 60 seconds.
SQL Indexing: To further optimize performance, consider implementing indexing on NATIVE_LANG and RECORDED_DATE for faster querying, especially for large datasets.
Steps to Run the Application
1. Install Dependencies
Run the following command to install the required dependencies:

bash
Copy code
pip install -r requirements.txt
2. Set up Snowflake Credentials
Configure your Snowflake connection in the get_snowflake_connection() function. Replace the placeholders with your actual Snowflake account details:

python
Copy code
def get_snowflake_connection():
    return snowflake.connector.connect(
        user='YOUR_USERNAME',
        password='YOUR_PASSWORD',
        account='YOUR_ACCOUNT',
        warehouse='YOUR_WAREHOUSE',
        database='YOUR_DATABASE',
        schema='YOUR_SCHEMA'
    )
3. Run Flask Server
Start the Flask server by running the following command:

bash
Copy code
python app.py
4. Test API Endpoints
You can test the endpoints using Postman or any HTTP client:

GET /translations: Retrieve translations based on the language parameter.
POST /translations: Insert new translation data into the database.
GET /analytics: Retrieve translation analytics by language or period.
Conclusion
This API provides a scalable solution for managing multilingual translation data. Caching and query optimizations ensure efficient handling of large datasets. With the ability to fetch translations, upload new data, and analyze usage, this system can be extended and integrated into various multilingual data-driven applications.
