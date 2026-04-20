# ChatGPT Adapter

## 사용법
1. `prompts/orchestration/master_orchestration_agent.md` 내용을 시스템 프롬프트로 사용
2. 사용자 메시지에 변수 JSON을 함께 입력
3. 응답 형식은 JSON 유지, 마크다운 설명은 JSON 뒤에 추가

## 권장 설정
- Reasoning: high
- Temperature: 0.3~0.6
- Tool use: on (데이터 분석/리포트 자동화 시)

## 입력 예시
```json
{
  "campaign_name": "2026 Q3 B2B 리드 전환 캠페인",
  "brand_name": "Samsung DX",
  "brand_category": "B2B 솔루션",
  "competitor_set": ["LG B2B", "Siemens", "Honeywell"],
  "product_specs": "공식 스펙 문서 기반 핵심 성능 요약",
  "topic_clusters": ["스마트 오피스", "운영 효율", "보안"],
  "target_region": "KR",
  "campaign_data": "CSV 또는 요약 지표"
}
```
