from shipman.scraper.gls import GlsScraper
from shipman.scraper.amazon import AmazonScraper
from shipman.scraper.dhl import DhlScraper
from shipman.scraper.base import BaseScraper
from typing import Dict, Type


scrapers: Dict[str, Type[BaseScraper]] = {
    GlsScraper.get_arg_name(): GlsScraper,
    AmazonScraper.get_arg_name(): AmazonScraper,
    DhlScraper.get_arg_name(): DhlScraper
}
