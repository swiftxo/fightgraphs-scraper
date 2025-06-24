import scrapy
from ufcstats_scraper.utils import clean_text, get_fight_urls
from ufcstats_scraper.items import FightItem
import time as Time


class FightSpider(scrapy.Spider):
    name = "fight"
    allowed_domains = ["www.ufcstats.com"]
    start_urls = get_fight_urls()

    def parse(self, response):
        start_time = Time.time()
        self.logger.info(
            f"Parsing fight details from {response.url}",
            extra={
                "event": "parse_fight_details_started",
                "spider": self.name,
                "url": response.url,
                "timestamp": Time.strftime("%Y-%m-%dT%H:%M:%SZ", Time.gmtime()),
            },
        )
        fight_item = FightItem()
        fight_ufcstats_url = response.url
        fighter_xpath = "//div[@class='b-fight-details__persons clearfix']/div[@class='b-fight-details__person']"
        for i in [1, 2]:
            xpath = f"{fighter_xpath}[{i}]"
            name = clean_text(
                response.xpath(
                    f"{xpath}//h3[@class='b-fight-details__person-name']/a/text()[normalize-space()]"
                ).get()
            )
            nickname = clean_text(
                response.xpath(
                    f"{xpath}//p[@class='b-fight-details__person-title']/text()[normalize-space()]"
                ).get()
            )
            fighter_ufcstats_url = clean_text(
                response.xpath(
                    f"{xpath}//h3[@class='b-fight-details__person-name']/a/@href"
                ).get()
            )
            fighter_status = clean_text(
                response.xpath(
                    f"{xpath}/i[contains(@class, 'b-fight-details__person-status')]/text()[normalize-space()]"
                ).get()
            )

        fighter_xpath = "//div[@class='b-fight-details__persons clearfix']/div[@class='b-fight-details__person']"
        for i in [1, 2]:
            xpath = f"{fighter_xpath}[{i}]"

            fight_item[f"fighter{i}"] = {
                "name": name,
                "nickname": nickname,
                "fighter_ufcstats_url": fighter_ufcstats_url,
                "fighter_status": fighter_status,
            }

            self.logger.debug(
                f"Scraped fighter{i} details for fight {response.url}",
                extra={
                    "event": f"fighter{i}_details_scraped",
                    "spider": self.name,
                    "fight_url": response.url,
                    "fighter_name": name,
                    "timestamp": Time.strftime("%Y-%m-%dT%H:%M:%SZ", Time.gmtime()),
                },
            )

        general_xpath = "//div[@class='b-fight-details__content']"
        event_ufcstats_url = clean_text(
            response.xpath('//a[@class="b-link"]/@href').get()
        )

        method = clean_text(
            response.xpath(
                f"{general_xpath}//i[@class='b-fight-details__label' and normalize-space(.)='Method:']/following-sibling::i[1]/text()[normalize-space()]"
            ).get()
        )
        time = clean_text(
            response.xpath(
                f"{general_xpath}//i[@class='b-fight-details__label' and normalize-space(.)='Round:']/parent::i/text()[normalize-space()][1]"
            ).get()
        )

        time_format = clean_text(
            response.xpath(
                f"{general_xpath}//i[@class='b-fight-details__label' and normalize-space(.)='Time format:']/parent::i/text()[normalize-space()][1]"
            ).get()
        )

        referee = clean_text(
            response.xpath(
                f"{general_xpath}//i[@class='b-fight-details__label' and normalize-space(.)='Referee:']/following-sibling::span[1]/text()[normalize-space()]"
            ).get()
        )

        finish_details = clean_text(
            response.xpath(
                f"{general_xpath}//i[@class='b-fight-details__label' and normalize-space(.)='Details:']/parent::*/following-sibling::text()[normalize-space()][1]"
            ).get()
        )

        fight_of_the_night = clean_text(
            response.xpath(
                "boolean(//i[@class='b-fight-details__fight-title']/img[contains(@src, 'fight.png')])"
            ).get()
        )
        performance_of_the_night = clean_text(
            response.xpath(
                "boolean(//i[@class='b-fight-details__fight-title']/img[contains(@src, 'perf.png')])"
            ).get()
        )

        weight_class = clean_text(
            clean_text(
                response.xpath(
                    "//div[@class='b-fight-details__fight-head']/i[@class='b-fight-details__fight-title']/text()[normalize-space()]"
                ).get()
            )
        )
        title_fight = clean_text(
            clean_text(
                response.xpath(
                    "boolean(//div[@class='b-fight-details__fight-head']/i[@class='b-fight-details__fight-title']/img[contains(@src, 'belt.png')])"
                ).get()
            )
        )

        judge_xpath = (
            "//p[@class='b-fight-details__text'][i[normalize-space(.)='Details:']]"
        )

        judge1_name = clean_text(
            response.xpath(
                f"{judge_xpath}/i[@class='b-fight-details__text-item'][1]/span/text()[normalize-space()]"
            ).get()
        )
        judge1_score = clean_text(
            response.xpath(
                f"{judge_xpath}/i[@class='b-fight-details__text-item'][1]/text()[normalize-space()]"
            ).get()
        )
        judge2_name = clean_text(
            response.xpath(
                f"{judge_xpath}/i[@class='b-fight-details__text-item'][2]/span/text()[normalize-space()]"
            ).get()
        )
        judge2_score = clean_text(
            response.xpath(
                f"{judge_xpath}/i[@class='b-fight-details__text-item'][2]/text()[normalize-space()]"
            ).get()
        )
        judge3_name = clean_text(
            response.xpath(
                f"{judge_xpath}/i[@class='b-fight-details__text-item'][3]/span/text()[normalize-space()]"
            ).get()
        )

        judge3_score = clean_text(
            response.xpath(
                f"{judge_xpath}/i[@class='b-fight-details__text-item'][3]/text()[normalize-space()]"
            ).get()
        )

        fight_details = {
            "event_ufcstats_url": event_ufcstats_url,
            "method": method,
            "time": time,
            "time_format": time_format,
            "referee": referee,
            "finish_details": finish_details,
            "fight_of_the_night": fight_of_the_night,
            "performance_of_the_night": performance_of_the_night,
            "weight_class": weight_class,
            "title_fight": title_fight,
            "judge1_name": judge1_name,
            "judge1_score": judge1_score,
            "judge2_name": judge2_name,
            "judge2_score": judge2_score,
            "judge3_name": judge3_name,
            "judge3_score": judge3_score,
        }

        self.logger.debug(
            f"Scraped general fight details for {response.url}",
            extra={
                "event": "general_fight_details_scraped",
                "spider": self.name,
                "fight_url": response.url,
                "details": fight_details,
                "timestamp": Time.strftime("%Y-%m-%dT%H:%M:%SZ", Time.gmtime()),
            },
        )

        rounds = ["Round 1", "Round 2", "Round 3", "Round 4", "Round 5"]
        total_stats_xpath = "//table[contains(@class, 'b-fight-details__table') and contains(@class, 'js-fight-table')]"
        sig_strikes_totals_xpath = "(//table[contains(@class, 'b-fight-details__table') and contains(@class, 'js-fight-table')])[2]"

        fight_stats = {}
        for round_name in rounds:
            if not response.xpath(
                f"{total_stats_xpath}/tbody/thead[th[normalize-space(.)='{round_name}']]"
            ):
                self.logger.debug(
                    f"Round {round_name} not found for fight {response.url}, skipping.",
                    extra={
                        "event": "round_not_found",
                        "spider": self.name,
                        "fight_url": response.url,
                        "round": round_name,
                        "timestamp": Time.strftime("%Y-%m-%dT%H:%M:%SZ", Time.gmtime()),
                    },
                )
                continue

            round_xpath = f"{total_stats_xpath}/tbody/thead[th[normalize-space(.)='{round_name}']]/following-sibling::tr[1]"
            sig_round_xpath = f"{sig_strikes_totals_xpath}/tbody/thead[th[normalize-space(.)='{round_name}']]/following-sibling::tr[1]"

            # Extract round number from "Round X"

            fight_stats[round_name] = {
                "fighter1": {},
                "fighter2": {},
            }

            for i in [1, 2]:
                # Get fighter link
                fighter_ufcstats_url = fight_item[f"fighter{i}"]["fighter_ufcstats_url"]

                # Extract basic stats
                kd = clean_text(
                    response.xpath(f"{round_xpath}/td[2]/p[{i}]/text()").get()
                )
                sig_strikes = clean_text(
                    response.xpath(f"{round_xpath}/td[3]/p[{i}]/text()").get()
                )
                total_strikes = clean_text(
                    response.xpath(f"{round_xpath}/td[5]/p[{i}]/text()").get()
                )
                takedowns = clean_text(
                    response.xpath(f"{round_xpath}/td[6]/p[{i}]/text()").get()
                )
                sub_attempts = clean_text(
                    response.xpath(f"{round_xpath}/td[8]/p[{i}]/text()").get()
                )
                reversals = clean_text(
                    response.xpath(f"{round_xpath}/td[9]/p[{i}]/text()").get()
                )
                control_time = clean_text(
                    response.xpath(f"{round_xpath}/td[10]/p[{i}]/text()").get()
                )

                # Extract detailed strike stats
                head_strikes = clean_text(
                    response.xpath(f"{sig_round_xpath}/td[4]/p[{i}]/text()").get()
                )
                body_strikes = clean_text(
                    response.xpath(f"{sig_round_xpath}/td[5]/p[{i}]/text()").get()
                )
                leg_strikes = clean_text(
                    response.xpath(f"{sig_round_xpath}/td[6]/p[{i}]/text()").get()
                )
                distance_strikes = clean_text(
                    response.xpath(f"{sig_round_xpath}/td[7]/p[{i}]/text()").get()
                )
                clinch_strikes = clean_text(
                    response.xpath(f"{sig_round_xpath}/td[8]/p[{i}]/text()").get()
                )
                ground_strikes = clean_text(
                    response.xpath(f"{sig_round_xpath}/td[9]/p[{i}]/text()").get()
                )

                fight_stats[round_name][f"fighter{i}"] = {
                    "kd": kd,
                    "fighter_ufcstats_url": fighter_ufcstats_url,
                    "sig_strikes": sig_strikes,
                    "total_strikes": total_strikes,
                    "takedowns": takedowns,
                    "sub_attempts": sub_attempts,
                    "reversals": reversals,
                    "control_time": control_time,
                    "head_strikes": head_strikes,
                    "body_strikes": body_strikes,
                    "leg_strikes": leg_strikes,
                    "distance_strikes": distance_strikes,
                    "clinch_strikes": clinch_strikes,
                    "ground_strikes": ground_strikes,
                }
                self.logger.debug(
                    f"Scraped round {round_name} stats for fighter {i} in fight {response.url}",
                    extra={
                        "event": "round_stats_scraped",
                        "spider": self.name,
                        "fight_url": response.url,
                        "round": round_name,
                        "fighter": i,
                        "stats": fight_stats[round_name][f"fighter{i}"],
                        "timestamp": Time.strftime("%Y-%m-%dT%H:%M:%SZ", Time.gmtime()),
                    },
                )

        fight_item["fight_ufcstats_url"] = fight_ufcstats_url
        fight_item["fight_details"] = fight_details
        fight_item["fight_stats"] = fight_stats
        elapsed = int((Time.time() - start_time) * 1000)
        self.logger.info(
            f"Finished parsing fight details from {response.url}",
            extra={
                "event": "parse_fight_details_finished",
                "spider": self.name,
                "url": response.url,
                "metrics": {"processing_time_ms": elapsed},
                "timestamp": Time.strftime("%Y-%m-%dT%H:%M:%SZ", Time.gmtime()),
            },
        )
        yield fight_item
