# Architecture

```text
CLI / Desktop / FastAPI
          |
      Orchestrator
          |
  Engine registry + adapters
   |        |       |       |
AudioSep  Demucs  Spleeter  UMX
          |
  External native processes
          |
Artifacts + SQLite + JSON manifest
```

The UI layers never construct engine-specific commands. Each adapter owns detection, installation guidance, command construction, and artifact discovery.
