# ステップ1: 仮のファクトチェックデータ作成用スクリプト
import json
import pandas as pd

from _input.comments import gold_data
from collections import Counter
from factcheckers.simple_llm.checker import SimpleLLMChecker
from factcheckers.simple_web.checker import SimpleWebChecker
from factcheckers.target_site.checker import TargetSiteChecker
from pandas import json_normalize
from typing import List, Dict
from utils.preprocess import extract_claims, extract_source
from utils.types import FactcheckResult

# 各ファクトチェック手法の結果を集める
fact_check_dataset = []
for i in range(len(gold_data)):
    comment = gold_data[i][0]
    truthiness = gold_data[i][1]
    reason_type = gold_data[i][2]
    detail = gold_data[i][3]

    item = {
        "original_comment": comment,
        "claim": extract_claims(comment)[0],  # FIXME 一旦 claims = commentとして実装を続けているが、後で要修正
        "source": extract_source(comment),
        "manual_judge": FactcheckResult(
            truthiness=truthiness,
            reason_type=reason_type,
            detail=detail
        ),
        "site_check": TargetSiteChecker().check(comment),
        "web_check": SimpleWebChecker().check(comment),
        "llm_check": SimpleLLMChecker().check(comment)
    }
    fact_check_dataset.append(item)

# ロジックごとの一致度集計
def evaluate_fact_checks(dataset: List[Dict]) -> Dict:
    results = {
        "site_check": Counter({'correct': 0, 'incorrect': 0, 'total': 0}),
        "web_check": Counter({'correct': 0, 'incorrect': 0, 'total': 0}),
        "llm_check": Counter({'correct': 0, 'incorrect': 0, 'total': 0})
    }
    detailed = []

    for item in dataset:
        true_label = item["manual_judge"].truthiness.val()
        for method in ["site_check", "web_check", "llm_check"]:
            pred = item[method].truthiness.val()
            if true_label == pred:
                results[method]["correct"] += 1
            else:
                results[method]["incorrect"] += 1
            results[method]["total"] += 1
        detailed.append({
            "claim": item["claim"],
            "true_label": true_label,
            "site": item["site_check"].truthiness.val(),
            "web": item["web_check"].truthiness.val(),
            "llm": item["llm_check"].truthiness.val()
        })
    
    summary_csv =[]
    for method in ["site_check", "web_check", "llm_check"]:
        summary_csv.append({
            "method": method,
            "correct": results[method]["correct"],
            "incorrect": results[method]["incorrect"],
            "total": results[method]["total"]
        })

    return {"summary": summary_csv, "details": detailed}

# 評価実行と保存
evaluation = evaluate_fact_checks(fact_check_dataset)

with open("_output/fact_check_evaluation_summary.json", "w", encoding="utf-8") as f:
    json_normalize(evaluation["summary"]).to_csv(f)

with open("_output/fact_check_evaluation_details.json", "w", encoding="utf-8") as f:
    json_normalize(evaluation["details"]).to_csv(f)

print("評価結果を保存しました")
