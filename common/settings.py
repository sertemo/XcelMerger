#   Copyright 2024 Carlos García, Afonso Teixeira, Carlos, Sergio Tejedor
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
#   limitations under the License..

from pathlib import Path

# Log
FOLDER_LOGS = Path("logs")
LOG_FILE = "xcelmerger.log"
LOG_PATH = FOLDER_LOGS / LOG_FILE

# Servicios
# Auth
AUTH_SERVICE_URL = "http://auth:8000"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3
USERSDB_NAME = "users.db"

# Frontend
FRONTEND_SERVICE_URL = "http://frontend:5050"
