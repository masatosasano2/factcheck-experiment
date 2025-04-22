from annotated_types import T
from utils.types import FactcheckResult, ReasonType, Truthiness
from factcheckers.abstract_checker import AbstractChecker
import requests

class TargetSiteChecker(AbstractChecker):
    def __init__(self):
        super().__init__()

    def check(self, claim: str) -> FactcheckResult:
        print(f"Checking target sites...")
        url = "https://ja.wikipedia.org/w/api.php" # FIXME 指定された複数のサイトをチェックしたい
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": claim,
            "utf8": 1
        }
        result: Truthiness = Truthiness.UNCERTAIN
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data["query"]["search"]:
                result = Truthiness.TRUE
            else:
                result = Truthiness.UNCERTAIN # FIXME このやり方だと決して偽と判定されない
        except Exception as e:
            print(f"Error checking Wikipedia: {e}")
            result = Truthiness.UNKNOWN
        
        return FactcheckResult(
            truthiness=result,
            reason_type=ReasonType.UNKNOWN,
            detail="Wikipediaを参照"
        )