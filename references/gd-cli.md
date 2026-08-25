<!--
[INPUT]: Depends on confirmed absence of a native image-generation tool, the parent's exact final prompt, user-provided or task-required images, Node.js 20+ with npm or pnpm, and the live authentication, organization, image.generate Tool, and vivi-image-2-0 contracts returned by gd-cli
[OUTPUT]: Provides first-run installation and verification, authentication and organization setup, a fixed vivi-image-2-0 request profile, pre-charge confirmation, request JSON, minimal image inputs, output persistence, error handling, and no automatic paid retry
[POS]: Fallback renderer adapter in references, loaded by SKILL.md only when the runtime has no native image-generation tool; it does not define the sticker sheet's visual design
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# GD CLI Fallback Renderer

[Routing](#routing-gate) · [Setup](#first-run-setup) · [Contract](#verify-the-live-contract) · [Input](#build-the-input) · [Call](#call-and-persist) · [Retry](#no-automatic-correction) · [Errors](#error-contract) · [Evidence](#return-evidence)

## Routing Gate

- This is not a peer alternative to native image generation. If the runtime exposes any callable native image-generation tool, return to the parent workflow without inspecting, installing, or calling GD CLI.
- Enter this flow only when the runtime exposes no native image-generation tool. Native failure, rate limiting, latency, poor output, or a user-requested correction does not count as tool absence.
- The parent Skill still owns source inspection, final-prompt writing, and the minimal delivery check. Call the atomic `image.generate` Tool; do not start a GD CLI Agent workflow.
- Keep the final prompt backend-neutral. Renderer-specific fields belong only in the request JSON.

## First-run Setup

Installation alone is not readiness. Verify the command, version, authentication, organization, and `image.generate` separately.

1. Run read-only checks first:

   ```bash
   command -v gd-cli
   node --version
   command -v npm
   command -v pnpm
   ```

2. If `gd-cli` exists, run `gd-cli --version` and `gd-cli --help`. Do not reinstall or update automatically. If required commands are missing, disclose the incompatibility and obtain permission before running `gd-cli update`.
3. If `gd-cli` is missing, require Node.js 20 or later and at least one package manager. Do not silently install Node.js, install a package manager, or edit shell startup files. Explain that the public `gaoding-cli` package will be installed globally and obtain permission first.
4. Use one installed package manager and allow install scripts only for `gaoding-cli`:

   ```bash
   npm install --global --allow-scripts=gaoding-cli gaoding-cli
   # or
   pnpm add --global --allow-build=gaoding-cli gaoding-cli
   ```

   Do not default to `npx`, `pnpm dlx`, Yarn, `sudo`, or unrestricted install-script permissions.
5. Verify with `command -v gd-cli`, `gd-cli --version`, and `gd-cli --help`. If the package is installed but the command is unavailable, inspect `npm prefix --global` or `pnpm bin --global` and the current `PATH`; do not reinstall blindly.
6. Check authentication and organization:

   ```bash
   gd-cli auth status --json
   gd-cli auth login
   gd-cli org list --json
   gd-cli org current --json
   gd-cli org switch --org <org-id>
   ```

   Log in only when needed; use `--no-browser` when a browser cannot open. Never request credentials. Keep a valid current organization; otherwise show the real organization list and let the user choose. Never guess an organization ID.
7. Run `gd-cli tool list` and continue only if `image.generate` is available. Installation, login, organization switching, and the first paid submission are separate state changes. Explain each one and obtain confirmation before the first paid submission.

If any requirement remains unmet, stop the generation workflow and report the exact blocking requirement. Do not return the internal prompt as a substitute.

## Verify the Live Contract

Run immediately before constructing a paid request:

```bash
gd-cli tool list
gd-cli model get vivi-image-2-0
```

- Use `vivi-image-2-0` only. Do not select or fall back to another model.
- Fix every request to `width: "1200"`, `height: "2000"`, `resolution: "2K"`, and `quality: "medium"`.
- Recheck `model get vivi-image-2-0` before submission to confirm that these fields and values remain valid and to obtain the current price range and estimated duration. If the live contract no longer accepts this profile, stop and report the incompatibility without returning the internal prompt.
- Before submission, disclose the fixed model, current price range, and estimated duration.

## Build the Input

Build JSON from the live Model detail. Include:

- `model: "vivi-image-2-0"`;
- the final `prompt` unchanged;
- `width: "1200"` and `height: "2000"`;
- `resolution: "2K"` and `quality: "medium"`;
- only user-provided images or images strictly required by the current task, with the source cat first when applicable.

Never include `assets/yellow-cat-collage-anchor.png` in `image_urls`. Do not add unrelated recent images or automatic references. Use absolute `file://` URLs for local media so GD CLI can upload them temporarily; do not fabricate public URLs.

```json
{
  "model": "vivi-image-2-0",
  "prompt": "<exact-final-prompt>",
  "width": "1200",
  "height": "2000",
  "image_urls": [
    "file:///absolute/path/to/source-cat.png"
  ],
  "resolution": "2K",
  "quality": "medium"
}
```

## Call and Persist

```bash
gd-cli tool call image.generate --input request.json
# or pass the same JSON object through --input -
```

- Parse stdout as JSON and handle stderr warnings or errors separately.
- A successful result contains `content` and `usage`. Download the first image resource to `output/cat-sticker-sheets/`; verify its MIME type and raster content before choosing an extension, and never expose a complete signed URL.
- Task creation alone is not success; obtain an image that can be opened. The catalog price range in `usage` does not prove the amount actually charged.

## No Automatic Correction

- Do not submit another paid request because of count, layout, style, color, text, border, or other visual-review preferences.
- Submit a correction or fresh generation only when the user explicitly asks. Keep the source cat first; when a prior draft is required, label it as the result to edit rather than a style reference. Never add the bundled anchor.
- If a paid request may have been submitted but its terminal state is unknown, stop and report the uncertainty. Do not resubmit it.

## Error Contract

- Exit `0`: parse and verify the successful result.
- Exit `1`: runtime, service, or state failure; follow only published `error.details.next_steps`.
- Exit `2`: command or input error; inspect the relevant `--help`, then fix the call without guessing.
- Exit `130`: user interruption; stop immediately.
- Never expose access tokens, cookies, signatures, credentials, or complete signed URLs.

## Return Evidence

Record why fallback was entered, the fixed model, requested size, terminal state, current catalog price range, known boundary of the actual charge, and local output path. Then apply only the parent Skill's minimal delivery check.
