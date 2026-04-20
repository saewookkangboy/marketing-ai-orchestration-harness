# 실행 런북

## 1) 입력 준비
- `examples/input-template.json`를 복제해 캠페인별 입력 작성
- 필수 슬롯 누락 여부 확인

## 2) 프롬프트 렌더링
- 오케스트레이션:  
  `python3 scripts/render_prompt.py --input examples/input-template.json --stage orchestration`
- 단계별(M2~M6):  
  `python3 scripts/render_prompt.py --input examples/input-template.json --stage M2`

## 3) LLM별 실행
- ChatGPT: `prompts/providers/chatgpt_adapter.md` 참고
- Claude: `prompts/providers/claude_adapter.md` 참고
- Gemini: `prompts/providers/gemini_adapter.md` 참고

## 4) 데이터 연속성 원칙
- 각 단계 출력 JSON의 `handoff_payload`를 다음 단계 입력으로 전달
- 누락 시 단계 재실행

## 5) 운영 리듬
- 주간: M3/M4 크리에이티브 갱신
- 월간: M5/M6 보고 체계 업데이트
