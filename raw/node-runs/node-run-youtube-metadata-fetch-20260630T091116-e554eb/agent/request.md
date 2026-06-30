Use skill youtube-metadata-fetch to execute this Node Execution Request.

# Node Execution Request

Runtime context:
- runtime_id: youtube-wiki
- instance_id: wiki-sop-new-instance
- workflow_id: youtube-research-wiki
- node_id: youtube-metadata-fetch
- node_run_id: node-run-youtube-metadata-fetch-20260630T091116-e554eb

Input contract:
- entry_inputs: {
  "source_url": "raw/node-runs/node-run-youtube-metadata-fetch-20260630T091116-e554eb/inputs/sources/0001.txt"
}
- input_manifest_path: raw/node-runs/node-run-youtube-metadata-fetch-20260630T091116-e554eb/inputs/sources/manifest.json
- input_directory: raw/node-runs/node-run-youtube-metadata-fetch-20260630T091116-e554eb/inputs/sources
- source_url: raw/node-runs/node-run-youtube-metadata-fetch-20260630T091116-e554eb/inputs/sources/0001.txt
- Only use files listed in the input manifest unless the selected skill already has a stricter rule.

Relay context:
No upstream relay context was provided for this run.

Approved Edge Handoff Guide:
No approved Edge Handoff Guide was resolved for this run.

Output contract:
- output_directory: raw/node-runs/node-run-youtube-metadata-fetch-20260630T091116-e554eb/outputs
- output_manifest_path: raw/node-runs/node-run-youtube-metadata-fetch-20260630T091116-e554eb/outputs/manifest.json
- receipt_path: raw/node-runs/node-run-youtube-metadata-fetch-20260630T091116-e554eb/agent/receipt.json
- Do not report success unless the declared output manifest and receipt are written or the runtime wrapper writes equivalent state that the adapter can verify.

Execution command:
```bash

```
If the execution command is empty, execute the selected skill directly from this request: read entry_inputs, input_directory, input_manifest and the approved handoff guide, then write outputs to output_directory and output_manifest_path.


Execution rules:
- Use the selected skill only: youtube-metadata-fetch.
- Run the command from the Instance workspace unless the skill has an equivalent deterministic wrapper.
- Preserve the provided environment variables.
- Do not invent paths.
- If execution fails, return the failure and include stderr/log guidance.
