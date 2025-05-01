from utils.llm import ask_llm
from utils.types import CheckerType, FactcheckResult, Truthiness
from factcheckers.abstract_checker import AbstractChecker

class SimpleLLMChecker(AbstractChecker):
    def __init__(self, name: CheckerType):
        super().__init__(name)

    async def check_one_condition(self, claims: list[str], condition: dict = {}) -> list[FactcheckResult]:
        print(f"Checking LLM asynchronously...")
        results = []
        
        for claim in claims:
            prompt = f"""
            あなたはファクトチェックの専門家です。
            以下の主張が事実に基づいているかどうかを評価してください。
            主張: "{claim}"
            回答は以下のいずれかの形式で返してください："true", "false", "uncertain"
            """
            result: Truthiness = Truthiness.UNCERTAIN
            try:
                answer = await ask_llm(prompt)
                if "true" in answer:
                    result = Truthiness.TRUE
                elif "false" in answer:
                    result = Truthiness.FALSE
                else:
                    result = Truthiness.UNCERTAIN
            except Exception as e:
                print(f"Error checking llm: {e}")
                result = Truthiness.UNCERTAIN
            
            results.append(FactcheckResult(result)) # FIXME 理由を返すようにしたい
        
        return results
