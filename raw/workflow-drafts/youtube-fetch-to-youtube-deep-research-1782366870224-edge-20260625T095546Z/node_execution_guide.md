Use skill sop-youtube-deep-research to execute this downstream node.

## Node Execution Guide
- Edge: youtube-fetch -> youtube-deep-research
- Evaluation summary: 上游source_url可直接映射到下游source_url，意图清晰；metadata_file的映射存在混淆，但作为补充不成阻塞。
- Edge Handoff Instruction: 将 youtube-fetch 输出的 source_url 直接传递给 youtube-deep-research 的 source_url 输入；metadata_file 作为补充上下文不作为主输入，但可通过 json_path 解析器从中提取 source_url 备用。

### Upstream artifacts
- **source_url** (scalar url): raw/node-runs/{pipeline_id}/outputs/files/source-url.txt
- **metadata_file** (file json): raw/node-runs/{pipeline_id}/outputs/files/metadata.json

### Downstream input construction
1. **source_url**: Use the upstream `source_url` artifact directly via direct-url resolver. If unavailable, fall back to extracting `source_url` from `metadata_file` using json_path resolver (path: `$.source_url`).
2. Note: The relay mapping for `metadata_file` uses an incorrect direct-url resolver; ignore that mapping for production and use json_path if needed.

### Execution steps
1. Read upstream artifacts from paths above.
2. Construct the `source_url` input for downstream as per construction.
3. Execute the skill `sop-youtube-deep-research` with the constructed input.
4. Verify outputs: analysis_file and transcript_file are written to their expected paths.

### Expected outputs
- **analysis_file**: raw/youtube-deep-research/{pipeline_id}/outputs/analysis.md
- **transcript_file**: raw/youtube-deep-research/{pipeline_id}/outputs/transcript.txt
