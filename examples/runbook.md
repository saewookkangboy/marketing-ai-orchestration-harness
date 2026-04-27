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
  - `campaign_data` 미입력 시 M4는 `simulation_mode`로 실행

## 2) 카드형 프롬프트 선택

- 전체 실행(권장):
  - `prompts/orchestration/master_orchestration_agent.md`의 `Starter` 또는 `Advanced` 블록 사용
- 단계별 단독 실행:
  - `prompts/stages/M1_content_strategy_agent.md` ~ `M5_executive_reporting_agent.md` 사용
- 모델별 입력 UX:
  - `prompts/providers/chatgpt_adapter.md`
  - `prompts/providers/claude_adapter.md`
  - `prompts/providers/gemini_adapter.md`
  - 공통 가이드는 `prompts/providers/orchestration_prompt_input_guide.md` 사용

## 3) 프롬프트 렌더링(자동 변수 주입이 필요할 때)

- 오케스트레이션 렌더링:  
  `python3 scripts/render_prompt.py --input examples/input-template.json --stage orchestration`
- 단계별(M1~M5) 렌더링:  
  `python3 scripts/render_prompt.py --input examples/input-template.json --stage M1`
- 게이트 연동 파이프라인(권장):  
  `python3 scripts/run_with_gate.py --docs-dir <local_docs_dir> --input examples/input-template.json --stage orchestration`

## 4) 실제 입력 절차 (복붙 기준)

1. 선택한 카드 파일에서 `입력 컨텍스트` 섹션의 `{{...}}` 값을 채운다.
2. 같은 파일의 `실행 프롬프트(복붙용)` 블록을 모델 입력창에 붙여 넣는다.
3. 출력은 반드시 `json` 단일 코드 블록으로 수집한다.
4. 단계 실행이라면 `handoff_payload`를 다음 단계 입력 컨텍스트에 전달한다.

## 5) 데이터 연속성 원칙

- 각 단계 출력 JSON의 `handoff_payload`를 다음 단계 입력으로 전달
- 누락 시 단계 재실행
- 각 단계 `inputs_used.sources`에 실제 사용한 로컬 파일 경로를 유지

## 6) JSON -> Markdown 보고서 변환(선택)

- 단계 결과 JSON을 사람이 읽기 쉬운 보고서로 변환:  
  `python3 scripts/export_markdown_report.py --input examples/runs/galaxy-fold8/M1_output.json`
- 출력 경로를 지정하려면:  
  `python3 scripts/export_markdown_report.py --input examples/runs/galaxy-fold8/M1_output.json --output dist/M1_report.md`

## 7) 운영 리듬

- 주간: M2/M3 크리에이티브 갱신
- 월간: M4/M5 보고 체계 업데이트
