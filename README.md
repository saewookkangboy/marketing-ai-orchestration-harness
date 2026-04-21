# Marketing AI Orchestration Harness

전략(M1) → 실행(M2) → 최적화(M3) → 분석(M4) → 보고(M5) 파이프라인을 단절 없이 운영하기 위한 프롬프트 레포입니다. 필요 시 전 단계를 묶어 요약하는 **SYNTH** 산출물 스키마도 `schemas/handoff.schema.json`에 포함합니다.

![Orchestration blueprint](./git_blueprint.png)

## Repository About & Description (KR/EN)

### About

- KR: `캠페인 입력 변수와 로컬 근거 문서를 기반으로, M1~M5 마케팅 에이전트를 단계적으로 지휘하는 프롬프트 운영 레포입니다. 단계 간 handoff JSON 스키마(M1~M5 및 선택적 SYNTH)와 렌더링·리포트 스크립트를 포함해 실행 일관성과 데이터 연속성을 보장합니다.`
- EN: `A prompt operations repository that orchestrates M1–M5 marketing agents from campaign inputs and local evidence files. It includes handoff JSON schemas (including an optional SYNTH rollup stage) plus rendering/reporting scripts to ensure execution consistency and cross-stage data continuity.`

## 목적

- 캠페인/브랜드/카테고리/경쟁사 리서치 변수를 입력받아 마케팅 에이전트 팀을 통합 지휘
- 전략(M1), 실행(M2), 최적화(M3), 분석(M4), 보고(M5)를 단일 하네스로 연결
- ChatGPT, Claude, Gemini에서 공통 활용 가능한 프롬프트 체계 제공

## 폴더 구조

- `prompts/orchestration`: 오케스트레이션 마스터 프롬프트
- `prompts/stages`: M1~M5 단계별 전문 에이전트 프롬프트
- `prompts/specialized`: 이미지/메시지/영상 제안 등 확장 모듈
- `prompts/providers`: 모델별 적용 가이드(ChatGPT/Claude/Gemini)
- `prompts/providers/orchestration_prompt_input_guide.md`: 입력 변수만 채워 실행하는 원프롬프트 가이드
- `schemas`: 단계 간 핸드오프 JSON 스키마(M1~M5 및 선택적 SYNTH)
- `examples`: 입력 템플릿, **실행 런북**(`examples/runbook.md`), **샘플 런**(`examples/runs/galaxy-fold8/` — `input.json`, 단계별 `M*_output.json` / `.md`, `SYNTH_report.md`)
- `scripts`: 로컬 인덱싱·게이트, 변수 주입 렌더링, 게이트 연동 일괄 실행, JSON→Markdown 변환

## 빠른 시작

상세 단계·검증 체크리스트는 `examples/runbook.md`를 기준으로 하면 됩니다.

1. 입력 변수 파일 작성
   - `examples/input-template.json`을 복사해 값 입력(샘플 런은 `examples/runs/galaxy-fold8/input.json` 참고)
2. 프롬프트 렌더링
   - 오케스트레이션: `python3 scripts/render_prompt.py --input examples/input-template.json --stage orchestration`
   - 단계별(M1~M5): 동일 명령에 `--stage M1` … `M5` 지정
   - 출력 경로를 바꾸려면 `--output dist/my_rendered.md`(미지정 시 `dist/<stage>_rendered.md`)
3. 출력 프롬프트 사용
   - 생성된 Markdown을 ChatGPT/Claude/Gemini에 붙여 실행
   - 또는 `prompts/providers/orchestration_prompt_input_guide.md`의 공통 원프롬프트에 입력 변수 JSON만 채워 즉시 실행
4. 단계 결과를 Markdown 보고서로 변환(선택)
   - `python3 scripts/export_markdown_report.py --input examples/runs/galaxy-fold8/M1_output.json`
   - 기본 출력: 입력과 같은 디렉터리에 `<입력파일_stem>.md`(예: `M1_output.md`)
   - 경로·제목 지정: `--output dist/M1_report.md`, `--title "M1 전략 요약"`
   - M2 콘텐츠 출력 조건 반영 예시: `examples/runs/galaxy-fold8/M2_output.json`의 `artifacts.conditions_applied`

## Cursor Agent / Claude Cowork 로컬 문서 연동 프로세스

로컬 파일(`.md`, `.markdown`, `.txt`, `.doc`, `.docx`, `.pdf`)을 근거로 실행할 때는 아래 순서를 권장합니다.

1. **근거 파일 수집 및 자동 인덱싱**
   - 캠페인 브리프, 제품 스펙 문서, 경쟁사 분석 자료를 로컬 폴더에 모음
   - 자동 인덱싱 + 게이트 검사 실행:
     - `python3 scripts/local_intake_gate.py --docs-dir <local_docs_dir>`
     - 산출 경로를 바꿀 때: `--output <gate_report.json>`, `--input-output <suggested_input.json>`
   - 기본 산출:
     - `dist/local_intake_gate_report.json` (게이트 판정/근거 맵)
     - `dist/local_intake_input_suggested.json` (입력 변수 후보값)
   - `.doc`는 macOS `textutil`, `.pdf`는 `pdftotext`(poppler 등)가 있으면 텍스트 추출 품질이 좋아집니다. 없으면 해당 형식은 스킵되거나 빈 문자열로 처리될 수 있습니다.
2. **필수 입력 변수 매핑**
   - `dist/local_intake_input_suggested.json`을 검토 후 `examples/input-template.json`에 게이트 필수 항목(스칼라 5개·배열 2종)을 반영해 확정
   - `content_output_conditions`가 있으면 M2 콘텐츠 생성 제약으로 함께 반영
3. **필수 입력 변수 게이트 확인**
   - 필수 스칼라: `campaign_name`, `brand_name`, `brand_category`, `product_specs`, `target_region`
   - 필수 컬렉션: `competitor_set`(1개 이상), `topic_clusters`(1개 이상)
   - `campaign_data`가 없으면 M4는 시뮬레이션 모드로 실행
4. **프롬프트 렌더링 및 실행**
   - `python3 scripts/render_prompt.py --input examples/input-template.json --stage orchestration`
   - 렌더링 결과를 Cursor Agent 또는 Claude Cowork에 붙여 실행
5. **출력 검증**
   - 인테이크 직후: `dist/local_intake_gate_report.json`의 `intake_status.gate_pass`와 `source_documents`로 근거 맵을 확인
   - 단계 실행 후: 각 단계 출력 JSON의 `inputs_used` 등에 근거·변수 매핑이 남는지 확인

## 게이트-렌더 파이프라인 실행

게이트 통과 시에만 프롬프트 렌더링을 수행하려면 다음 커맨드를 사용합니다.

`python3 scripts/run_with_gate.py --docs-dir <local_docs_dir> --input examples/input-template.json --stage orchestration`

- 기본 동작:
  - `local_intake_gate.py` 실행
  - 게이트 실패 시 렌더링 스킵(누락 필드·후속 질문을 stdout에 출력)
  - 게이트 통과 시 베이스 입력과 제안 입력을 병합한 `dist/resolved_input.json`을 만든 뒤 `render_prompt.py` 실행
- 주요 옵션:
  - `--input`: 베이스 입력 JSON(기본 `examples/input-template.json`). 이미 채운 필드는 제안값보다 우선합니다.
  - `--stage`: `orchestration` 또는 `M1`~`M5`(기본 `orchestration`)
  - `--gate-report`, `--suggested-input`, `--resolved-input`: 각 단계 산출 JSON 경로
  - `--render-output dist/orchestration_rendered.md`: 렌더 결과 파일명
  - `--fail-on-gate-fail`: 게이트 실패 시 exit code 2

## 지원 입력 변수

- `campaign_name`: 특정 기업 캠페인명
- `brand_name`: 특정 기업 브랜드명
- `brand_category`: 특정 기업 카테고리
- `competitor_set`: 유사 경쟁 기업 및 포지셔닝 정보(예: `name`, `positioning`, `message_pattern` 등 객체 배열)
- `product_specs`: 제품/서비스 기술 및 증빙 정보
- `topic_clusters`: 콘텐츠 주제 클러스터
- `target_region`: 국가/언어/규제 민감도
- `campaign_data`: 성과 데이터(없으면 M4 시뮬레이션 모드)
- `content_output_conditions`: 콘텐츠 출력 조건(채널별 포맷, 최적화 지침, CTA/이미지 생성 제약)

## 데이터 연속성

- 각 단계 출력 JSON의 `handoff_payload`를 다음 단계 입력으로 넘깁니다. 누락 시 해당 단계를 다시 실행합니다.
- `schemas/handoff.schema.json`에서 `stage`는 `M1`~`M5`와 파이프라인 요약·통합 산출에 쓰일 수 있는 `SYNTH`를 허용합니다.
- 단계별 `inputs_used`에 실제 인용한 로컬 근거 경로를 남겨 감사 가능성을 유지합니다.

## 권장 운영 방식

`examples/runbook.md`와 동일한 리듬을 권장합니다.

- 주간: M2/M3 크리에이티브 갱신
- 월간: M4/M5 보고 체계 업데이트
- 분기: 경쟁사 리서치·메시지/크리에이티브 라이브러리 리빌드, M1 전략 프레임 재정렬

## 전체 프롬프트 구조 도식화

### 트리 구조

```text
Marketing AI Orchestration Prompt System
├─ 1) 최상위 정책 계층 (Policy)
│  ├─ System 규칙
│  │  ├─ 역할/행동 원칙
│  │  ├─ 채널 규칙(commentary/final)
│  │  └─ 도구 우선 사용 원칙
│  ├─ Developer 규칙
│  │  ├─ 편집/검증/보고 방식
│  │  ├─ Git 안전 수칙
│  │  └─ 모드 전환(Agent/Plan) 기준
│  └─ User 규칙
│     └─ 항상 한국어 응답
├─ 2) 실행 계층 (Execution)
│  ├─ 파일/코드 탐색 도구(ReadFile, Glob, rg, SemanticSearch)
│  ├─ 실행 도구(Shell, Await)
│  ├─ 편집 도구(ApplyPatch, EditNotebook)
│  └─ 검증 도구(ReadLints, 테스트 커맨드)
├─ 3) 안전/품질 계층 (Safety & Quality)
│  ├─ 파괴적 명령 제한
│  ├─ 커밋/PR 절차 강제
│  ├─ 비밀정보 커밋 방지
│  └─ 변경 후 린트/검증 권장
├─ 4) 확장 계층 (MCP & Skills)
│  ├─ MCP 서버(브라우저, Notion, Supabase, Slack 등)
│  ├─ MCP 스키마 선확인 규칙
│  └─ 목적별 Skill 모듈(디버깅/배포/PR/문서화 등)
└─ 5) 작업 계층 (Task Intent)
   ├─ 사용자 목표 해석
   ├─ 단계별 실행(M1 → M5)
   └─ 결과 산출물(dist 프롬프트, JSON 출력, 보고물)
```

### 계층 다이어그램

```mermaid
flowchart TB
  A["5) 작업 계층<br/>Task Intent"] --> B["4) 확장 계층<br/>MCP & Skills"]
  B --> C["3) 안전/품질 계층<br/>Safety & Quality"]
  C --> D["2) 실행 계층<br/>Execution Tools"]
  D --> E["1) 최상위 정책 계층<br/>System / Developer / User Rules"]
```

### 해석 가이드

- `정책 계층`이 가장 강한 제약으로, 모든 실행 판단의 기준입니다.
- `실행 계층`은 실제 작업을 수행하는 도구 집합입니다.
- `안전/품질 계층`은 실행 중 실수와 리스크를 줄이는 방어선입니다.
- `확장 계층`은 외부 시스템 연동(MCP)과 재사용 가능한 작업 템플릿(Skill)을 담당합니다.
- `작업 계층`은 M1~M5 목표 달성을 위한 실제 사용자 요청과 산출물에 해당합니다.

### `prompts/` 파일별 계층 매핑

| 파일 경로 | 분류 | 매핑 계층 | 역할 요약 |
| --- | --- | --- | --- |
| `prompts/orchestration/master_orchestration_agent.md` | Orchestration | 5) 작업 계층 (Task Intent) | M1~M5 전체 파이프라인을 지휘하고 단계 간 입력/출력을 연결하는 최상위 실행 프롬프트 |
| `prompts/stages/M1_content_strategy_agent.md` | Stage (M1) | 5) 작업 계층 (Task Intent) | 리서치 변수 기반 콘텐츠 전략/프레임 설계 |
| `prompts/stages/M2_content_execution_agent.md` | Stage (M2) | 5) 작업 계층 (Task Intent) | 전략을 실제 콘텐츠 제작 지시/산출로 변환 |
| `prompts/stages/M3_optimization_agent.md` | Stage (M3) | 5) 작업 계층 (Task Intent) | 품질 게이트, 개선 루프, 실험/최적화 지시 |
| `prompts/stages/M4_performance_analysis_agent.md` | Stage (M4) | 5) 작업 계층 (Task Intent) | 성과 데이터 분석 및 인사이트 도출 |
| `prompts/stages/M5_executive_reporting_agent.md` | Stage (M5) | 5) 작업 계층 (Task Intent) | 의사결정자 관점의 보고/요약 산출 |
| `prompts/specialized/content_message_prompt.md` | Specialized Module | 4) 확장 계층 (MCP & Skills) | 메시지/카피라이팅 등 특정 목적 작업을 보강하는 확장 모듈 |
| `prompts/specialized/image_generation_prompt.md` | Specialized Module | 4) 확장 계층 (MCP & Skills) | 이미지 생성 업무를 위한 목적형 확장 프롬프트 |
| `prompts/specialized/video_service_proposal_prompt.md` | Specialized Module | 4) 확장 계층 (MCP & Skills) | 영상/서비스 제안서 성격의 특화 산출물 생성 모듈 |
| `prompts/providers/chatgpt_adapter.md` | Provider Adapter | 4) 확장 계층 (MCP & Skills) | ChatGPT 환경에 맞는 적용 규칙/변환 가이드 |
| `prompts/providers/claude_adapter.md` | Provider Adapter | 4) 확장 계층 (MCP & Skills) | Claude 환경에 맞는 적용 규칙/변환 가이드 |
| `prompts/providers/gemini_adapter.md` | Provider Adapter | 4) 확장 계층 (MCP & Skills) | Gemini 환경에 맞는 적용 규칙/변환 가이드 |
| `prompts/providers/orchestration_prompt_input_guide.md` | Provider / Ops Guide | 4) 확장 계층 (MCP & Skills) | 공통 원프롬프트에 입력 JSON만 채워 오케스트레이션을 바로 실행하는 가이드 |
| `examples/runbook.md` | Operations | 5) 작업 계층 (Task Intent) | 입력 준비부터 렌더·LLM 실행·핸드오프·Markdown 변환까지의 실행 런북 |

> 참고: 현재 `prompts/` 디렉터리의 파일은 `작업 계층(5)`과 `확장 계층(4)`에 집중되어 있으며, `정책/실행/안전 계층(1~3)`은 주로 시스템/개발자 지침 및 런타임 도구 규칙에서 담당합니다.
