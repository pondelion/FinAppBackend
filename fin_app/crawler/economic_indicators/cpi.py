from .fred import FredCrawler


class CPICrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNCPIALLMINMEI'
