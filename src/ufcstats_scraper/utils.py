from datetime import datetime
import pymongo
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

mongo_uri = settings.get("MONGODB_URI")
mongo_db = settings.get("MONGODB_DATABASE")
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]


def clean_text(text):
    """Clean extracted text by removing extra whitespace and handling None values."""
    if text:
        return text.strip()
    return None


def format_date(date_str):
    """Format date string to a standard format (YYYY-MM-DD)."""
    date_str = clean_text(date_str)
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def get_fight_urls():
    events_collection = db["events"]
    fighters_collection = db["fighters"]
    fight_urls = set()

    for event in events_collection.find():
        if "fight_refs" in event:
            for fight_ref, _ in event["fight_refs"]:
                fight_urls.add(fight_ref)

    for fighter in fighters_collection.find():
        if "fight_urls" in fighter:
            for fight_url in fighter["fight_urls"]:
                fight_urls.add(fight_url)
    client.close()
    return list(fight_urls)
