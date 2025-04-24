import pandas as pd

from utils.settings import CSE_ID, GCP_KEY
from utils.types import CheckerType, FactcheckResult, Truthiness
from factcheckers.abstract_checker import AbstractChecker
from googleapiclient.discovery import build

class SimpleWebChecker(AbstractChecker):
    def __init__(self, name: CheckerType):
        super().__init__(name)

    def check_one_condition(self, claim: str, condition: any = {}) -> FactcheckResult:
        print(f"Checking web...")

        result: Truthiness = Truthiness.UNCERTAIN
        try:
            service = build("customsearch", "v1", cache_discovery = False, developerKey = GCP_KEY)
            response = service.cse().list(q = "\"" + claim.replace(" ", "+") + "\"", cx = CSE_ID, num = 10, start = 0).execute()
            count = int(response['searchInformation']['totalResults'])

            if count == 0:
                result = Truthiness.FALSE # FIXME 検索されなければ偽、でいいのか？
            else:
                result = Truthiness.UNCERTAIN # 検索結果があるとしても、必ずしも正しいとは限らない
        except Exception as e:
            print(f"Error checking web: {e}")
            result = Truthiness.UNCERTAIN
        
        return FactcheckResult(result)