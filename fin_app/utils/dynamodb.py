import copy
from typing import Dict
import json
from decimal import Decimal


def format_data(data: Dict):
    data = empty2null(data)
    return json.loads(json.dumps(data), parse_float=Decimal)


def empty2null(data: Dict):
    """[summary]

    Args:
        data (Dict): [description]

    Returns:
        [type]: [description]
    """
    ret = copy.deepcopy(data)

    if isinstance(data, dict):
        for k, v in ret.items():
            ret[k] = format_data(v)

    # convert empty string to null
    if data == '':
        ret = None

    return ret
