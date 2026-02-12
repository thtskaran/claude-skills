# Claude Skills

Personally curated, self-tested skills for Claude Code — an experimental attempt to make vibe coding actually useful.

Each skill here is battle-tested on real codebases before being published.

## Skills

### `/deslop`
Audit and harden AI-generated (vibe-coded) codebases for production. Two-phase workflow: first a structured multi-pass audit (`AUDIT.md`), then systematic fixes applied in safety-tiered order. Language-agnostic. Never changes business logic — only hardens, cleans, and robustifies.

**Install:** Copy the `deslop/` directory to `~/.claude/skills/deslop/`

**Example output:** [`deslop/examples/AUDIT-claude-researcher.md`](deslop/examples/AUDIT-claude-researcher.md) — real audit of a multi-agent research system

## Contributing

Feel free to open PRs — new skills, improvements to existing ones, bug fixes, all welcome.

## License

MIT

## Contact

Karan Prasad — hello@KaranPrasad.com
