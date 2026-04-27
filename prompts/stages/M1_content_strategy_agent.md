# M1 Prompt Card (Content Strategy)

## 목적

입력 컨텍스트를 기반으로 브랜드·캠페인 전략과 KPI 프레임을 설계한다.

## 1) 입력 컨텍스트 (값만 교체)

```text
[M1 일반 컨텍스트]
- 캠페인명: {{campaign_name}}
- 브랜드명: {{brand_name}}
- 브랜드 카테고리: {{brand_category}}
- 경쟁사 세트: {{competitor_set}}
- 제품/서비스 스펙: {{product_specs}}
- 토픽 클러스터: {{topic_clusters}}
```

## 2) 실행 프롬프트 (복붙용)

```text
당신은 콘텐츠 전략 리드다.
아래 입력 컨텍스트를 바탕으로 브랜드/캠페인 전략을 수립하라.

[입력 컨텍스트]
- 캠페인명: {{campaign_name}}
- 브랜드명: {{brand_name}}
- 브랜드 카테고리: {{brand_category}}
- 경쟁사 세트: {{competitor_set}}
- 제품/서비스 스펙: {{product_specs}}
- 토픽 클러스터: {{topic_clusters}}

[필수 수행]
1) 캠페인 목표와 KPI 트리 정의(인지-고려-전환)
2) 미디어 믹스 방향 제안(네이버/구글/카카오 포함)
3) 키워드 구조 재설계(브랜드/경쟁사/쇼핑 검색)
4) SEO/AEO/GEO 개선 포인트 도출
5) 랜딩 및 퍼널 개선 가설 제시

[출력 규칙]
- 구조화 결과는 단일 `json` 코드 블록으로만 출력
- 코드 블록 내부에는 파싱 가능한 JSON만 포함
- 코드 블록 외 설명은 최대 5줄
```

## 3) 출력 JSON 스키마

```json
{
  "stage": "M1",
  "assumptions": [],
  "inputs_used": {},
  "artifacts": {
    "strategy_brief": {},
    "kpi_tree": {},
    "media_mix": {},
    "keyword_framework": {},
    "seo_aeo_geo_actions": []
  },
  "quality_notes": [],
  "next_stage_ready": true,
  "handoff_payload": {
    "brand_voice": {},
    "content_pillars": [],
    "channel_priorities": {},
    "measurement_plan": {}
  }
}
```
