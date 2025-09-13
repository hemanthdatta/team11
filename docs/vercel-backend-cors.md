# Backend CORS Configuration for Vercel Deployment

When you deploy your frontend to Vercel, you need to update the CORS settings in your backend to allow requests from your Vercel domain. Here's how to do it:

## 1. Find your Vercel domain

Your Vercel domain will typically be in one of these formats:
- `team11-xxxx.vercel.app` (automatically generated)
- `team11.vercel.app` (if you claimed the project name)
- Your custom domain (if configured)

## 2. Update the backend CORS settings

Open `/backend/app/main.py` and add your Vercel domain to the `allowed_origins` list:

```python
# Add CORS middleware - configure based on environment
import os
allowed_origins = ["http://localhost:5000", "http://127.0.0.1:5000", "http://0.0.0.0:5000"]

# Add production domain if deployed
if os.getenv("REPLIT_DOMAIN"):
    allowed_origins.append(f"https://{os.getenv('REPLIT_DOMAIN')}")

# Add Vercel domain
allowed_origins.append("https://your-vercel-domain.vercel.app")  # Replace with your actual Vercel domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,  # Disabled for security
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)
```

## 3. Alternative: Allow all origins (less secure, only for testing)

If you're just testing and want to quickly allow all origins, you can modify the CORS middleware:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - ONLY FOR TESTING!
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)
```

⚠️ WARNING: Using `allow_origins=["*"]` is not recommended for production as it allows any website to make requests to your API.

## 4. Deploy your updated backend

After making these changes, deploy your backend to your chosen hosting provider.

## 5. Update the frontend configuration

Finally, update the `src/config.ts` file with your actual backend URL:

```typescript
// When running on Vercel (production)
if (window.location.hostname !== 'localhost' && 
    window.location.hostname !== '127.0.0.1' && 
    window.location.hostname !== '0.0.0.0') {
  return 'https://your-actual-backend-url.com';  // Replace with your deployed backend URL
}
```

After making these changes, redeploy your frontend to Vercel.
