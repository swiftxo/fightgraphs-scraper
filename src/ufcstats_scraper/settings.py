import os
from dotenv import load_dotenv


load_dotenv()


BOT_NAME = "ufcstats_scraper"

SPIDER_MODULES = ["ufcstats_scraper.spiders"]
NEWSPIDER_MODULE = "ufcstats_scraper.spiders"

ADDONS = {}

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE= os.getenv("MONGODB_DATABASE")




CONCURRENT_REQUESTS = int(os.getenv("CONCURRENT_REQUESTS"))
CONCURRENT_REQUESTS_PER_DOMAIN = int(os.getenv("CONCURRENT_REQUESTS_PER_DOMAIN"))
ROBOTSTXT_OBEY = os.getenv("ROBOTSTXT_OBEY")


LOG_ENABLED = True
LOGSTASH_HOST = os.getenv("LOGSTASH_HOST")
LOGSTASH_PORT = os.getenv("LOGSTASH_PORT")
LOG_LEVEL = 'INFO'



ITEM_PIPELINES = {
	"ufcstats_scraper.pipelines.MongoDataLakePipeline": 300,
}

SPIDER_MIDDLEWARES = {
    'ufcstats_scraper.middlewares.LogstashLoggerMiddleware': 50, # Adjust priority as needed
    'ufcstats_scraper.middlewares.UfcstatsScraperSpiderMiddleware': 543, # Adjust priority
}

# Downloader Middlewares
DOWNLOADER_MIDDLEWARES = {
    'ufcstats_scraper.middlewares.UfcstatsScraperDownloaderMiddleware': 543, # Adjust priority
}
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "ufcstats_scraper.middlewares.UfcstatsScraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "ufcstats_scraper.middlewares.UfcstatsScraperDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "ufcstats_scraper.pipelines.UfcstatsScraperPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
