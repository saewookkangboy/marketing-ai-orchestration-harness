# Gemini Adapter

## 사용법
1. 마스터 프롬프트를 system instruction으로 설정
2. 구조화 출력은 JSON schema를 함께 제시
3. **채팅/자유 텍스트 응답**에서는 API structured output을 쓰지 않을 때에도, 단계 산출 JSON 전체를 **`json` 태그 Markdown 코드 블록 한 블록**에만 넣어 사용자가 한 번에 복사할 수 있게 한다(블록 밖 자연어는 요약·안내만).
4. 이미지/영상 관련 결과는 `prompts/specialized` 템플릿을 함께 첨부

## 권장 설정
- Temperature: 0.4
- Top-p: 0.9
- Structured output: 활성화 권장

## 멀티모달 팁
- 이미지 생성 프롬프트는 `장면/구도/피사체/톤/금지요소`를 필수 슬롯으로 고정
- 영상 제안은 15초/30초/60초 버전으로 분기
