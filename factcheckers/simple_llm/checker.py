from utils.llm import ask_llm
from utils.types import FactcheckResult, ReasonType, Truthiness
from factcheckers.abstract_checker import AbstractChecker

class SimpleLLMChecker(AbstractChecker):
    def __init__(self):
        super().__init__()

    def check(self, claim: str) -> FactcheckResult:
        print(f"Checking LLM...")
        prompt = f"""
        あなたはファクトチェックの専門家です。
        以下の主張が事実に基づいているかどうかを評価してください。
        主張: "{claim}"
        回答は以下のいずれかの形式で返してください："true"（事実に基づいている）, "false"（事実に反している）, "uncertain"（判断できない）
        """
        result: Truthiness = Truthiness.UNCERTAIN
        try:
            answer = ask_llm(
                llm_type="openai",
                model="o4-mini",
                system_prompt="",
                user_prompt=prompt
            )
            if "true" in answer:
                result = Truthiness.TRUE
            elif "false" in answer:
                result = Truthiness.FALSE
            else:
                result = Truthiness.UNCERTAIN
        except Exception as e:
            print(f"Error checking llm: {e}")
            result = Truthiness.UNCERTAIN
        
        return FactcheckResult(
            truthiness=result,
            reason_type=ReasonType.UNKNOWN, # FIXME 答えさせる
            detail="LLMに質問" # FIXME 答えさせる
        )