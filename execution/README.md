# Layer 3: Execution (Doing the work)

- Deterministic Python scripts.
- Environment variables, api tokens, etc are stored in `.env`.
- Handle API calls, data processing, file operations, database interactions.
- Reliable, testable, fast. Use scripts instead of manual work.

This directory contains the Python scripts that perform the actual work.

## File Structure

```text
execution/
├── README.md           # This file
├── [script_name].py    # Deterministic Python scripts (e.g., scrape_single_site.py)
└── ...
```

Note: Environment variables for these scripts are stored in the root `.env` file.

## The 3-Layer Architecture

This folder represents **Layer 3** of the system architecture:

1.  **Directives (Layer 1):** define WHAT to do (SOPs).
2.  **Orchestration (Layer 2):** (The Agent) routes intent to execution.
3.  **Execution (Layer 3):** Deterministic scripts that DO the work.

## Self-annealing Loop

Scripts in this directory should be written to support the self-annealing loop:

1.  **Fix it:** When a script breaks, fix the script.
2.  **Update the tool:** Ensure the tool uses the fixed script.
3.  **Test:** Verify it works.
4.  **Update Directive:** Reflect learnings (API limits, edge cases) in Layer 1.
