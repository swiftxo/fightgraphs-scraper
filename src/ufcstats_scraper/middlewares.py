# In src/ufcstats_scraper/middlewares.py

import logging
import logstash
from scrapy import signals
from scrapy.utils.project import get_project_settings

# Helper function to configure Logstash
def configure_logstash_handler(logger, host, port, message_type):
    """
    Adds a Logstash TCP handler to the given logger if it doesn't already exist.
    Supports both Logger and LoggerAdapter.
    """
    # Get the underlying logger if this is a LoggerAdapter
    base_logger = getattr(logger, "logger", logger)
    if not hasattr(base_logger, "handlers"):
        return False
    if not any(isinstance(h, logstash.TCPLogstashHandler) for h in base_logger.handlers):
        handler = logstash.TCPLogstashHandler(
            host=host,
            port=port,
            version=1,
            message_type=message_type
        )
        base_logger.addHandler(handler)
        return True
    return False

class LogstashLoggerMiddleware:
    """
    Scrapy middleware to configure Logstash logging for spiders.
    """
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        settings = get_project_settings()
        host = settings.get('LOGSTASH_HOST')
        port = settings.get('LOGSTASH_PORT')

        if not host or not port:
            spider.logger.warning("LOGSTASH_HOST or LOGSTASH_PORT not set in settings. Logstash logging will not be enabled.")
            return

        try:
            port = int(port)
        except ValueError:
            spider.logger.error(f"Invalid LOGSTASH_PORT: {port}. Must be an integer.")
            return

        # Configure Scrapy's root logger (often used by the engine)
        if configure_logstash_handler(logging.getLogger('scrapy'), host, port, 'scrapy'):
            spider.logger.info(f"Added Logstash handler to 'scrapy' logger: {host}:{port}")

        # Configure the spider's specific logger
        if hasattr(spider, 'logger') and configure_logstash_handler(spider.logger, host, port, f'scrapy_spider_{spider.name}'):
            spider.logger.info(f"Added Logstash handler to spider logger: {host}:{port}")

        # You might also want to add it to the root Python logger if you want all logs
        # from anywhere in your application to go to Logstash. Be careful with this,
        # as it can send a lot of data.
        # if configure_logstash_handler(logging.getLogger(), host, port, 'application_root'):
        #     spider.logger.debug(f"Added Logstash handler to root logger: {host}:{port}")


class UfcstatsScraperSpiderMiddleware:
    """
    Default spider middleware for the UFC Stats Scraper project.
    Contains methods to process spider input, output, and exceptions.
    """
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        # Must return an iterable of Request, or item objects.
        yield from result # Use yield from for clarity and efficiency

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        #
        # Should return either None or an iterable of Request or item objects.
        # If no custom exception handling is needed, this method can be omitted.
        spider.logger.error(f"Spider exception in {spider.name} for {response.url}: {exception}")
        pass # Returning None implicitly

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")


class UfcstatsScraperDownloaderMiddleware:
    """
    Default downloader middleware for the UFC Stats Scraper project.
    Contains methods to process requests, responses, and exceptions.
    """
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader middleware.
        # If no custom request processing is needed, this method can be omitted.
        return None # Continue processing this request

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # If no custom response processing is needed, this method can be omitted.
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
        # If no custom exception handling is needed, this method can be omitted.
        spider.logger.error(f"Downloader exception for {request.url} in {spider.name}: {exception}")
        pass # Returning None implicitly

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")