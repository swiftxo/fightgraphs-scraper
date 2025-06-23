import scrapy
from ufcstats_scraper.items import EventItem
from ufcstats_scraper.utils import clean_text, format_date
import time

class EventSpider(scrapy.Spider):
    name = "event"
    allowed_domains = ["www.ufcstats.com"]
    start_urls = [
        "http://www.ufcstats.com/statistics/events/completed?page=all",
        "http://www.ufcstats.com/statistics/events/upcoming?page≤all",
    ]

    def parse(self, response):
        self.logger.info(
            "Spider started",
            extra={
                "event": "spider_started",
                "spider": self.name,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        )
        if "events/completed" in response.url:
            event_status = "completed"
        elif "events/upcoming" in response.url:
            event_status = "upcoming"
        else:
            event_status = "unknown"

        event_rows = response.xpath("//tr[@class='b-statistics__table-row']")
        self.logger.info(
            f"Found {len(event_rows)} event rows",
            extra={
                "event": "event_rows_found",
                "spider": self.name,
                "url": response.url,
                "metrics": {
                    "event_rows_found": len(event_rows)
                },
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        )

        for row in event_rows:
            event_name = row.xpath("td[1]/i/a/text()").get()
            event_ufcstats_url = row.xpath("td[1]/i/a/@href").get()
            event_date = row.xpath("td[1]/i/span/text()").get()
            event_location = row.xpath("td[2]/text()").get()
            if not event_ufcstats_url:
                self.logger.warning(
                    "Missing event URL in row",
                    extra={
                        "event": "missing_event_url",
                        "spider": self.name,
                        "row": row.get(),
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    }
                )
                continue
            event = EventItem()
            event["event_name"] = clean_text(event_name)
            event["event_ufcstats_url"] = clean_text(event_ufcstats_url)
            event["event_date"] = format_date(event_date)
            event["event_location"] = clean_text(event_location)
            event["event_status"] = event_status
            self.logger.info(
                "Requesting event details",
                extra={
                    "event": "requesting_event_details",
                    "spider": self.name,
                    "event_url": event["event_ufcstats_url"],
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
            )
            yield scrapy.Request(
                url=event["event_ufcstats_url"],
                callback=self.parse_fight_refs,
                meta={"event_item": event},
            )


    def parse_fight_refs(self,response):
        fight_refs = []
        rows = response.xpath("//tbody/tr[@data-link]")
        event_item = response.meta["event_item"]
        for card_position, row in enumerate(rows):
            fight_ufcstats_url = row.xpath("@data-link").get()
            if fight_ufcstats_url:
                fight_refs.append((fight_ufcstats_url, str(card_position)))
        event_item["fight_refs"] = fight_refs
        self.logger.info(
            f"Extracted {len(fight_refs)} fight refs for event",
            extra={
                "event": "fight_refs_extracted",
                "spider": self.name,
                "event_url": event_item["event_ufcstats_url"],
                "metrics": {
                    "fight_refs_extracted": len(fight_refs)
                },
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        )
        yield event_item