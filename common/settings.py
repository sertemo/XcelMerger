#   Copyright 2024 Carlos García, Afonso Teixeira, Sergio Tejedor
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Log
FOLDER_LOGS = Path("logs")
LOG_FILE = "xcelmerger.log"
LOG_PATH = FOLDER_LOGS / LOG_FILE

# Databases
# Users
USER_DB_URL = os.getenv("USER_DB_URL", " ")

# Fetch
FETCH_DB_USER = os.getenv("FETCH_DB_USER")
FETCH_DB_PASSWORD = os.getenv("FETCH_DB_PASSWORD")
FETCH_DB_HOST = os.getenv("FETCH_DB_HOST")
FETCH_DB_NAME = os.getenv("FETCH_DB_NAME")
FETCH_DB_URL = (
    f"postgresql://{FETCH_DB_USER}:{FETCH_DB_PASSWORD}@{FETCH_DB_HOST}/{FETCH_DB_NAME}"
)

# Servicios
# Auth
AUTH_SERVICE_URL = "http://auth:8000"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3

# Frontend
FRONTEND_SERVICE_URL = "http://frontend:5050"
