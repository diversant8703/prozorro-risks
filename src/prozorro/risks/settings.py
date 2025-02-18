from datetime import datetime

from pymongo import ReadPreference
from pymongo.write_concern import WriteConcern
from pymongo.read_concern import ReadConcern
from pytz import timezone
import standards
import sys
import os

API_HOST = os.environ.get("PUBLIC_API_HOST", "https://api.prozorro.gov.ua")
API_VERSION = os.environ.get("API_VERSION", "2.5")
BASE_URL = f"{API_HOST}/api/{API_VERSION}"

MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://mongo:27017/")
DB_NAME = os.environ.get("DB_NAME", "prozorro-risks")
# 'PRIMARY', 'PRIMARY_PREFERRED', 'SECONDARY', 'SECONDARY_PREFERRED', 'NEAREST',
READ_PREFERENCE = getattr(ReadPreference, os.environ.get("READ_PREFERENCE", "PRIMARY"))
raw_write_concert = os.environ.get("WRITE_CONCERN", "1")
WRITE_CONCERN = WriteConcern(w=int(raw_write_concert) if raw_write_concert.isnumeric() else raw_write_concert)
READ_CONCERN = ReadConcern(level=os.environ.get("READ_CONCERN") or None)

SWAGGER_DOC_AVAILABLE = bool(os.environ.get("SWAGGER_DOC_AVAILABLE", True))

IS_TEST = "test" in sys.argv[0]
SENTRY_DSN = os.getenv("SENTRY_DSN")
TIMEZONE = timezone(os.getenv("TIMEZONE", "Europe/Kiev"))
CLIENT_MAX_SIZE = int(os.getenv("CLIENT_MAX_SIZE", 1024**2 * 100))

MAX_LIST_LIMIT = int(os.environ.get("MAX_LIST_LIMIT", 100))
MAX_TIME_QUERY = int(os.environ.get("MAX_TIME_QUERY", 10000))  # query time limit during filtering risks in ms
MONGODB_ERROR_INTERVAL = float(os.getenv("MONGODB_ERROR_INTERVAL", 1))
CRAWLER_START_DATE = datetime.fromisoformat(os.getenv("CRAWLER_START_DATE", "2015-02-23T12:00:00.756010+02:00"))
OLD_SAS_RISKS_END_DATE = os.getenv("OLD_SAS_RISKS_END_DATE", "2024-10-31")

# Excel cannot handle more than 1,048,576 rows
REPORT_ITEMS_LIMIT = min(int(os.environ.get("REPORT_ITEMS_LIMIT", 100000)), 1048500)
ALLOW_ALL_ORIGINS = bool(os.environ.get("ALLOW_ALL_ORIGINS", True))
WINNER_AWARDED_DAYS_LIMIT_FOR_OPEN_TENDERS = 5
TEST_MODE = bool(os.environ.get("TEST_MODE", False))
HTTPS_PROXY = os.environ.get("HTTPS_PROXY", "")

WORKING_DAYS = {}
HOLIDAYS = standards.load("calendars/workdays_off.json")
for date_str in HOLIDAYS:
    WORKING_DAYS[date_str] = True

CACHE_TTL = os.environ.get("CACHE_TTL", 86400)  # default 24 hours
