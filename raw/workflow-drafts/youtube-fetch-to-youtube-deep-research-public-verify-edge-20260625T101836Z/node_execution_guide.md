Use skill sop-youtube-deep-research to execute this downstream node.

Node Execution Guide
- Edge: youtube-fetch -> youtube-deep-research
- Evaluation summary: 上下游存在显式引用或同名输入输出，可稳定生成节点执行指导文档。
- Edge Handoff Instruction: 把上游视频 URL 交给 YouTube 深度研究节点，metadata 只作为可选上下文。

Upstream artifacts
- source_url: raw/node-runs/{pipeline_id}/outputs/files/source-url.txt
- metadata_file: raw/node-runs/{pipeline_id}/outputs/files/metadata.json

Execution rules
- Use only the resolved Edge inputs and materialized artifacts.
- For source_url, read the content of source-url.txt and use it as the source_url input to youtube-deep-research.
- Optionally, read metadata.json and pass it as supporting context; the downstream node's resolvers can extract source_url from it if needed.
- Run the node execution command without modifications.
- Verify outputs: analysis.md and transcript.txt are produced in expected paths.
