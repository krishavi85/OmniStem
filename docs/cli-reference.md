# CLI reference

Run `omnistem --help` and command-specific `--help` for the authoritative installed reference.

Core commands:

```text
omnistem doctor
omnistem env
omnistem engines list
omnistem models list
omnistem inspect FILE
omnistem separate FILE
omnistem batch DIRECTORY
omnistem ensemble FILE FILE --output FILE
omnistem history list
omnistem serve
omnistem desktop
```

`separate` supports `--dry-run` to validate and reveal the exact native command before execution. Use `--extra-arg` only with flags verified against the selected upstream engine version.
