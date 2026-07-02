Use skill article-writer to execute this Node Execution Request.

# Node Execution Request

Runtime context:
- runtime_id: runtime-206-189-196-65
- instance_id: agent-runtime-codex-smoke
- workflow_id: youtube-research-wiki
- node_id: article-writer-a2a
- node_run_id: node-run-article-writer-a2a-20260702T140937-a99f26

Input contract:
- entry_inputs: {
  "prompt": "写一篇中文分析文章。"
}
- input_manifest_path: raw/node-runs/node-run-article-writer-a2a-20260702T140937-a99f26/inputs/sources/manifest.json
- input_directory: raw/node-runs/node-run-article-writer-a2a-20260702T140937-a99f26/inputs/sources
- source_url: https://www.youtube.com/watch?v=Ahfe-BW1cFc
- Only use files listed in the input manifest unless the selected skill already has a stricter rule.

Relay context:
No upstream relay context was provided for this run.

Approved Edge Handoff Guide:
No approved Edge Handoff Guide was resolved for this run.

Output contract:
- output_directory: raw/node-runs/node-run-article-writer-a2a-20260702T140937-a99f26/outputs
- output_manifest_path: raw/node-runs/node-run-article-writer-a2a-20260702T140937-a99f26/outputs/manifest.json
- receipt_path: raw/node-runs/node-run-article-writer-a2a-20260702T140937-a99f26/agent/receipt.json
- Do not report success unless the declared output manifest and receipt are written or the runtime wrapper writes equivalent state that the adapter can verify.

Execution command:
```bash

```
If the execution command is empty, execute the selected skill directly from this request: read entry_inputs, input_directory, input_manifest and the approved handoff guide, then write outputs to output_directory and output_manifest_path.


Execution rules:
- Use the selected skill only: article-writer.
- Run the command from the Instance workspace unless the skill has an equivalent deterministic wrapper.
- Preserve the provided environment variables.
- Do not invent paths.
- If execution fails, return the failure and include stderr/log guidance.
