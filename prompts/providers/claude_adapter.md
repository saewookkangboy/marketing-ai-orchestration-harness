# Claude Adapter

## 사용법
1. 마스터 프롬프트를 System에 배치
2. 단계별 실행 시 `M1 -> M2 -> M3 -> M4 -> M5` 순서로 분할 호출
3. 각 단계의 `handoff_payload`를 다음 호출의 첫 문단에 그대로 전달

## 권장 설정
- Temperature: 0.2~0.5
- Max tokens: 충분히 크게 설정(단계별 4k 이상 권장)
- 스타일: concise + **json 코드 펜스로 감싼 단일 JSON**(채팅 UI 복사 우선)

## 주의
- 긴 설명 대신 **구조화 데이터는 항상 json fenced code block 안**에만 두고, 블록 밖 설명은 최소화한다.
- 근거 없는 비교표현 금지 규칙을 매 호출에 재명시
