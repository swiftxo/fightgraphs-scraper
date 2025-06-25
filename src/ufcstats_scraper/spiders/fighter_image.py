import scrapy
from ufcstats_scraper.utils import get_fighter_collection_items
from ufcstats_scraper.items import FighterImageItem
import time


class FighterImageSpider(scrapy.Spider):
    name = "fighter_image"
    allowed_domains = ["www.ufc.com"]
    fighter_urls = get_fighter_collection_items(
        ["first_name", "last_name", "fighter_ufcstats_url"]
    )
    url_template = (
        "https://www.ufc.com/athlete/{first_name}-{last_name}"  # Lowercase names
    )

    def start_requests(self):
        for fighter in self.fighter_urls:
            first_name = fighter.get("first_name")
            last_name = fighter.get("last_name")
            if not first_name or not last_name:
                self.logger.warning(
                    f"Missing first or last name for fighter: {fighter}",
                    extra={
                        "event": "missing_fighter_name",
                        "spider": self.name,
                        "fighter": fighter,
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    },
                )
                continue
            first_name = first_name.lower()
            last_name = last_name.lower()
            fighter_ufcstats_url = fighter.get("fighter_ufcstats_url")
            url = self.url_template.format(first_name=first_name, last_name=last_name)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"fighter_ufcstats_url": fighter_ufcstats_url},
            )

    def parse(self, response):
        if response.status == 200:
            image_url = response.css("img.hero-profile__image::attr(src)").get()
            if image_url:
                self.logger.info(
                    f"Image found for {response.meta['fighter_ufcstats_url']}: {image_url}",
                    extra={
                        "event": "image_found",
                        "spider": self.name,
                        "url": response.url,
                        "fighter_ufcstats_url": response.meta["fighter_ufcstats_url"],
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    },
                )
                image_item = FighterImageItem()
                image_item["fighter_ufcstats_url"] = response.meta[
                    "fighter_ufcstats_url"
                ]
                image_item["fighter_image_url"] = image_url
                yield image_item
            else:
                self.logger.warning(
                    f"No image found for {response.meta['fighter_ufcstats_url']}",
                    extra={
                        "event": "no_image_found",
                        "spider": self.name,
                        "url": response.url,
                        "fighter_ufcstats_url": response.meta["fighter_ufcstats_url"],
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    },
                )
        else:
            self.logger.error(
                f"Failed to retrieve {response.meta['fighter_ufcstats_url']}: HTTP status {response.status}",
                extra={
                    "event": "fighter_image_failed",
                    "spider": self.name,
                    "url": response.url,
                    "fighter_ufcstats_url": response.meta["fighter_ufcstats_url"],
                    "metrics": {"http_status": response.status},
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                },
            )
