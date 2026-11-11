#!/usr/bin/env python3
"""보고서 검증기. 사용법: python3 scripts/validate_report.py reports/2026-11-11.md
통과하면 종료 코드 0, 실패하면 1."""
import re
import sys

SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9_\-]{20,}", r"ghp_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
    r"AKIA[0-9A-Z]{16}", r"xox[baprs]-[A-Za-z0-9-]{10,}", r"[\w.+-]+@[\w-]+\.[\w.]+",
    r"(?i)(password|passwd|api[_-]?key|secret|token)\s*[:=]\s*\S{6,}",
]


def main(path):
    text = open(path, encoding="utf-8").read()
    errs = []
    if not re.match(r"# KMR Daily CEO Briefing — \d{4}-\d{2}-\d{2}\n", text):
        errs.append("제목이 'KMR Daily CEO Briefing — YYYY-MM-DD' 형식이 아님")
    for sec in ["## A.", "## B.", "## C.", "## D.", "## E."]:
        if sec not in text:
            errs.append(f"섹션 누락: {sec}")

    def section(letter):
        m = re.search(rf"## {letter}\..*?(?=\n## [A-F]\.|\Z)", text, re.S)
        return m.group(0) if m else ""

    a = section("A")
    if len(re.findall(r"^### A-\d", a, re.M)) != 3:
        errs.append("A: '### A-1~A-3' 업무가 정확히 3개여야 함")
    for kw in ["왜 중요", "예상 소요", "실행 방법"]:
        if a.count(kw) < 3:
            errs.append(f"A: 각 업무에 '{kw}' 필요")
    b = section("B")
    if len(re.findall(r"^\|\s*\d\s*\|", b, re.M)) != 5:
        errs.append("B: 표현 표(| 1 | ~ | 5 |) 5개 필요")
    for kw in ["영어", "흥미", "검수"]:
        if kw not in b:
            errs.append(f"B: '{kw}' 항목 누락")
    rows = re.findall(r"^\|\s*\d\s*\|.*$", b, re.M)
    for r in rows:
        if re.search(r"통과|검수\s*완료|확인됨|OK|✅", r) and "AI 초안" not in r:
            errs.append("B: 원어민 검수 없이 '통과/검수 완료' 표시 금지 → 'AI 초안 · 검수 필요' 사용: " + r[:30])
        elif "AI 초안 · 검수 필요" not in r and "검수 완료" not in r:
            errs.append("B: 각 표현 행에 'AI 초안 · 검수 필요'(또는 실제 검수 시 '검수 완료') 필요: " + r[:30])
    if any("검수 완료" in r for r in rows) and "reviewed/" not in b:
        errs.append("B: '검수 완료'는 reviewed/ 기록 근거를 함께 적을 때만 허용")
    if len(re.findall(r"카드\s*\d", b)) < 2 or not re.search(r"카드\s*1", b) or not re.search(r"카드\s*2\s*~\s*6", b):
        errs.append("B: 카드뉴스 템플릿 v1 설명(카드 1 / 카드 2~6) 필요")
    if re.search(r"CTA|저장·팔로우 유도|팔로우 유도|마무리 카드|훅 카드", b.replace("CTA 전용 카드 없음", "")):
        errs.append("B: 카드뉴스에 CTA/훅/마무리 등 별도 카드 금지(템플릿 v1)")
    c = section("C")
    if len(re.findall(r"^### C-\d", c, re.M)) != 2:
        errs.append("C: '### C-1, C-2' 주제 2개 필요")
    if not re.search(r"출처|아이디어|확인 불가", c):
        errs.append("C: 각 주제에 '출처' 또는 '아이디어(근거 미확인)' 표시 필요")
    d = section("D")
    for kw in ["예상 소요", "지표"]:
        if kw not in d:
            errs.append(f"D: '{kw}' 누락")
    e = section("E")
    for kw in ["홈페이지", "Threads", "학습상품", "Lemon Squeezy"]:
        if kw not in e:
            errs.append(f"E: '{kw}' 누락")
    if "확인 필요" not in e and "확인 불가" not in e:
        errs.append("E: 확인 못 한 항목에 '확인 필요/확인 불가' 표시 필요")
    for p in SECRET_PATTERNS:
        if re.search(p, text):
            errs.append(f"민감정보 의심 패턴 발견: {p}")
    if len(re.findall(r"[가-힣]", text)) < 300:
        errs.append("한국어 본문이 너무 적음")
    if errs:
        print("FAIL")
        for x in errs:
            print(" -", x)
        return 1
    print("PASS:", path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
