import os
from datetime import datetime
from typing import Tuple
import gc

import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance


def creaet_candle_chart(
    opens: pd.Series,
    closes: pd.Series,
    highs: pd.Series,
    lows: pd.Series,
    width: int = 1,
    size: Tuple = (8, 8),
    filepath: str = None,
) -> str:
    """[summary]

    Args:
        opens (pd.Series): [description]
        closes (pd.Series): [description]
        highs (pd.Series): [description]
        lows (pd.Series): [description]
        width (int, optional): [description]. Defaults to 1.
        size (Tuple, optional): [description]. Defaults to (8, 8).
        filepath (str, optional): [description]. Defaults to None.

    Returns:
        str: [description]
    """
    fig = plt.figure(figsize=size)
    ax = plt.subplot()

    _ = mpl_finance.candlestick2_ohlc(
        ax,
        opens=opens,
        closes=closes,
        highs=highs,
        lows=lows,
        width=width, colorup='g', colordown='r'
    )

    plt.tick_params(
        bottom=False,
        left=False,
        right=False,
        top=False
    )
    plt.tick_params(
        labelbottom=False,
        labelleft=False,
        labelright=False,
        labeltop=False
    )

    ax.set_facecolor((0.0, 0.0, 0.0))
    plt.xlim(0-width//2, len(opens)+width//2)

    if not filepath:
        filepath = os.path.join(
            '/tmp/',
            f'ohlc_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png',
        )
    fig.savefig(filepath, bbox_inches="tight", pad_inches=0.0)

    plt.clf()
    plt.close(fig)
    gc.collect()

    return filepath
