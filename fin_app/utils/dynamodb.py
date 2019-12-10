import copy
from typing import Dict


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
            ret[k] = empty2null(v)

    if data == '':
        ret = None

    return ret
