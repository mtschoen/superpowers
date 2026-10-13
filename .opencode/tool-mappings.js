// Tool mapping injected into the bootstrap, differentiated by host flavor.
// V1 (OpenCode 1.18.x) and V2 (OpenCode 2.0.4/2.0.7) expose different built-in
// tools, so each flavor's injection path picks its own constant below.
// Kept out of plugins/superpowers.js because an older V1 loader invokes every
// export of the plugin module and fails on a string. Exported for tests
// (tests/opencode/test-bootstrap-caching.mjs).

// V1 built-ins: todowrite, task (subagent_type), skill, read, apply_patch,
// bash, grep, glob, webfetch.
export const V1_MAPPING = `**Tool Mapping for OpenCode:**
When skills request actions, substitute OpenCode equivalents:
- Create or update todos → \`todowrite\`
- \`Subagent (general-purpose):\` → \`task\` with \`subagent_type: "general"\`
- Invoke a skill → OpenCode's native \`skill\` tool
- Read files → \`read\`
- Create, edit, or delete files → \`apply_patch\`
- Run shell commands → \`bash\`
- Search files → \`grep\`, \`glob\`
- Fetch a URL → \`webfetch\`

Use OpenCode's native \`skill\` tool to list and load skills.`;

// V2 built-ins: no todo tool at all; task → subagent (agent name in 'agent',
// continuation via sessionID); apply_patch → patch (patchText, same patch
// format); bash → shell. read, write, edit, grep, glob, webfetch, websearch,
// and skill all exist under those names (verified against the 2.0.4 and 2.0.7
// host contracts).
export const V2_MAPPING = `**Tool Mapping for OpenCode:**
When skills request actions, substitute OpenCode equivalents:
- Create or update todos → OpenCode v2 has no todo tool; track the plan in a markdown file (or the harness's plan facility) instead
- \`Subagent (general-purpose):\` → \`subagent\` with \`agent: "general"\` (give it \`description\` and \`prompt\`, optionally \`background\`; pass \`sessionID\` to continue a previous subagent)
- Invoke a skill → OpenCode's native \`skill\` tool
- Read files → \`read\`
- Create, edit, or delete files → use \`patch\` with \`patchText\` when available; otherwise use \`write\` to create or overwrite files, \`edit\` for targeted changes, and \`shell\` for deletion
- Run shell commands → \`shell\` (\`command\`, \`workdir\`, \`timeout\`, \`background\`)
- Search files → \`grep\`, \`glob\`
- Fetch a URL → \`webfetch\`
- Search the web → \`websearch\`

Use OpenCode's native \`skill\` tool to list and load skills.`;
