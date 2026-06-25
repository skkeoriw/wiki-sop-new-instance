Use skill sop-youtube-deep-research to execute this downstream node.

Node Execution Guide
- Edge: youtube-fetch -> youtube-deep-research
- Evaluation summary: 上下游存在显式引用或同名输入输出，可稳定生成节点执行指导文档。
- Edge Handoff Instruction: 将 youtube-fetch 输出的 source_url 直接传递给 youtube-deep-research 的 source_url 输入；metadata_file 作为补充上下文不作为主输入，但可通过 json_path 解析器从中提取 source_url 备用。

Upstream artifacts
- source_url: raw/node-runs/{pipeline_id}/outputs/files/source-url.txt
- metadata_file: raw/node-runs/{pipeline_id}/outputs/files/metadata.json

Execution steps:
1. Read the upstream source_url file (scalar URL) and pass it as the primary input to the downstream's `source_url` parameter using the direct-url resolver.
2. Optionally, read the metadata_file (JSON) and use a json_path resolver (e.g., metadata-source-url) to extract `$.source_url` as a fallback if the primary source_url is missing or invalid.
3. Execute the skill sop-youtube-deep-research with the constructed inputs.

Expected outputs:
- analysis_file: raw/youtube-deep-research/{pipeline_id}/outputs/analysis.md
- transcript_file: raw/youtube-deep-research/{pipeline_id}/outputs/transcript.txt

Note: Ensure the downstream node's workspace paths are correctly resolved using the pipeline_id from the runtime context.
