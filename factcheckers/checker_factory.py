from factcheckers.abstract_checker import AbstractChecker
from factcheckers.simple_llm.checker import SimpleLLMChecker
from factcheckers.simple_web.checker import SimpleWebChecker
from factcheckers.target_site.checker import TargetSiteChecker
from utils.types import CheckerType

def checker_of(name: CheckerType) -> AbstractChecker:
    """
    Returns an instance of the specified checker type.
    """
    if name == "site":
        return TargetSiteChecker(name)
    elif name == "web":
        return SimpleWebChecker(name)
    elif name == "llm":
        return SimpleLLMChecker(name)
    else:
        raise ValueError(f"Unknown checker type: {name}")
