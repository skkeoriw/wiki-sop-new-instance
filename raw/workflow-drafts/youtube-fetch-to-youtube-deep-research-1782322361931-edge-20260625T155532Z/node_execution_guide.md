Use skill sop-youtube-deep-research to execute this downstream node.

## Node Execution Guide
- Edge: youtube-fetch -> youtube-deep-research
- Evaluation summary: 上下游存在直接同名输入输出映射，显式引用清晰，可稳定生成节点执行指导。
- Edge Handoff Instruction: 从上游 outputs 中读取 source_url 传给下游节点

### Upstream artifacts
- source_url: raw/node-runs/{pipeline_id}/outputs/files/source-url.txt
- metadata_file: raw/node-runs/{pipeline_id}/outputs/files/metadata.json (supporting context)

### Execution rules
- **Primary input**: Use the resolved source_url from upstream. It is a URL string.
- **Execution command**: Execute the downstream skill with the source_url as input.
- **No additional user input required.**

### Steps
1. Read source_url from the upstream output file.
2. Pass source_url to the downstream node's input.
3. Run the downstream skill `sop-youtube-deep-research`.
4. Verify that analysis_file and transcript_file are generated.

### Notes
- The upstream metadata_file is not required but can be used for additional context if needed.
- The handoff is automatic; no manual mapping is required.
