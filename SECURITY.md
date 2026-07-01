# Security policy

## Supported version

Security fixes target the latest released minor version.

## Reporting

Open a private GitHub security advisory when the repository is published. Do not disclose exploitable vulnerabilities in a public issue before a fix is available.

## Security properties

- Native engine commands are passed as argument arrays, not interpolated shell strings.
- Input files must exist and use an allowed audio extension.
- OmniStem never overwrites the original input.
- The API binds to `127.0.0.1` by default.
- Telemetry and cloud upload are absent.
- Model files are not bundled.

## Remaining risk

Installed engines, models, FFmpeg builds, and plugins are third-party executable code. Install them only from trusted sources and verify hashes where upstream publishes them.
