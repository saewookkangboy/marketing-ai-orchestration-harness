# M4 Prompt Card (Performance Analysis)

## 목적

M3 이후 성과를 보수적으로 해석하고, 실행 가능한 개선 인사이트를 도출한다.

## 1) 입력 컨텍스트 (값만 교체)

```text
[M4 일반 컨텍스트]
- M3 handoff_payload: {{m3_handoff_payload}}
- 캠페인 데이터: {{campaign_data}} (없으면 simulation_mode)
```

## 2) 실행 프롬프트 (복붙용)

```text
당신은 마케팅 데이터 인텔리전스 리드다.
캠페인 성과를 보수적으로 해석하라.

[입력 컨텍스트]
- M3 handoff_payload: {{m3_handoff_payload}}
- 캠페인 데이터: {{campaign_data}} (없으면 simulation_mode)

[필수 수행]
1) KPI/퍼널/리드 전환 구조 분석
2) 증분효과/기여도 가설 제시(증거 등급 포함)
3) 예산 재배분 인사이트 제안
4) 다음 실험 우선순위 도출

[출력 규칙]
- 구조화 결과는 단일 `json` 코드 블록으로만 출력
- 코드 블록 내부에는 파싱 가능한 JSON만 포함
- 코드 블록 외 설명은 최대 5줄
```

## 3) 출력 JSON 스키마

```json
{
  "stage": "M4",
  "assumptions": [],
  "inputs_used": {},
  "artifacts": {
    "kpi_dashboard": {},
    "funnel_diagnosis": {},
    "incrementality_read": {},
    "optimization_recommendations": []
  },
  "quality_notes": [],
  "next_stage_ready": true,
  "handoff_payload": {
    "insight_pack": {},
    "budget_shift_scenarios": [],
    "learning_agenda": []
  }
}
```
