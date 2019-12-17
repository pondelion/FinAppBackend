import logging

formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(format=formatter)


class Logger:

    @staticmethod
    def d(tag: str, message: str):
        """debug log"""
        logger = logging.getLogger('fin_app')
        logger.setLevel(logging.DEBUG)
        logger.debug('[%s] %s', tag, message)

    @staticmethod
    def i(tag: str, message: str):
        """infomation log"""
        logger = logging.getLogger('fin_app')
        logger.setLevel(logging.INFO)
        logger.info('[%s] %s', tag, message)

    @staticmethod
    def e(tag: str, message: str):
        """error log"""
        logger = logging.getLogger('fin_app')
        logger.setLevel(logging.ERROR)
        logger.error('[%s] %s', tag, message)

    @staticmethod
    def w(tag: str, message: str):
        """warning log"""
        logger = logging.getLogger('fin_app')
        logger.setLevel(logging.WARNING)
        logger.warn('[%s] %s', tag, message)
