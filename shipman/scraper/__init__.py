from shipman.scraper.gls import GlsScraper
from shipman.scraper.amazon import AmazonScraper
from shipman.scraper.dhl import DhlScraper
from shipman.scraper.tnt import TntScraper
from shipman.scraper.brt import BrtScraper
from shipman.scraper.poste import PosteScraper
from shipman.scraper.base import BaseScraper
from typing import Dict, Type


scrapers: Dict[str, Type[BaseScraper]] = {
    GlsScraper.get_arg_name(): GlsScraper,
    AmazonScraper.get_arg_name(): AmazonScraper,
    DhlScraper.get_arg_name(): DhlScraper,
    TntScraper.get_arg_name(): TntScraper,
    BrtScraper.get_arg_name(): BrtScraper,
    PosteScraper.get_arg_name(): PosteScraper,
}
