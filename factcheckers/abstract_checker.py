from utils.types import FactcheckResult

class AbstractChecker:
    def __init__(self):
        """
        ファクトチェックの抽象クラス
        """
        pass

    def check(self, claim: str) -> FactcheckResult:
        """
        ファクトチェックを行うメソッド
        :param claim: チェック対象の主張
        :return: ファクトチェック結果
        """
        raise NotImplementedError("This method should be overridden by subclasses")
