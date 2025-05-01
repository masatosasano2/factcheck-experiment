from typing import final
from utils.types import CheckConditionAndResult, CheckerType, FactcheckResult, check_conditions, type_and_cond

class AbstractChecker:
    """
    ファクトチェックの抽象クラス
    """
    def __init__(self, method: CheckerType):
        self.method: CheckerType = method

    def conditions(self) -> list[dict]:
        """
        チェック条件を取得するメソッド
        :return: チェック条件のリスト
        """
        return [{}]

    async def check_one_condition(self, claims: list[str], condition: dict = {}) -> list[FactcheckResult]:
        """
        チェック条件に基づいてファクトチェックを実行するメソッド
        :param claims: チェック対象の主張のリスト
        :param condition: チェック条件
        :return: ファクトチェックの結果のリスト
        """
        raise NotImplementedError("This method should be overridden by subclasses")
