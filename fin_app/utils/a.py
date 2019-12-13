class BadCase:

    def __init__(self):
        self._a = 1
        self._b = 4.3

    def add(
        self,
        val: str  # ※
    ) -> None:
        self._a += val

    def sub(
        self,
        val: float
    ) -> float:
        self._b += val


class GoodCase:

    def __init__(self):
        self._a = 1
        self._b = 4.3

    def add(
        self,
        val: int  # ※
    ) -> None:
        self._a += val

    def sub(
        self,
        val: float
    ) -> None:
        self._b += val


if __name__ == '__main__':
    bc = BadCase()
    bc.add(10)
    bc.sub(2.3)

    gc = GoodCase()
    gc.add(10)
    gc.sub(2.3)
