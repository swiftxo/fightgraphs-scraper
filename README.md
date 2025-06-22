# FightGraphs Scraper

[](https://www.python.org/downloads/)
[](https://github.com/astral-sh/ruff)
[](https://opensource.org/licenses/MIT)

This repository contains the Scrapy-based web scraping component of the FightGraphs project. Its sole purpose is to gather raw Mixed Martial Arts (MMA) data from various public sources. It is designed to be modular, configurable, and scalable to accommodate new data sources over time.

The data extracted by these spiders is validated and cleaned at the source and is saved directly into a local MongoDB database via a custom pipeline.

## Key Features

  * **Multi-Source Scraping:** Spiders are organized by data source, allowing for targeted and maintainable scraping logic. (e.g., UFCStats, Tapology, etc.).
  * **Direct Database Storage:** Comes with a Scrapy pipeline to save validated items directly into a configured MongoDB database.
  * **Modern Dependency Management:** Uses [Poetry](https://python-poetry.org/) for robust dependency management and reproducible environments.



---
## Instructions will be added soon