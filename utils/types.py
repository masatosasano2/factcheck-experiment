from enum import Enum

class Truthiness(Enum):
    TRUE = 1
    UNCERTAIN = 0
    FALSE = -1
    def val(self):
        return int(self.value)

class ReasonType(Enum):
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

class FactcheckResult: 
    def __init__(self, truthiness: Truthiness, reason_type: ReasonType, detail: str):
        self.truthiness = truthiness
        self.reason_type = reason_type
        self.detail = detail
