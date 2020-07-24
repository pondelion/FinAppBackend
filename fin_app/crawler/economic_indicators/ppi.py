from .fred import FredCrawler


class PPICrawler(FredCrawler):

    def _get_tag(self):
        return 'PITGCG01JPM661N'

    def _get_name(self):
        return 'ppi'
