import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from datetime import datetime
from mqtt_client import start_mqtt

# Start MQTT in the background
start_mqtt(blocking=False)

# Load environment variables from .env file
load_dotenv()

# Required environment variables for config endpoint
REQUIRED_VARS = [
    'DJI_APP_ID',
    'DJI_APP_KEY',
    'DJI_LICENSE',
    'MQTT_HOST',
    'MQTT_USERNAME',
    'MQTT_PASSWORD',
]

# Configuration
PORT = int(os.getenv('PORT', 3000))
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"🚀 Server running on http://localhost:{PORT}")
    print(f"📊 Dashboard available at http://localhost:{PORT}")
    print(f"🔧 API config endpoint: http://localhost:{PORT}/api/config")

    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        print(f"⚠️  Missing environment variables: {', '.join(missing)}")
        print("⚠️  Please check your .env file")
    else:
        print("✅ All environment variables loaded successfully")
    yield
    # Shutdown (if needed)

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Middleware: enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

@app.get("/api/config")
async def get_config():
    # Only return configuration if all required environment variables are set
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Missing environment variables",
                "missing": missing,
            },
        )
    return {
        "appId": int(os.getenv('DJI_APP_ID')),
        "appKey": os.getenv('DJI_APP_KEY'),
        "license": os.getenv('DJI_LICENSE'),
        "mqttHost": os.getenv('MQTT_HOST'),
        "username": os.getenv('MQTT_USERNAME'),
        "password": os.getenv('MQTT_PASSWORD'),
    }

@app.get("/api/health")
async def health_check():
    # Health check endpoint
    return {"status": "OK", "timestamp": datetime.utcnow().isoformat()}

@app.get("/")
async def serve_dashboard():
    # Serve the dashboard HTML
    dashboard_path = os.path.join(PUBLIC_DIR, 'dashboard.html')
    if not os.path.exists(dashboard_path):
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return FileResponse(dashboard_path)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Handle 404 errors with custom message
    if exc.status_code == 404:
        return JSONResponse(status_code=404, content={"error": "Endpoint not found"})
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the error stack and return generic message
    print(f"Error: {exc}")
    return JSONResponse(status_code=500, content={"error": "Something went wrong!"})

if __name__ == "__main__":
    import uvicorn
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=PORT)
