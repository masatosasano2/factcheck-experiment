from annotated_types import T
from utils.types import FactcheckResult, ReasonType, Truthiness
from factcheckers.abstract_checker import AbstractChecker
import requests

class SimpleWebChecker(AbstractChecker):
    def __init__(self):
        super().__init__()

    def check(self, claim: str) -> FactcheckResult:
        print(f"Checking web...")
        headers = {"User-Agent": "Mozilla/5.0"}
        query = claim.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}"
        result: Truthiness = Truthiness.UNCERTAIN
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if "一致する情報が見つかりませんでした" in response.text:
                result = Truthiness.FALSE
            elif "についての情報" in response.text or "Wikipedia" in response.text:
                result = Truthiness.TRUE # FIXME 怪しすぎる。〇〇はデマ、の〇〇が検出されかねない
            else:
                result = Truthiness.UNCERTAIN
        except Exception as e:
            print(f"Error checking web: {e}")
            result = Truthiness.UNKNOWN
        
        return FactcheckResult(
            truthiness=result,
            reason_type=ReasonType.UNKNOWN,
            detail="Webを参照"
        )