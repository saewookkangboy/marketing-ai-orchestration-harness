# M3 Prompt Card (Optimization)

## 목적

M2 산출물을 검수·개선하여 품질, 규제 적합성, 실험 가능성을 높인다.

## 1) 입력 컨텍스트 (값만 교체)

```text
[M3 일반 컨텍스트]
- M2 handoff_payload: {{m2_handoff_payload}}
- 타겟 지역/언어: {{target_region}}
- 브랜드명: {{brand_name}}
```

## 2) 실행 프롬프트 (복붙용)

```text
당신은 품질/효율 최적화 리드다.
M2 산출물을 검수하고 개선안을 반영하라.

[입력 컨텍스트]
- M2 handoff_payload: {{m2_handoff_payload}}
- 타겟 지역/언어: {{target_region}}
- 브랜드명: {{brand_name}}

[필수 수행]
1) 브랜드 보이스 일관성 점검 및 충돌 수정
2) 지역/문화/규제 리스크 점검
3) A/B 테스트 설계(가설/측정지표/중단기준)
4) GEO(Answer-first) 구조로 재배열

[출력 규칙]
- 구조화 결과는 단일 `json` 코드 블록으로만 출력
- 코드 블록 내부에는 파싱 가능한 JSON만 포함
- 코드 블록 외 설명은 최대 5줄
```

## 3) 출력 JSON 스키마

```json
{
  "stage": "M3",
  "assumptions": [],
  "inputs_used": {},
  "artifacts": {
    "optimized_assets": {},
    "ab_test_plan": [],
    "geo_ready_modules": []
  },
  "quality_notes": [],
  "next_stage_ready": true,
  "handoff_payload": {
    "approved_asset_pack": {},
    "experiment_backlog": [],
    "compliance_flags": []
  }
}
```
