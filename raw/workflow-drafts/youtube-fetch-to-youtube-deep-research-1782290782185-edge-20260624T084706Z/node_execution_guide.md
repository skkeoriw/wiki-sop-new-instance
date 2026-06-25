Use skill sop-youtube-deep-research to execute this downstream node.

Node Execution Guide
- Edge: youtube-fetch -> youtube-deep-research
- Evaluation summary: 上游的 source_url 可直连传入下游 source_url，metadata_file 可作为可选上下文通过 JSON 路径提取 URL。边缘指令明确，无阻塞。
- Edge Handoff Instruction: 把上游视频 URL 交给深度研究节点，metadata 只作为可选上下文。

Upstream artifacts
- source_url: raw/node-runs/{pipeline_id}/outputs/files/source-url.txt (scalar URL)
- metadata_file: raw/node-runs/{pipeline_id}/outputs/files/metadata.json (JSON file)

Execution rules
- Use only the resolved Edge inputs and materialized artifact for source_url.
- For source_url: use the content of source_url.txt as direct URL.
- Optionally, if metadata_file is available, you may extract source_url using json_path "$.source_url" or "$.youtube_url" as fallback.
- Do not require metadata_file; downstream must accept the primary source_url.
- Downstream skill expects source_url as required input; ensure pipeline provides it.

Output expectations
- analysis_file: raw/youtube-deep-research/{pipeline_id}/outputs/analysis.md (markdown)
- transcript_file: raw/youtube-deep-research/{pipeline_id}/outputs/transcript.txt (text)

Handover note: This node runs after youtube-fetch and before wiki-build.
