Use skill sop-youtube-deep-research to execute this downstream node.

## Node Execution Guide
- Edge: youtube-fetch -> youtube-deep-research
- Evaluation summary: 上下游存在显式映射，且下游输入接受多种解析方式，可稳定执行。
- Edge Handoff Instruction: 将 youtube-fetch 输出的 source_url 直接传递给 youtube-deep-research 的 source_url 输入；metadata_file 作为补充上下文不作为主输入，但可通过 json_path 解析器从中提取 source_url 备用。

### Upstream artifacts
- **source_url**: `raw/node-runs/{pipeline_id}/outputs/files/source-url.txt` (text file containing the URL)
- **metadata_file**: `raw/node-runs/{pipeline_id}/outputs/files/metadata.json` (JSON file with possible fields like source_url, youtube_url)

### Input construction for downstream
- **Primary**: Directly use the content of `source-url.txt` as the value for `source_url` input.
- **Fallback**: If `source-url.txt` is unavailable, parse `metadata.json` using json_path `$.source_url` or `$.youtube_url` to extract the URL.

### Execution steps
1. Retrieve the upstream artifacts from the resolved paths.
2. Determine the `source_url` value using the primary or fallback method.
3. Invoke `sop-youtube-deep-research` with the constructed input.
4. Ensure outputs are saved to the designated paths.

### Notes
- The `source_url` is required; the metadata_file is optional and only serves as backup.
- All file paths are relative to the instance workspace.
