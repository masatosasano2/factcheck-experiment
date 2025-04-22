
import re
from typing import List

def extract_claims(comment: str) -> List[str]:
    claims = []
    claims.append(comment) # TODO 後回し
    return claims
    # 単純なヒューリスティック：句点区切り＋主張っぽい文
    # sentences = [s.strip() for s in comment.split("。") if s.strip()]
    # claims = []
    # for s in sentences:
    #     # パターン1: AだからBだ → A部分を取り出す
    #     m = re.search(r'(.+?)だから.+?だ', s)
    #     if m:
    #         claims.append(m.group(1) + "だ")
    #         continue
    #     # パターン2: CなD → DはCだ
    #     m = re.search(r'(.+?)な(.+)', s)
    #     if m:
    #         claims.append(f"{m.group(2)}は{m.group(1)}だ")
    #         continue
    #     # デフォルト：そのまま主張と見なす
    #     if any(kw in s for kw in ["は", "が", "する", "なる"]):
    #         claims.append(s)
    # return claims

def extract_source(claim: str) -> str:
    return "" # TODO 後回し
    # match = re.search(r'(https?://\S+|出典：[^\s。、]+|引用：[^\s。、]+)', claim)
    # return match.group(0) if match else ""
