import datetime
import asyncio
from operator import truth

from _input.comments import gold_data
from evaluators.evaluator import evaluate_fact_checks
from factcheckers.checker_factory import checker_of
from pandas import json_normalize
from typing import Dict, List
from utils.types import CheckConditionAndResult, CheckerType, FactcheckDatasetItem, FactcheckResult, Truthiness, TypeAndCond, check_conditions, type_and_cond

CHECKER_TYPES: List[CheckerType] = [
    'site', 
    'web', 
    'llm'
]

async def process_method_cond_claim_async(method: CheckerType, condition_index: int, claims: List[str], manual_checks: List[FactcheckResult]) -> List[Dict[TypeAndCond, FactcheckResult]]:
    checker_results_list: List[Dict[TypeAndCond, FactcheckResult]] = []
    tasks: List[asyncio.Task] = []
    
    checker = checker_of(method)
    condition = checker.conditions()[condition_index]
    
    check_conditions[type_and_cond(method, condition_index)] = str(condition)
    
    tasks.append(asyncio.create_task(checker.check_one_condition(claims, condition)))
    
    results_list: List[List[FactcheckResult]] = await asyncio.gather(*tasks)
    results: List[FactcheckResult] = results_list[0]
    
    for i, result in enumerate(results):
        checker_result = {}
        checker_result[type_and_cond(method, condition_index)] = result
        checker_results_list.append(checker_result)
    
    return checker_results_list

async def main_async() -> None:
    claims: List[str] = []
    manual_checks: List[FactcheckResult] = []
    
    for i in range(len(gold_data)):
        claims.append(gold_data[i][0])
        truthiness: Truthiness = gold_data[i][1]
        reason_type: str = gold_data[i][2]
        reason_detail: str = gold_data[i][3]
        manual_checks.append(FactcheckResult(truthiness, reason_type, reason_detail))
    
    fact_check_dataset: List[FactcheckDatasetItem] = []
    
    for method in CHECKER_TYPES:
        checker = checker_of(method)
        conditions = checker.conditions()
        
        for condition_index in range(len(conditions)):
            tasks: List[asyncio.Task] = []
            tasks.append(asyncio.create_task(process_method_cond_claim_async(method, condition_index, claims, manual_checks)))
            
            checker_results_list = (await asyncio.gather(*tasks))[0]
            
            for i, claim in enumerate(claims):
                if i >= len(fact_check_dataset):
                    fact_check_dataset.append(FactcheckDatasetItem(claim, manual_checks[i], {}))
                
                fact_check_dataset[i].checker_judge.update(checker_results_list[i])
    
    evaluation: Dict[str, List[Dict[str, str | int | float]]] = evaluate_fact_checks(fact_check_dataset)

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
