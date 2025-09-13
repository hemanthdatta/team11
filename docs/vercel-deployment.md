# Deploying Backend on Vercel

This project is configured to deploy both the frontend and backend on Vercel. Here's how it works:

## Architecture

1. **Frontend**: React application in `/src` directory, built to `/build` directory
2. **Backend**: FastAPI application deployed as a Vercel serverless function in `/api` directory

## How It Works

- When you deploy to Vercel, it will:
  - Build the frontend according to the build command in `package.json`
  - Deploy the `/api` directory as serverless functions
  - Use the routing rules in `vercel.json` to direct requests

## Configuration Files

- **vercel.json**: Configures routes and serverless function settings
- **api/index.py**: Main serverless function entry point that imports your FastAPI app
- **api/requirements.txt**: Python dependencies for the serverless function

## Limitations

Deploying a FastAPI backend on Vercel serverless functions has some limitations:

1. **Execution Time**: Functions are limited to 10 seconds on the free plan, 60 seconds on paid plans
2. **Cold Starts**: First request after inactivity may be slow
3. **Database**: SQLite isn't suitable for serverless. Consider using a cloud database like:
   - Supabase
   - MongoDB Atlas
   - PostgreSQL on Railway
   - Neon.tech (serverless PostgreSQL)

4. **Background Tasks**: Celery and Redis won't work with Vercel's serverless model

## Recommended Adjustments

For a production application, consider:

1. Using a cloud database instead of SQLite
2. Removing the Celery dependency or using a different background task solution
3. Adding proper environment variables for secrets in the Vercel dashboard

## Environment Variables

Set these in the Vercel dashboard:
- SECRET_KEY
- DATABASE_URL (pointing to a cloud database)
- GEMINI_API_KEY

## Deploying Updates

Just push to your GitHub repository and Vercel will automatically redeploy both frontend and backend.
