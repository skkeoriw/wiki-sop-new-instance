Use skill sop-youtube-deep-research to execute this downstream node.

## Node Execution Guide
- Edge: youtube-fetch -> youtube-deep-research
- Evaluation: 上下游输入输出映射清晰，可运行。
- Edge Handoff Instruction: 把上游视频 URL 交给 YouTube 深度研究节点，metadata 只作为可选上下文。

### Upstream Artifacts
- `source_url`: `raw/node-runs/{pipeline_id}/outputs/files/source-url.txt` (scalar/url)
- `metadata_file`: `raw/node-runs/{pipeline_id}/outputs/files/metadata.json` (file/json, optional)

### Execution Rules
1. **Primary Input**: Use `source_url` from upstream as `source_url` for downstream. This is the direct relay mapping.
2. **Fallback Input**: If `source_url` is unavailable, extract `$.source_url` from `metadata_file` using json_path resolver.
3. **Optional Context**: `metadata_file` is not required by downstream; only use if needed for fallback.
4. **Execution Command**: Run the downstream node with the resolved `source_url`. Example:
   ```
   Use skill sop-youtube-deep-research to execute this Node Execution Request.
   Execution command: bash __SKILL_DIR__/scripts/run_youtube_deep_research.sh --source-url "${RESOLVED_URL}"
   ```
5. **Outputs**: Downstream produces `analysis_file` and `transcript_file` as per skill definition.
