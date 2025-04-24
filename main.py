import datetime

from _input.comments import gold_data
from evaluators.evaluator import evaluate_fact_checks
from factcheckers.checker_factory import checker_of
from pandas import json_normalize
from typing import Dict
from utils.types import CheckerType, FactcheckDatasetItem, FactcheckResult, TypeAndCond, type_and_cond

CHECKER_TYPES: list[CheckerType] = [
    'site', 
    'web', 
    'llm'
] # 比べたいものだけ指定する

# 各手法でファクトチェック
fact_check_dataset: list[FactcheckDatasetItem] = []
for i in range(len(gold_data)):
    claim = gold_data[i][0]
    manual_check = FactcheckResult(gold_data[i][1], gold_data[i][2], gold_data[i][3])

    checker_results: Dict[TypeAndCond, FactcheckResult] = {}
    for method in CHECKER_TYPES:
        condAndResults = checker_of(method).check(claim)
        for condAndResult in condAndResults:
            checker_results[type_and_cond(method, condAndResult.condition_index)] = condAndResult.result

    fact_check_dataset.append(FactcheckDatasetItem(claim, manual_check, checker_results))

# スコアリング
evaluation = evaluate_fact_checks(fact_check_dataset)

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y%m%d%H%M')

with open("_output/summary_" + now + ".csv", "w", encoding="utf-8") as f:
    json_normalize(evaluation["summary"]).to_csv(f)

with open("_output/details_" + now + ".csv", "w", encoding="utf-8") as f:
    json_normalize(evaluation["details"]).to_csv(f)

print("評価結果を保存しました")
