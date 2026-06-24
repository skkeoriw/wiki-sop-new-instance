Use skill sop-youtube-deep-research to execute this Node Execution Request.

# Node Execution Request

Runtime context:
- runtime_id: runtime-152-32-214-95
- instance_id: test-instance
- workflow_id: youtube-research-wiki
- node_id: youtube-deep-research
- node_run_id: node-run-youtube-deep-research-edge-guide-audit-20260624T092756Z

Input contract:
- input_manifest_path: raw/node-runs/node-run-youtube-deep-research-edge-guide-audit-20260624T092756Z/inputs/sources/manifest.json
- input_directory: raw/node-runs/node-run-youtube-deep-research-edge-guide-audit-20260624T092756Z/inputs/sources
- source_url: https://www.youtube.com/watch?v=dQw4w9WgXcQ
- Only use files listed in the input manifest unless the selected skill already has a stricter rule.

Relay context:
Edge: edge-youtube-fetch-to-youtube-deep-research (youtube-fetch -> youtube-deep-research)
Intent: 将视频地址交给深度研究节点
Instruction: 下游只需要一个可解析的 YouTube URL。优先使用 source_url；只有显式选择 metadata_file 时才从 JSON 字段提取 URL。
Bindings:
- source_url -> source_url via auto; path=raw/node-runs/node-run-youtube-fetch-20260622T083527Z-cfe243/outputs/files/source-url.txt

Approved Edge Handoff Guide:
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

Output contract:
- output_directory: raw/node-runs/node-run-youtube-deep-research-edge-guide-audit-20260624T092756Z/outputs/files
- output_manifest_path: raw/node-runs/node-run-youtube-deep-research-edge-guide-audit-20260624T092756Z/outputs/files/manifest.json
- receipt_path: raw/node-runs/node-run-youtube-deep-research-edge-guide-audit-20260624T092756Z/agent/receipt.json
- Do not report success unless the declared output manifest and receipt are written or the runtime wrapper writes equivalent state that the adapter can verify.

Execution command:
```bash
bash /root/agent-brain-plugins/youtube-wiki/skills/sop-youtube-deep-research/scripts/run_youtube_deep_research.sh /root/wiki/wiki-sop-new-instance node-run-youtube-deep-research-edge-guide-audit-20260624T092756Z node-run-youtube-deep-research-edge-guide-audit-20260624T092756Z
```

Execution rules:
- Use the selected skill only: sop-youtube-deep-research.
- Run the command from the Instance workspace unless the skill has an equivalent deterministic wrapper.
- Preserve the provided environment variables.
- Do not invent paths.
- If execution fails, return the failure and include stderr/log guidance.
