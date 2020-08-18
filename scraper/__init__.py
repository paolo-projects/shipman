from scraper.gls import GlsScraper
from scraper.amazon import AmazonScraper
from scraper.dhl import DhlScraper
from scraper.basescraper import BaseScraper
from typing import Dict, Type


scrapers: Dict[str, Type[BaseScraper]] = {
    GlsScraper.get_arg_name(): GlsScraper,
    AmazonScraper.get_arg_name(): AmazonScraper,
    DhlScraper.get_arg_name(): DhlScraper
}
