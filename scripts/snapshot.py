#!/usr/bin/env python3
"""읽기 전용 상태 스냅샷: 홈페이지와 Threads 공개 정보를 조회해 JSON으로 출력한다.

- GET 요청만 사용한다. 로그인·쓰기·게시 기능 없음. 인증 정보 불필요.
- 조회 실패 시 값을 추측하지 않고 "확인 불가"로 출력한다.
"""
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

HOME = "https://www.koreamadereal.com"
THREADS = "https://www.threads.com/@koreamadereal"
UA = "Mozilla/5.0 (compatible; kmr-briefing-readonly/1.0)"
UNKNOWN = "확인 불가"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status, r.read().decode("utf-8", "ignore")


def homepage():
    try:
        status, body = get(HOME)
        title = re.search(r"<title>(.*?)</title>", body, re.S)
        text = re.sub(r"(?s)<(script|style).*?</\1>", "", body)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
        text = re.sub(r"\s+", " ", text)
        return {
            "status": status,
            "title": html.unescape(title.group(1)).strip() if title else UNKNOWN,
            "has_coming_soon": "coming soon" in text.lower(),
            "text_excerpt": text[:600],
        }
    except Exception as e:  # noqa: BLE001
        return {"status": UNKNOWN, "error": type(e).__name__}


def threads():
    try:
        status, body = get(THREADS)
        m = re.search(r'og:description" content="([^"]*)', body)
        desc = html.unescape(m.group(1)) if m else ""
        f = re.search(r"([\d,\.KkMm]+)\s+Followers", desc)
        t = re.search(r"([\d,\.KkMm]+)\s+Threads", desc)
        return {
            "status": status,
            "followers": f.group(1) if f else UNKNOWN,
            "posts": t.group(1) if t else UNKNOWN,
            "bio": desc.split("•")[-1].strip() if desc else UNKNOWN,
            "note": "공개 메타 태그 기준. 조회수·도달·반응은 확인 불가(로그인 필요).",
        }
    except Exception as e:  # noqa: BLE001
        return {"status": UNKNOWN, "error": type(e).__name__}


if __name__ == "__main__":
    kst = datetime.now(timezone(timedelta(hours=9)))
    json.dump(
        {"checked_at_kst": kst.strftime("%Y-%m-%d %H:%M"), "homepage": homepage(), "threads": threads()},
        sys.stdout, ensure_ascii=False, indent=2,
    )
    print()
