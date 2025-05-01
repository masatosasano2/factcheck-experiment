from typing import final
from utils.types import CheckConditionAndResult, CheckerType, FactcheckResult, check_conditions, type_and_cond

class AbstractChecker:
    """
    ファクトチェックの抽象クラス
    """
    def __init__(self, method: CheckerType):
        self.method: CheckerType = method

    def conditions(self) -> list[any]:
        """
        チェック条件を取得するメソッド
        :return: チェック条件のリスト
        """
        return [{}]

    async def check_one_condition(self, claim: str, condition: any = {}) -> FactcheckResult:
        """
        チェック条件に基づいてファクトチェックを実行するメソッド
        :param claim: チェック対象の主張
        :param condition: チェック条件
        :return: ファクトチェックの結果
        """
        raise NotImplementedError("This method should be overridden by subclasses")
    
    @final
    async def check(self, claims: list[str]) -> list[list[CheckConditionAndResult]]:
        """
        ファクトチェックを実行するメソッド
        :param claims: チェック対象の主張のリスト
        :return: ファクトチェックの結果のリスト（claim毎にCheckConditionAndResultのリスト）
        """
        all_results: list[list[CheckConditionAndResult]] = []
        conditions = self.conditions()
        
        for claim in claims:
            check_results: list[CheckConditionAndResult] = []
            for idx in range(len(conditions)):
                condition = self.conditions()[idx]
                global check_conditions
                check_conditions[type_and_cond(self.method, idx)] = str(condition)
                result = await self.check_one_condition(claim, condition)
                check_results.append(CheckConditionAndResult(idx, result))
            all_results.append(check_results)
            
        return all_results
