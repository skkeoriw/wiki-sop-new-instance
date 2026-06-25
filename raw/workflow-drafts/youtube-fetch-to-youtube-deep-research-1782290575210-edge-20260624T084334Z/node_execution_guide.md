使用技能 `sop-youtube-deep-research` 执行下游节点。

## Node Execution Guide
- **Edge**: youtube-fetch → youtube-deep-research
- **手顺指令**: 把上游视频 URL 交给深度研究节点，metadata 只作为可选上下文。
- **上游产物**:
  - `source_url`: raw/node-runs/{pipeline_id}/outputs/files/source-url.txt
  - `metadata_file`: raw/node-runs/{pipeline_id}/outputs/files/metadata.json (可选)

## 执行规则
1. 仅使用已解析的 Edge 输入（source_url）作为下游主输入。
2. 如需要，可将 metadata_file 内容作为额外上下文传递给下游 skill，但不可替代 source_url。
3. 确保下游 skill 在调用时正确接收 source_url（字符串类型 URL）。
4. 跟踪并记录 handoff 评估结果。

## 输出预期
- `analysis_file`: raw/youtube-deep-research/{pipeline_id}/outputs/analysis.md
- `transcript_file`: raw/youtube-deep-research/{pipeline_id}/outputs/transcript.txt
