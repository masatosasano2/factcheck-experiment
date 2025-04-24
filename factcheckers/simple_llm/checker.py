from utils.llm import ask_llm
from utils.types import CheckerType, FactcheckResult, Truthiness
from factcheckers.abstract_checker import AbstractChecker

class SimpleLLMChecker(AbstractChecker):
    def __init__(self, name: CheckerType):
        super().__init__(name)

    def check_one_condition(self, claim: str, condition: any = {}) -> FactcheckResult:
        print(f"Checking LLM...")
        prompt = f"""
        あなたはファクトチェックの専門家です。
        以下の主張が事実に基づいているかどうかを評価してください。
        主張: "{claim}"
        回答は以下のいずれかの形式で返してください："true"（事実に基づいている）, "false"（事実に反している）, "uncertain"（判断できない）
        """
        result: Truthiness = Truthiness.UNCERTAIN
        try:
            answer = ask_llm(prompt)
            if "true" in answer:
                result = Truthiness.TRUE
            elif "false" in answer:
                result = Truthiness.FALSE
            else:
                result = Truthiness.UNCERTAIN
        except Exception as e:
            print(f"Error checking llm: {e}")
            result = Truthiness.UNCERTAIN
        
        return FactcheckResult(result) # FIXME 理由を返すようにしたい