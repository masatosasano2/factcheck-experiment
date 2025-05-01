from utils.llm import ask_llm
from utils.types import CheckerType, FactcheckResult, Truthiness
from factcheckers.abstract_checker import AbstractChecker
import requests
import httpx

class TargetSiteChecker(AbstractChecker):
    def __init__(self, name: CheckerType):
        super().__init__(name)

    async def check_one_condition(self, claims: list[str], condition: dict = {}) -> list[FactcheckResult]:
        print(f"Checking target sites asynchronously...")
        results = []
        
        for claim in claims:
            prompt = f"""
            政治的な主張に対してファクトチェックをしたいです。
            方法は、真偽を逆にした上で、Wikipedia記事にヒットしやすいように文章を簡略化します。
            簡略化の具体例は、少ない語数での言い換え、句読点の削除、不要な活用語尾の削除、などです。
            てにをはは省略しません。
            
            「{claim}」という主張について、上記の方針で簡略化してください。
            簡略化された文以外は回答しないでください。
            """
            inverse_claim = await ask_llm(prompt)
            print(f"Inverse claim: {inverse_claim}")

            url = "https://ja.wikipedia.org/w/rest.php/v1/search/page" # FIXME 指定された複数のサイトをチェックしたい
            params = {
                "q": "\"" + inverse_claim.replace(" ", "+") + "\"",
                "utf8": 1,
                "limit": 5,
            }
            result: Truthiness = Truthiness.UNCERTAIN
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    data = response.json()
                    if len(data["pages"]) > 0:
                        result = Truthiness.FALSE # 真偽を逆にしてヒットしたので、偽と判定
                    else:
                        result = Truthiness.UNCERTAIN
            except Exception as e:
                print(f"Error checking Wikipedia: {e}")
                result = Truthiness.UNCERTAIN
            
            results.append(FactcheckResult(result))
        
        return results
