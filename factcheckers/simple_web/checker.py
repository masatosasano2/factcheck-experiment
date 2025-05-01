import pandas as pd

from utils.settings import CSE_ID, GCP_KEY
from utils.types import CheckerType, FactcheckResult, Truthiness
from factcheckers.abstract_checker import AbstractChecker
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import asyncio

class SimpleWebChecker(AbstractChecker):
    def __init__(self, name: CheckerType):
        super().__init__(name)

    async def check_one_condition(self, claims: list[str], condition: dict = {}) -> list[FactcheckResult]:
        print(f"Checking web asynchronously...")
        results = []
        
        for claim in claims:
            result: Truthiness = Truthiness.UNCERTAIN
            try:
                loop = asyncio.get_event_loop()
                service = await loop.run_in_executor(None, lambda: build("customsearch", "v1", developerKey=GCP_KEY))
                response = await loop.run_in_executor(None, lambda: service.cse().list(q=f'"{claim}"', cx=CSE_ID, num=10, start=1).execute())
                count = int(response.get('searchInformation', {}).get('totalResults', 0))

                if count == 0:
                    result = Truthiness.FALSE
                else:
                    result = Truthiness.UNCERTAIN
            except HttpError as e:
                print(f"HTTP error occurred: {e}")
            except Exception as e:
                print(f"Error checking web: {e}")
            
            results.append(FactcheckResult(result))
        
        return results
