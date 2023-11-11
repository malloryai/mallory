
from .base import ScrapeMeta, ScrapeBase, ScrapeFactory
from .scrape_generic import ScrapeGeneric
from .scrape_bleeping_computer import ScrapeBleepingComputer
from .scrape_dark_reading import ScrapeDarkReading
from .scrape_greynoise import ScrapeGreynoise
from .scrape_help_net_security import ScrapeHelpNetSecurity
from .scrape_thn import ScrapeTHN


# If you want, you can also initialize package-wide variables.
scrapers_initialized = True

# You can also define functions, classes, or any other Python constructs 
# that you want to be available at the package level.
def show_registered_scrapers():
    return list(ScrapeFactory.registry.keys())