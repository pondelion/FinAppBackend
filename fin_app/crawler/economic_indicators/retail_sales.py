from .fred import FredCrawler


class RetailSalesCrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNSARTMISMEI'
