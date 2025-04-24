from enum import Enum
from typing import Dict, Literal

class Truthiness(Enum):
    # 真偽判定の結果
    TRUE = 1
    UNCERTAIN = 0
    FALSE = -1
    def val(self):
        return int(self.value)

class ReasonType(Enum):
    # 真偽判定の理由の種別
    FACT = "事実かどうか確定している"
    LOGIC = "そうでないケースもある" # 例：コメントに「必ず」「すべて」などとある
    CRITERIA = "判定基準による"
    INTERPRETATION = "事実の解釈による" # 例：法解釈、データの解釈
    CONTEXTUAL = "コメント文の意味による" # 例：文法的に意味が曖昧、文意が曖昧、単語の意味が曖昧
    DIFFICULT = "事実の確定が困難"
    STANDARD = "専門家の支配的意見"
    POLITICAL = "政治哲学による"
    PREDICTION = "未来予測にすぎない"
    UNDEFINED = "原理的に真偽のどちらでもない"
    NOT_TARGET = "ファクトチェックの対象外" # 当面は扱わなくていい前提
    UNKNOWN = "不明" 
    def val(self):
        return str(self.value)

type CheckerType = Literal['site', 'web', 'llm']

type TypeAndCond = str
''' Always use type_and_cond() to create this type '''
def type_and_cond(type: CheckerType, condition_index: int) -> TypeAndCond:
    return type + "_" + str(condition_index)

check_conditions: Dict[TypeAndCond, str] = {}
''' Global list of checked conditions for each checker type '''

class FactcheckResult: 
    ''' Result of AbstractChecker#check '''
    def __init__(self, truthiness: Truthiness, reason_type: ReasonType = ReasonType.UNKNOWN, reason_detail: str = ""):
        self.truthiness = truthiness
        self.reason_type = reason_type
        self.reason_detail = reason_detail

class CheckConditionAndResult:
    def __init__(self, condition_index: int, result: FactcheckResult):
        self.condition_index = condition_index
        self.result = result

class FactcheckDatasetItem:
    def __init__(self, claim: str, manual_judge: FactcheckResult, checker_judges: Dict[TypeAndCond, FactcheckResult]):
        self.claim = claim
        self.manual_judge = manual_judge
        self.checker_judge = checker_judges