# kmr-daily-ceo-briefing

**KOREA MADE REAL** 대표를 위한 매일 아침 비즈니스 브리핑 자동화 저장소입니다.
Claude Code **클라우드 루틴(Scheduled task)** 이 매일 오전 9시(Asia/Seoul)에 이 저장소를 열어 `KMR Daily CEO Briefing — YYYY-MM-DD` 보고서를 생성합니다. 로컬 PC가 꺼져 있어도 실행됩니다.

> 이 저장소는 홈페이지·학습자료 프로젝트와 **분리된 자동화 전용 저장소**입니다.

## 구성

| 파일 | 설명 |
|---|---|
| `BUSINESS_MODEL.md` | 브랜드·사업 목표·현재 상황 (보고서의 사실 기준) |
| `BRIEFING_RULES.md` | 보고서 형식, 안전 규칙, 팩트체크 규칙 |
| `ROUTINE_PROMPT.md` | 클라우드 루틴에 등록된 프롬프트 사본 |
| `scripts/snapshot.py` | 홈페이지·Threads 공개 정보를 읽기 전용으로 조회 |
| `scripts/validate_report.py` | 생성된 보고서의 형식·민감정보 검증 |
| `examples/` | 예시 보고서 |
| `reports/` | 매일 생성되는 보고서 (`YYYY-MM-DD.md`) |

## 사용

```bash
python3 scripts/snapshot.py                         # 공개 상태 조회 (읽기 전용)
python3 scripts/validate_report.py reports/2026-11-11.md   # 보고서 검증
```

## 안전 원칙

읽기·분석·보고서 생성만 합니다. SNS 게시, 이메일/DM 발송, 고객 연락, 결제·상품 등록, 운영 홈페이지·PDF 수정, 외부 시스템 변경은 **하지 않습니다.** 비밀번호·API 키·토큰·개인정보는 저장소에 기록하지 않습니다. 자세한 내용은 `BRIEFING_RULES.md`.

## 참고

- 이 저장소는 공개(public)입니다. 보고서에 비공개 매출·고객 정보를 넣지 마세요.
- 예약 설정(루틴)은 저장소 코드가 아니라 Claude Code 계정에 저장됩니다. 확인: claude.ai/code → Scheduled / Routines.
