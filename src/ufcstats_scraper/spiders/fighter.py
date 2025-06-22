import scrapy

from ufcstats_scraper.items import FighterItem
from ufcstats_scraper.utils import clean_text

class FighterSpider(scrapy.Spider):
    name = "fighter"
    allowed_domains = ["www.ufcstats.com"]
    url_template = (
        "http://www.ufcstats.com/statistics/fighters?char={char}&page={page_num}"
    )

    char_range = "abcdefghijklmnopqrstuvwxyz"
    start_page = 1
    row_xpath = "//tbody/tr[@class='b-statistics__table-row' and not(td[@class='b-statistics__table-col_type_clear'])]"

    def start_requests(self):
        for char in self.char_range:
            yield scrapy.Request(
                url=self.url_template.format(char=char, page_num=self.start_page),
                callback=self.parse,
                cb_kwargs={"char": char, "page_num": self.start_page},
            )

    def parse(self, response, char, page_num):
        rows = response.xpath(self.row_xpath)
        if not rows:
            return

        for row in rows:
            fighter_ufcstats_url = clean_text(row.xpath("./td[1]/a/@href").get())
            first_name = clean_text(row.xpath("normalize-space(./td[1]/a/text())").get())
            last_name = clean_text(row.xpath("normalize-space(./td[2]/a/text())").get())
            nickname = clean_text(row.xpath("normalize-space(./td[3]/a/text())").get())
            height = clean_text(row.xpath("normalize-space(./td[4]/text())").get())
            weight = clean_text(row.xpath("normalize-space(./td[5]/text())").get())
            reach = clean_text(row.xpath("normalize-space(./td[6]/text())").get())
            stance = clean_text(row.xpath("normalize-space(./td[7]/text())").get())
            fighter_item = FighterItem()
            fighter_item.update({
                "fighter_ufcstats_url": fighter_ufcstats_url,
                "first_name": first_name,
                "last_name": last_name,
                "nickname": nickname,
                "height": height,
                "weight": weight,
                "reach": reach,
                "stance": stance,
            })

            request_url = response.urljoin(fighter_ufcstats_url)
            request = scrapy.Request(request_url, callback=self.parse_fighter_details)
            request.meta["fighter_item"] = fighter_item
            yield request

        next_page = page_num + 1
        yield scrapy.Request(
            url=self.url_template.format(char=char, page_num=next_page),
            callback=self.parse,
            cb_kwargs={"char": char, "page_num": next_page},
        )

    @staticmethod
    def parse_fighter_details(response):

        fighter_item = response.meta["fighter_item"]

        fighter_record = clean_text(
            response.xpath(
                "//text()[parent::*[@class='b-content__title-record']]"
            ).get()
        )
        date_of_birth = clean_text(
            response.xpath(
                "//li[i[normalize-space(text())='DOB:']]/text()[normalize-space()]"
            ).get()
        )

        fight_urls = []
        fights_table = response.xpath(
            "//table[contains(@class, 'b-fight-details__table')]"
        )
        if fights_table:
            fight_rows = fights_table.xpath(
                ".//tbody/tr[contains(@class, 'b-fight-details__table-row') and contains(@class, 'js-fight-details-click')]"
            )
            for row in fight_rows:
                link_href = row.xpath("./td[1]//a/@href").get()
                if link_href:
                    fight_urls.append(link_href.strip())

        fighter_item.update({
        "fighter_record": fighter_record,
        "date_of_birth": date_of_birth,
        "fight_urls": fight_urls,
        })

        yield fighter_item
