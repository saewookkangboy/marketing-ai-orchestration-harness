#!/usr/bin/env python3
import argparse
import html
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any


SUPPORTED_EXTENSIONS = {".md", ".markdown", ".txt", ".doc", ".docx", ".pdf"}
REQUIRED_SCALARS = [
    "campaign_name",
    "brand_name",
    "brand_category",
    "product_specs",
    "target_region",
]
REQUIRED_COLLECTIONS = ["competitor_set", "topic_clusters"]

KEYWORDS: dict[str, list[str]] = {
    "campaign_name": ["campaign", "캠페인", "프로모션"],
    "brand_name": ["brand", "브랜드"],
    "brand_category": ["category", "카테고리", "산업", "industry", "sector"],
    "competitor_set": ["competitor", "경쟁", "rival", "benchmark"],
    "product_specs": ["spec", "스펙", "제품", "서비스", "기술", "인증", "feature"],
    "topic_clusters": ["topic", "주제", "cluster", "키워드", "message pillar"],
    "target_region": ["region", "지역", "market", "국가", "언어", "language"],
    "campaign_data": ["kpi", "성과", "전환", "impression", "click", "lead", "roas"],
}


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_docx_file(path: Path) -> str:
    with zipfile.ZipFile(path, "r") as archive:
        xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    text = re.sub(r"<[^>]+>", " ", xml)
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def read_doc_file(path: Path) -> str:
    if shutil.which("textutil") is None:
        return ""
    try:
        output = subprocess.run(
            ["textutil", "-convert", "txt", "-stdout", str(path)],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return ""
    return output.stdout.strip()


def read_pdf_file(path: Path) -> str:
    if shutil.which("pdftotext") is None:
        return ""
    with tempfile.TemporaryDirectory() as temp_dir:
        out_path = Path(temp_dir) / "tmp.txt"
        try:
            subprocess.run(
                ["pdftotext", str(path), str(out_path)],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            return ""
        if not out_path.exists():
            return ""
        return out_path.read_text(encoding="utf-8", errors="ignore").strip()


def extract_text(path: Path) -> tuple[str, str | None]:
    extension = path.suffix.lower()
    try:
        if extension in {".md", ".markdown", ".txt"}:
            return read_text_file(path), None
        if extension == ".docx":
            return read_docx_file(path), None
        if extension == ".doc":
            text = read_doc_file(path)
            if text:
                return text, None
            return "", "DOC 파싱 실패(textutil 필요 또는 파일 손상 가능)"
        if extension == ".pdf":
            text = read_pdf_file(path)
            if text:
                return text, None
            return "", "PDF 파싱 실패(pdftotext 미설치 또는 파일 읽기 제한)"
    except Exception as exc:  # noqa: BLE001
        return "", f"파일 파싱 중 오류: {exc}"
    return "", f"지원하지 않는 확장자: {extension}"


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def text_score(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(word.lower()) for word in keywords)


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?다])\s+", text)
    return [normalize_text(chunk) for chunk in chunks if normalize_text(chunk)]


def first_sentence_for_keywords(text: str, keywords: list[str]) -> str:
    lowered_keywords = [word.lower() for word in keywords]
    for sentence in split_sentences(text):
        lowered = sentence.lower()
        if any(keyword in lowered for keyword in lowered_keywords):
            return sentence
    sentences = split_sentences(text)
    return sentences[0] if sentences else ""


def extract_competitor_set(text: str) -> list[dict[str, str]]:
    lines = [normalize_text(line) for line in text.splitlines() if normalize_text(line)]
    candidates = [
        line for line in lines if re.search(r"(competitor|경쟁|rival|벤치마크)", line, re.IGNORECASE)
    ]
    results = []
    for line in candidates[:5]:
        results.append(
            {
                "name": line[:60],
                "positioning": "",
                "message_pattern": "",
            }
        )
    return results


def extract_topic_clusters(text: str) -> list[str]:
    lines = [normalize_text(line) for line in text.splitlines() if normalize_text(line)]
    candidates = [
        line
        for line in lines
        if re.search(r"(topic|주제|cluster|키워드|메시지)", line, re.IGNORECASE)
    ]
    return [line[:80] for line in candidates[:7]]


def extract_campaign_data(text: str) -> dict[str, Any]:
    numbers = re.findall(r"\b\d[\d,]*\b", text)
    if not numbers:
        return {}
    return {
        "raw_metrics_candidates": numbers[:10],
        "note": "자동 추출값이므로 최종 KPI 구조화 필요",
    }


def build_variable_candidates(documents: list[dict[str, Any]]) -> dict[str, Any]:
    best_text_by_key: dict[str, str] = {}
    evidence_map: dict[str, list[dict[str, str]]] = {key: [] for key in KEYWORDS}

    for key, keywords in KEYWORDS.items():
        best_score = 0
        for doc in documents:
            text = doc.get("text", "")
            if not text:
                continue
            score = text_score(text, keywords)
            if score > 0:
                snippet = first_sentence_for_keywords(text, keywords)
                evidence_map[key].append(
                    {
                        "source": doc["path"],
                        "snippet": snippet[:220],
                    }
                )
            if score > best_score:
                best_score = score
                best_text_by_key[key] = text

    candidates: dict[str, Any] = {}
    for scalar_key in REQUIRED_SCALARS:
        text = best_text_by_key.get(scalar_key, "")
        candidates[scalar_key] = first_sentence_for_keywords(text, KEYWORDS[scalar_key]) if text else ""

    competitor_text = best_text_by_key.get("competitor_set", "")
    candidates["competitor_set"] = extract_competitor_set(competitor_text) if competitor_text else []

    topic_text = best_text_by_key.get("topic_clusters", "")
    candidates["topic_clusters"] = extract_topic_clusters(topic_text) if topic_text else []

    campaign_text = best_text_by_key.get("campaign_data", "")
    candidates["campaign_data"] = extract_campaign_data(campaign_text) if campaign_text else {}

    return {"candidates": candidates, "evidence_map": evidence_map}


def run_gate(candidates: dict[str, Any]) -> dict[str, Any]:
    missing_required: list[str] = []
    for scalar_key in REQUIRED_SCALARS:
        if not str(candidates.get(scalar_key, "")).strip():
            missing_required.append(scalar_key)

    for list_key in REQUIRED_COLLECTIONS:
        if not isinstance(candidates.get(list_key), list) or len(candidates.get(list_key, [])) < 1:
            missing_required.append(list_key)

    simulation_mode = not bool(candidates.get("campaign_data"))
    gate_pass = len(missing_required) == 0

    questions: list[str] = []
    if "campaign_name" in missing_required:
        questions.append("캠페인명을 문서 기준으로 1개 확정해주세요.")
    if "brand_name" in missing_required:
        questions.append("브랜드 공식명을 알려주세요.")
    if "product_specs" in missing_required:
        questions.append("검증 가능한 제품/서비스 스펙 근거 문서를 지정해주세요.")
    if "competitor_set" in missing_required:
        questions.append("비교할 경쟁사 최소 1개를 추가해주세요.")
    if "topic_clusters" in missing_required:
        questions.append("콘텐츠 주제 클러스터를 최소 1개 입력해주세요.")

    return {
        "gate_pass": gate_pass,
        "missing_required": missing_required,
        "simulation_mode": simulation_mode,
        "follow_up_questions": questions[:3],
    }


def build_source_documents(documents: list[dict[str, Any]], evidence_map: dict[str, Any]) -> list[dict[str, Any]]:
    used_by_source: dict[str, set[str]] = {}
    for key, evidences in evidence_map.items():
        for evidence in evidences:
            used_by_source.setdefault(evidence["source"], set()).add(key)

    source_docs: list[dict[str, Any]] = []
    for doc in documents:
        source_docs.append(
            {
                "path": doc["path"],
                "file_type": doc["file_type"],
                "used_in_variables": sorted(list(used_by_source.get(doc["path"], set()))),
                "parse_warning": doc.get("parse_warning"),
                "preview": doc.get("preview", ""),
            }
        )
    return source_docs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Index local markdown/doc/pdf files and run required-input gate checks."
    )
    parser.add_argument("--docs-dir", required=True, help="Directory containing local source documents")
    parser.add_argument(
        "--output",
        default="dist/local_intake_gate_report.json",
        help="Output JSON report path",
    )
    parser.add_argument(
        "--input-output",
        default="dist/local_intake_input_suggested.json",
        help="Output JSON path for suggested input variables",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    docs_dir = Path(args.docs_dir)
    if not docs_dir.is_absolute():
        docs_dir = (repo_root / docs_dir).resolve()
    if not docs_dir.exists():
        raise SystemExit(f"docs-dir does not exist: {docs_dir}")

    files = sorted(
        [
            path
            for path in docs_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
    )
    if not files:
        raise SystemExit(
            "지원 파일이 없습니다. 지원 확장자: .md, .markdown, .txt, .doc, .docx, .pdf"
        )

    documents: list[dict[str, Any]] = []
    for path in files:
        text, warning = extract_text(path)
        normalized = normalize_text(text)
        documents.append(
            {
                "path": str(path),
                "file_type": path.suffix.lower().lstrip("."),
                "text": normalized,
                "parse_warning": warning,
                "preview": normalized[:180],
            }
        )

    mapping = build_variable_candidates(documents)
    candidates = mapping["candidates"]
    gate = run_gate(candidates)
    source_documents = build_source_documents(documents, mapping["evidence_map"])

    report = {
        "intake_status": gate,
        "source_documents": source_documents,
        "variable_candidates": candidates,
        "evidence_map": mapping["evidence_map"],
    }

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = (repo_root / output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    input_output_path = Path(args.input_output)
    if not input_output_path.is_absolute():
        input_output_path = (repo_root / input_output_path).resolve()
    input_output_path.parent.mkdir(parents=True, exist_ok=True)
    input_output_path.write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Intake gate report saved to: {output_path}")
    print(f"Suggested input JSON saved to: {input_output_path}")
    if not gate["gate_pass"]:
        print("Gate failed. Please fill missing required fields:")
        for item in gate["missing_required"]:
            print(f"- {item}")


if __name__ == "__main__":
    main()
