# M5 Prompt Card (Executive Reporting)

## 목적

M1~M4 결과를 경영진 의사결정용 보고 형태로 통합한다.

## 1) 입력 컨텍스트 (값만 교체)

```text
[M5 일반 컨텍스트]
- M1~M4 handoff_payload: {{m1_m4_handoff_payload}}
- 캠페인명: {{campaign_name}}
- 브랜드명: {{brand_name}}
```

## 2) 실행 프롬프트 (복붙용)

```text
당신은 경영진 커뮤니케이션 리드다.
M1~M4 결과를 의사결정 문서로 통합하라.

[입력 컨텍스트]
- M1~M4 handoff_payload: {{m1_m4_handoff_payload}}
- 캠페인명: {{campaign_name}}
- 브랜드명: {{brand_name}}

[필수 수행]
1) 경영진 1페이지 요약 작성(배경/인사이트/임팩트/리스크)
2) 의사결정 요청사항 3개 이내 정의
3) 다음 분기 실행 우선순위 제시
4) 불확실성과 검증계획 병기

[출력 규칙]
- 구조화 결과는 단일 `json` 코드 블록으로만 출력
- 코드 블록 내부에는 파싱 가능한 JSON만 포함
- 코드 블록 외 설명은 최대 5줄
```

## 3) 출력 JSON 스키마

```json
{
  "stage": "M5",
  "assumptions": [],
  "inputs_used": {},
  "artifacts": {
    "executive_one_pager": {},
    "decision_asks": [],
    "quarterly_action_plan": []
  },
  "quality_notes": [],
  "next_stage_ready": true,
  "handoff_payload": {
    "board_ready_packet": {},
    "metrics_dictionary": {},
    "followup_tracking": []
  }
}
```
