

def test_authentication():
    from fin_app.crawler.twitter.api import API
    print(API.me())
