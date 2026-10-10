# Changelog

## Unreleased

- Ecosystem standardization: SECURITY.md, CONTRIBUTING.md, requirements, CI smoke checks.

## 1.0.0 (2026-09-18)

- Initial stable single-tool release (educational, authorized-use only).

## [3.0.0] - 2026-10-10
### Added
- Unified TBH v3 CLI: --proxy, --cookie, -H, --timeout, --version, --no-color
- Structured findings (severity + fix) with exit codes (1 on Medium/High)
- Threaded port scan (15 ports), 8-subdomain DNS enum, 6-header audit, X-Powered-By check
- JSON report schema with tool/version/target/ip/findings
### Fixed
- Bare except on DNS, utcnow deprecation, unhandled request failures

## [3.1.0] - 2026-10-11
### Added
- Multi-target scanning: --targets file (one URL per line)
- Aggregated JSON {targets, summary} for scope-wide recon
- -u no longer required when --targets is given; unresolvable targets skipped
