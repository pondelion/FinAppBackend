from .fred import FredCrawler


class IndustrialProductionCrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNPROINDMISMEI'
