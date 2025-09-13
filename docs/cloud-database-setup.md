# Setting Up a Cloud Database for Your Vercel Backend

For a production-ready application deployed on Vercel, you need to use a cloud database instead of SQLite. Here's how to set up different cloud database options for your application.

## Option 1: Neon - Serverless PostgreSQL (Recommended)

[Neon](https://neon.tech) is a serverless PostgreSQL service that works very well with Vercel deployments.

### Steps to Set Up Neon:

1. **Create a Neon Account**: 
   - Sign up at [https://neon.tech](https://neon.tech)
   - Create a new project

2. **Get Connection String**:
   - From your Neon dashboard, get the connection string
   - It will look like: `postgresql://user:password@endpoint/database`

3. **Update Database Configuration**:
   - Add the connection string to your Vercel environment variables as `DATABASE_URL`
   - Remove the `connect_args={"check_same_thread": False}` parameter from your database setup

4. **Install Required Package**:
   - Add `psycopg2-binary==2.9.9` to your requirements.txt file

5. **Update Database Schema**:
   - Run your database migrations or schema setup against the new database

## Option 2: Supabase - PostgreSQL with Authentication

Supabase provides PostgreSQL databases with built-in authentication services.

### Steps to Set Up Supabase:

1. **Create a Supabase Account**:
   - Sign up at [https://supabase.com](https://supabase.com)
   - Create a new project

2. **Get Connection String**:
   - From the project settings, find your database connection string
   - It will look like: `postgresql://postgres:password@project.supabase.co:5432/postgres`

3. **Update Database Configuration**:
   - Add the connection string to your Vercel environment variables as `DATABASE_URL`
   - Remove the `connect_args={"check_same_thread": False}` parameter from your database setup

4. **Install Required Package**:
   - Add `psycopg2-binary==2.9.9` to your requirements.txt file

## Option 3: MongoDB Atlas

If you prefer a NoSQL approach, MongoDB Atlas is a good option.

### Steps to Set Up MongoDB Atlas:

1. **Create a MongoDB Atlas Account**:
   - Sign up at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Create a new cluster (the free tier is fine for starting)

2. **Get Connection String**:
   - In the Atlas dashboard, click "Connect" and select "Connect your application"
   - Copy the connection string (it will look like: `mongodb+srv://user:password@cluster.mongodb.net/mydb`)

3. **Update Your Code**:
   - This would require more significant changes as you're currently using SQLAlchemy with SQL
   - You would need to switch to using a MongoDB client like pymongo or motor

4. **Install Required Packages**:
   - Add `pymongo==4.6.0` to your requirements.txt file

## Implementation for PostgreSQL (Neon/Supabase)

Here's how to update your database.py file for a PostgreSQL database:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL")

# If the URL starts with "postgres://" (Heroku format), change to "postgresql://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# For local development fallback
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./app.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # For production PostgreSQL database
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Setting Up for Production

1. **Create Database Tables**:
   - If you're using SQLAlchemy, you'll need to create the tables in your PostgreSQL database
   - Modify your `init_db.py` to connect to the PostgreSQL database

2. **Environment Variables on Vercel**:
   - Set the following environment variables in Vercel:
     - `DATABASE_URL`: Your database connection string
     - `SECRET_KEY`: A secure random key for JWT tokens
     - `GEMINI_API_KEY`: Your Google Gemini API key

3. **Deploy to Vercel**:
   - Push your changes to GitHub
   - Vercel will automatically deploy your application

Remember to never commit sensitive information like database credentials to your repository.
