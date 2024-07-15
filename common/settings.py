from pathlib import Path

# Log
FOLDER_LOGS = Path("logs")
LOG_FILE = "xcelmerger.log"
LOG_PATH = FOLDER_LOGS / LOG_FILE

# Servicios
## Auth
AUTH_SERVICE_URL = "http://auth:8000"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3

## Frontend
FRONTEND_SERVICE_URL = "http://frontend:5050"
