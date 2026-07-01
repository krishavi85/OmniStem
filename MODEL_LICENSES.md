# Model and checkpoint licensing

Model weights are not bundled with OmniStem.

A permissive source-code license does **not** automatically grant the same rights for pretrained weights or training datasets. Before commercial use, inspect the model card, checkpoint source, author notes, and dataset terms.

Known caution:

- Open-Unmix documents that its `umxl` weights are non-commercial (CC BY-NC-SA 4.0). Do not treat `umxl` as commercially licensed merely because Open-Unmix code is MIT.
- UVR-distributed MDX, MDXC, VR, BS-RoFormer, and Mel-Band RoFormer checkpoints may have model-specific terms. OmniStem therefore reports a caution rather than inventing a license.
- Demucs checkpoint and dataset terms should be reviewed at the upstream repository before redistribution or commercial embedding.
- Spleeter code is MIT, but users remain responsible for pretrained-model and source-material rights.

OmniStem records the chosen native model identifier in every job manifest to support later compliance audits.
