from utils.types import Truthiness, ReasonType

gold_data: list[str, Truthiness, ReasonType, str] = [
    ["日本の防衛費はGDPの2%を超えている。", Truthiness.FALSE, ReasonType.FACT, "2025年度で1.8%予定"],
    ["最低賃金を上げると失業率が必ず上がる。", Truthiness.FALSE, ReasonType.LOGIC, "「必ず」ではない"],
    ["温暖化は中国のせいだ。", Truthiness.UNCERTAIN, ReasonType.CONTEXTUAL, "部分的にそうだが、中国のみのせいではない"],
    ["新型コロナワクチンは5Gと関係している。", Truthiness.FALSE, ReasonType.FACT, "科学的に否定されている"],
    ["新型コロナウイルスは人工的に作られた。", Truthiness.UNCERTAIN, ReasonType.DIFFICULT, "自然発生説が有力だが、完全に否定はできない"],
    ["新型コロナウイルスはワクチンで治る。", Truthiness.FALSE, ReasonType.FACT, "予防効果があるが治療用ではない"],
    ["新型コロナウイルスは風邪の一種だ。", Truthiness.TRUE, ReasonType.FACT, "コロナウイルスの一種"],
    ["新型コロナウイルスはインフルエンザより危険だ。", Truthiness.UNCERTAIN, ReasonType.CRITERIA, "変異株によるし個人差も大きい"],
    ["消費税はすべて年金に使われている。", Truthiness.UNCERTAIN, ReasonType.UNDEFINED, "歳入と歳出の紐付けがない"],
    ["消費税は日本の経済を悪化させる。", Truthiness.UNCERTAIN, ReasonType.STANDARD, "経済学的には賛否両論"],
    ["消費税は日本の財政を改善する。", Truthiness.UNCERTAIN, ReasonType.STANDARD, "直接的には歳入増加に寄与する一方で、消費を減少させるなどの批判もある"],
    ["日本の国債は安全だ。", Truthiness.TRUE, ReasonType.STANDARD, "デフォルトリスクが低い"],
    ["日本の国債は危険だ。", Truthiness.FALSE, ReasonType.STANDARD, "デフォルトリスクが低い"],
    ["日本の国債は世界一だ。", Truthiness.UNCERTAIN, ReasonType.CRITERIA, "基準による"],
    ["台湾は日本の領土だった。", Truthiness.TRUE, ReasonType.FACT, "第二次世界大戦まで日本の統治下にあった"],
    ["アメリカは日本の防衛費を増やすように圧力をかけている。", Truthiness.TRUE, ReasonType.FACT, "アメリカの意向が影響している"],
    ["日本の自衛隊は憲法違反だ。", Truthiness.UNCERTAIN, ReasonType.INTERPRETATION, "憲法解釈による"],
    ["日本は核兵器を持つべきだ。", Truthiness.UNCERTAIN, ReasonType.POLITICAL, "賛否両論あり"],
    ["日本の年金制度は破綻する。", Truthiness.UNCERTAIN, ReasonType.CONTEXTUAL, "破綻の定義による"], 
    ["アメリカは選挙でAIを使って世論を操作している。", Truthiness.UNCERTAIN, ReasonType.DIFFICULT, "AIの利用は増えているが、世論操作の証拠はない"],
    ["日本の教育制度は世界一だ。", Truthiness.FALSE, ReasonType.CRITERIA, "基準による"],
    ["日本の医療制度は世界一だ。", Truthiness.FALSE, ReasonType.CRITERIA, "基準による"],
    ["日本の治安は世界一だ。", Truthiness.FALSE, ReasonType.CRITERIA, "基準による"],
    ["日本の経済成長率は先進国で最低だ。", Truthiness.TRUE, ReasonType.FACT, "OECD加盟国中で最低"],
    ["日本の人口は減少している。", Truthiness.TRUE, ReasonType.FACT, "継続的に人口減少している"],
    ["日本の出生率は1.5を下回っている。", Truthiness.TRUE, ReasonType.FACT, "2022年時点で1.34"],
    ["自民党の支持率は最近20%以下になった。", Truthiness.UNCERTAIN, ReasonType.CRITERIA, "朝日新聞の調査だと2024年末頃に19%台になったが、他の調査では20%を超えている"],
    ["日本の国債は世界一だ。", Truthiness.FALSE, ReasonType.STANDARD, "どの国債格付けランキングでも日本は最上位の評価ではない"],
    ["財務省はすべての国の借金を把握している。", Truthiness.FALSE, ReasonType.LOGIC, "「すべて」ではない"],
    ["憲法改正をすると戦争になる。", Truthiness.UNCERTAIN, ReasonType.PREDICTION, "予測に過ぎない"]
]
'''
正解データ。[コメント, 人力の正誤判定, 判定理由区分, 判定理由詳細]

TODO: CSVから読み込むようにする
'''