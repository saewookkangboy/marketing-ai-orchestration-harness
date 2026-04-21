# Claude Adapter

## 사용법
1. 마스터 프롬프트를 System에 배치
2. 단계별 실행 시 `M1 -> M2 -> M3 -> M4 -> M5` 순서로 분할 호출
3. 각 단계의 `handoff_payload`를 다음 호출의 첫 문단에 그대로 전달

## 권장 설정
- Temperature: 0.2~0.5
- Max tokens: 충분히 크게 설정(단계별 4k 이상 권장)
- 스타일: concise + structured JSON

## 주의
- Claude는 긴 컨텍스트에서 설명이 길어질 수 있으므로 `JSON first` 지시를 유지
- 근거 없는 비교표현 금지 규칙을 매 호출에 재명시
