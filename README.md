# FightGraphs Scraper

[](https://www.python.org/downloads/)
[](https://github.com/astral-sh/ruff)
[](https://opensource.org/licenses/MIT)

This repository contains the Scrapy-based web scraping component of the FightGraphs project. Its sole purpose is to gather raw Mixed Martial Arts (MMA) data from various public sources. It is designed to be modular, configurable, and scalable to accommodate new data sources over time.

The data extracted by these spiders is validated at the source using Pydantic models and is saved directly into a local MongoDB database via a custom pipeline.

## Key Features

  * **Multi-Source Scraping:** Spiders are organized by data source, allowing for targeted and maintainable scraping logic. (e.g., UFCStats, Tapology, etc.).
  * **Data Validation at Source:** Leverages Pydantic models to ensure that scraped data conforms to a predefined schema before being saved, preventing "garbage" data from entering the database.
  * **Direct Database Storage:** Comes with a Scrapy pipeline to save validated items directly into a configured MongoDB database.
  * **Centrally Configured Spiders:** Key spider settings like download delays and user agents are managed in a central `config/spiders.yml` file for easy editing.
  * **Modern Dependency Management:** Uses [Poetry](https://python-poetry.org/) for robust dependency management and reproducible environments.

## Architecture Overview

This project follows a "Smart Scraper" philosophy. Each spider is responsible not only for extracting data but also for ensuring its basic structure and types are correct. This is achieved by:

1.  Defining data structures as **Pydantic Models** in `items.py`.
2.  Spiders inheriting from a **Base Spider** (`spiders/base.py`) which provides shared helper methods.
3.  A **MongoDB Pipeline** in `pipelines.py` that takes the validated items and saves them as documents in the specified collection.


---
## Instructions will be added soon