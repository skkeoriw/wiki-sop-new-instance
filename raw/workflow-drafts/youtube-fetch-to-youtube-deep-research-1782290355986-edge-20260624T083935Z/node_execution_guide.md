Use skill sop-youtube-deep-research to execute this downstream node.

## Node Execution Guide
- Edge: `youtube-fetch` → `youtube-deep-research`
- Evaluation summary: 上游输出 source_url 直接匹配下游必需输入 source_url，metadata_file 可作为可选上下文。边缘指令清晰，无阻塞或兼容性问题。
- Edge Handoff Instruction: 把上游视频 URL 交给深度研究节点，metadata 只作为可选上下文。

### Upstream Artifacts
- `source_url`: `raw/node-runs/{pipeline_id}/outputs/files/source-url.txt`
  - Type: scalar (string, url)
  - Role: primary_source
- `metadata_file`: `raw/node-runs/{pipeline_id}/outputs/files/metadata.json`
  - Type: file (json)
  - Role: supporting_context

### Execution Rules
1. **Construct downstream input `source_url`**:
   - Preferred: Use the upstream `source_url` scalar directly via direct-url resolver.
   - Alternative: If `source_url` is unavailable, extract from `metadata_file` using JSON path `$.source_url` or `$.youtube_url`.
2. **Materialize artifacts** before invoking the downstream skill.
3. **Do not** pass `metadata_file` as primary input; it is optional context only.
4. Ensure the resolved URL is a valid YouTube watch URL.

### Downstream Required Inputs
- `source_url`: URL string (required) – obtained as above.

### Output Expectations
- `analysis_file`: Markdown file at `raw/youtube-deep-research/{pipeline_id}/outputs/analysis.md`
- `transcript_file`: Text file at `raw/youtube-deep-research/{pipeline_id}/outputs/transcript.txt`

### Error Handling
- If neither source_url scalar nor valid JSON path yields a URL, fail with clear message.
- Validate URL format before proceeding.

### Post-Execution
- Confirm output files exist and are non-empty.
- Relay outputs to next edge if applicable.
