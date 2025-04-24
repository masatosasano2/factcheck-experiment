from tabnanny import check
from typing import Counter, List, Dict
from utils.types import check_conditions, FactcheckDatasetItem, FactcheckResult, Truthiness, TypeAndCond

# 手法ごとに評価指標を求める
def evaluate_fact_checks(dataset: List[FactcheckDatasetItem]) -> Dict:
    print("Evaluating fact checks...")
    
    raw_scores: Dict[TypeAndCond, Counter] = {}
    details = []

    for item in dataset:
        correct_truthiness = item.manual_judge.truthiness
        checker_results: Dict[TypeAndCond, FactcheckResult] = item.checker_judge
        detail = {
            "claim": item.claim,
            "reason": item.manual_judge.reason_type.val(),
            "detail": item.manual_judge.reason_detail,
            "correct_truthiness": correct_truthiness.val(),
        }
        for typeAndCond in checker_results.keys():
            if typeAndCond not in raw_scores.keys():
                raw_scores[typeAndCond] = Counter({'total': 0, 'true': 0, 'false': 0, 'uncertain': 0, 'false_fake_judge': 0, 'missed_fake_judge': 0})

            raw_scores[typeAndCond]["total"] += 1
            if correct_truthiness == Truthiness.TRUE:
                raw_scores[typeAndCond]["true"] += 1
            elif correct_truthiness == Truthiness.FALSE:
                raw_scores[typeAndCond]["false"] += 1
            elif correct_truthiness == Truthiness.UNCERTAIN:
                raw_scores[typeAndCond]["uncertain"] += 1

            pred = checker_results[typeAndCond].truthiness
            if correct_truthiness != Truthiness.FALSE and pred == Truthiness.FALSE:
                raw_scores[typeAndCond]["false_fake_judge"] += 1
            elif correct_truthiness == Truthiness.FALSE and pred != Truthiness.FALSE:
                raw_scores[typeAndCond]["missed_fake_judge"] += 1

            detail[typeAndCond] = pred.val()
        details.append(detail)

    summary =[]
    global check_conditions
    for typeAndCond in raw_scores.keys():
        print(f"Evaluating {typeAndCond}...")
        
        total = raw_scores[typeAndCond]["total"]
        true = raw_scores[typeAndCond]["true"]
        false = raw_scores[typeAndCond]["false"]
        uncertain = raw_scores[typeAndCond]["uncertain"]
        false = 1 if false == 0 else false
        not_false = 1 if true + uncertain == 0 else true + uncertain

        false_fake_judge = raw_scores[typeAndCond]["false_fake_judge"]
        missed_fake_judge = raw_scores[typeAndCond]["missed_fake_judge"]
        false_fake_judge_rate = round(false_fake_judge / not_false, 5)
        missed_fake_judge_rate = round(missed_fake_judge / false, 5)
        condition: str = check_conditions[typeAndCond]
        summary.append({
            "method": typeAndCond.split("_")[0],
            "condition": condition,
            "count": total,
            "false_fake_judge_rate": false_fake_judge_rate,
            "missed_fake_judge_rate": missed_fake_judge_rate,
        })

    return {"summary": summary, "details": details}
