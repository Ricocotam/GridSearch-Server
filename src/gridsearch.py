"""Different parameter searching functions.

This module aims to have multiple functions to do parameters search.
The functions defined here are only used to get parameters. 
When possible, generators are preferred.
"""
import itertools
from typing import Dict, Sequence, Any

import utils

ParameterSet = Dict[str, Any]
ParameterPossibilities = Dict[str, Sequence[Any]]

def listing(*list_sets: Sequence[ParameterSet]
            ) -> ParameterSet:
    """Yields a list of combinations.

    The only purpose here is to have a function so imports are clean.

    Parameters
    -----------
        list_sets : list of the combinations
    
    Examples
    ---------
    >>> parameters = [{"param1": 2, "param2": "easy"}, {"param1": 2, "param2": "hard"}]
    >>> for item in listing(*parameters):
    >>>    print(item)
    {"param1": 2, "param2": "easy"}
    {"param1": 2, "param2": "hard"}
    """
    for item in list_sets:
        yield item


def product(**kwargs: ParameterPossibilities
            ) -> ParameterSet:
    """The classical gridsearch.

    From a list of parameters do every combination possible.

    Parameters
    -----------
        kwargs : dict of parameters with all possibilities

    Example
    --------
    >>> gen = product(param1=[1, 2, 3, 4], param2=["easy", "hard", "super-hard"])
    >>> for item in gen:
    >>>    print(item)
    {"param1": 1, "param2": "easy"}
    {"param1": 2, "param2": "easy"}
    {"param1": 3, "param2": "easy"}
    {"param1": 4, "param2": "easy"}
    {"param1": 1, "param2": "hard"}
    ...
    {"param1": 4, "param2": "super-hard"}
    """
    for item in utils.kwargs_product(kwargs):
        yield item