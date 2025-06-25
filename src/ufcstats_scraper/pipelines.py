import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime


class UfcstatsScraperPipeline:
    def process_item(self, item, spider):
        return item


class MongoDataLakePipeline:
    """
    Data Lake pipeline that stores raw scraped data in MongoDB
    with metadata for data lineage and processing tracking
    """

    def __init__(self, mongo_uri: str, mongo_db: str):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGODB_URI"),
            mongo_db=crawler.settings.get("MONGODB_DATABASE"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        spider.logger.info(f"Connected to MongoDB: {self.mongo_db} at {datetime.now()}")

    def close_spider(self, spider):
        if self.client:
            self.client.close()
            spider.logger.info(f"Disconnected from MongoDB at {datetime.now()}")

    def process_item(self, item, spider):
        """
        Process each item and store it in the appropriate MongoDB collection.
        """

        collection_name = self._get_collection_name(item)
        collection = self.db[collection_name]

        try:
            collection.insert_one(ItemAdapter(item).asdict())
            spider.logger.info(
                f"Inserted item into {collection_name} collection: {item}"
            )
        except pymongo.errors.PyMongoError as e:
            spider.logger.error(
                f"Error inserting item into {collection_name} collection: {e}"
            )
            raise DropItem(f"Failed to insert item into {collection_name}: {e}")

    @staticmethod
    def _get_collection_name(item) -> str:
        """
        Determine the collection name based on the item type.
        """
        item_type = type(item).__name__
        collection_map = {
            "EventItem": "events",
            "FighterItem": "fighters",
            "FightItem": "fights",
            "FighterImageItem": "fighter_images",
        }
        try:
            return collection_map[item_type]
        except KeyError:
            raise DropItem(f"Unknown item type: {item_type}")
