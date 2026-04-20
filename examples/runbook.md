# 실행 런북

## 1) 입력 준비

- `examples/input-template.json`를 복제해 캠페인별 입력 작성
- 필수 슬롯 누락 여부 확인
- 로컬 근거 파일(`.md`, `.txt`, `.doc/.docx`, `.pdf`)을 먼저 정리하고, 슬롯별 근거 출처를 메모
- 자동 인덱싱/게이트 검사 실행:  
  `python3 scripts/local_intake_gate.py --docs-dir <local_docs_dir>`
- 결과 파일:
  - `dist/local_intake_gate_report.json`
  - `dist/local_intake_input_suggested.json`

### 1-1) 필수 입력 변수 게이트(실행 전)

- 아래 항목이 모두 충족되지 않으면 실행하지 않고 누락 항목만 보완
  - 스칼라 필수: `campaign_name`, `brand_name`, `brand_category`, `product_specs`, `target_region`
  - 배열 필수: `competitor_set` 1개 이상, `topic_clusters` 1개 이상
  - `campaign_data` 미입력 시 M5는 `simulation_mode`로 실행

## 2) 프롬프트 렌더링

- 오케스트레이션:  
  `python3 scripts/render_prompt.py --input examples/input-template.json --stage orchestration`
- 단계별(M2~M6):  
  `python3 scripts/render_prompt.py --input examples/input-template.json --stage M2`
- 게이트 연동 파이프라인(권장):  
  `python3 scripts/run_with_gate.py --docs-dir <local_docs_dir> --input examples/input-template.json --stage orchestration`

## 3) LLM별 실행

- ChatGPT: `prompts/providers/chatgpt_adapter.md` 참고
- Claude: `prompts/providers/claude_adapter.md` 참고
- Gemini: `prompts/providers/gemini_adapter.md` 참고
- Cursor Agent / Claude Cowork 공통: 실행 시 로컬 파일 근거와 매핑된 변수 목록을 첫 입력 블록에 함께 전달

## 4) 데이터 연속성 원칙

- 각 단계 출력 JSON의 `handoff_payload`를 다음 단계 입력으로 전달
- 누락 시 단계 재실행
- 각 단계 `inputs_used.sources`에 실제 사용한 로컬 파일 경로를 유지

## 5) JSON -> Markdown 보고서 변환(선택)

- 단계 결과 JSON을 사람이 읽기 쉬운 보고서로 변환:  
  `python3 scripts/export_markdown_report.py --input examples/runs/galaxy-fold8/M2_output.json`
- 출력 경로를 지정하려면:  
  `python3 scripts/export_markdown_report.py --input examples/runs/galaxy-fold8/M2_output.json --output dist/M2_report.md`

## 6) 운영 리듬

- 주간: M3/M4 크리에이티브 갱신
- 월간: M5/M6 보고 체계 업데이트
