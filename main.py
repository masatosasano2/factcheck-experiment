import datetime
import asyncio

from _input.comments import gold_data
from evaluators.evaluator import evaluate_fact_checks
from factcheckers.checker_factory import checker_of
from pandas import json_normalize
from typing import Dict, List
from utils.types import CheckConditionAndResult, CheckerType, FactcheckDatasetItem, FactcheckResult, TypeAndCond, type_and_cond

CHECKER_TYPES: List[CheckerType] = [
    'site', 
    'web', 
    'llm'
]

async def process_claim_async(claim: str, manual_check: FactcheckResult) -> FactcheckDatasetItem:
    checker_results: Dict[TypeAndCond, FactcheckResult] = {}
    tasks: List[asyncio.Task] = []

    for method in CHECKER_TYPES:
        tasks.append(asyncio.create_task(checker_of(method).check(claim)))

    results: List[List[CheckConditionAndResult]] = await asyncio.gather(*tasks)

    for method, condAndResults in zip(CHECKER_TYPES, results):
        for condAndResult in condAndResults:
            checker_results[type_and_cond(method, condAndResult.condition_index)] = condAndResult.result

    return FactcheckDatasetItem(claim, manual_check, checker_results)

async def main_async() -> None:
    fact_check_dataset: List[FactcheckDatasetItem] = []
    tasks: List[asyncio.Task] = []

    for i in range(len(gold_data)):
        claim: str = gold_data[i][0]
        manual_check: FactcheckResult = FactcheckResult(gold_data[i][1], gold_data[i][2], gold_data[i][3])
        tasks.append(asyncio.create_task(process_claim_async(claim, manual_check)))

    fact_check_dataset = await asyncio.gather(*tasks)

    evaluation: Dict[str, List[Dict[str, any]]] = evaluate_fact_checks(fact_check_dataset)

    if evaluation and "summary" in evaluation and "details" in evaluation:
        now: str = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y%m%d%H%M')

        with open(f"_output/summary_{now}.csv", "w", encoding="utf-8") as summary_file:
            json_normalize(evaluation["summary"]).to_csv(summary_file)

        with open(f"_output/details_{now}.csv", "w", encoding="utf-8") as details_file:
            json_normalize(evaluation["details"]).to_csv(details_file)

        print("評価結果を保存しました")
    else:
        print("評価結果が正しく生成されませんでした")

asyncio.run(main_async())
