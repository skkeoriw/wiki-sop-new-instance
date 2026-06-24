Use skill sop-wiki-build to execute this Node Execution Request.

# Node Execution Request

Runtime context:
- runtime_id: runtime-152-32-214-95
- instance_id: test-instance
- workflow_id: youtube-research-wiki
- node_id: wiki-build
- node_run_id: node-run-wiki-build-20260622T135212-cc0bec

Input contract:
- input_manifest_path: raw/node-runs/node-run-wiki-build-20260622T135212-cc0bec/inputs/sources/manifest.json
- input_directory: raw/node-runs/node-run-wiki-build-20260622T135212-cc0bec/inputs/sources
- source_url: https://www.youtube.com/watch?v=dQw4w9WgXcQ
- Only use files listed in the input manifest unless the selected skill already has a stricter rule.

Output contract:
- output_directory: raw/node-runs/node-run-wiki-build-20260622T135212-cc0bec/outputs/files
- output_manifest_path: raw/node-runs/node-run-wiki-build-20260622T135212-cc0bec/outputs/files/manifest.json
- receipt_path: raw/node-runs/node-run-wiki-build-20260622T135212-cc0bec/agent/receipt.json
- Do not report success unless the declared output manifest and receipt are written or the runtime wrapper writes equivalent state that the adapter can verify.

Execution command:
```bash
bash /root/agent-brain-plugins/youtube-wiki/skills/sop-wiki-build/scripts/run_wiki_build.sh /root/wiki/wiki-sop-new-instance node-run-wiki-build-20260622T135212-cc0bec node-run-wiki-build-20260622T135212-cc0bec
```

Execution rules:
- Use the selected skill only: sop-wiki-build.
- Run the command from the Instance workspace unless the skill has an equivalent deterministic wrapper.
- Preserve the provided environment variables.
- Do not invent paths.
- If execution fails, return the failure and include stderr/log guidance.
