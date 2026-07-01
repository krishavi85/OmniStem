from __future__ import annotations

from omnistem.core.types import ModelDescriptor

_MODELS = (
    ModelDescriptor(
        id="htdemucs_ft",
        display_name="Demucs HTDemucs fine-tuned",
        engine="demucs",
        architecture="HTDemucs",
        supported_stems=("vocals", "drums", "bass", "other"),
        license="Model terms are supplied by the upstream Demucs project",
        repository_url="https://github.com/adefossez/demucs",
        notes="Four-stem model; use two-stems mode for vocals/instrumental.",
    ),
    ModelDescriptor(
        id="htdemucs_6s",
        display_name="Demucs six-source",
        engine="demucs",
        architecture="HTDemucs",
        supported_stems=("vocals", "drums", "bass", "guitar", "piano", "other"),
        license="Model terms are supplied by the upstream Demucs project",
        repository_url="https://github.com/adefossez/demucs",
    ),
    ModelDescriptor(
        id="model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        display_name="BS-RoFormer Viperx 1297",
        engine="audio-separator",
        architecture="MDXC/BS-RoFormer",
        supported_stems=("vocals", "instrumental"),
        license="Check model-specific metadata before commercial use",
        repository_url="https://github.com/nomadkaraoke/python-audio-separator",
    ),
    ModelDescriptor(
        id="UVR-MDX-NET-Inst_HQ_3.onnx",
        display_name="UVR MDX-Net Inst HQ 3",
        engine="audio-separator",
        architecture="MDX-Net",
        supported_stems=("vocals", "instrumental"),
        license="Check model-specific metadata before commercial use",
        repository_url="https://github.com/nomadkaraoke/python-audio-separator",
    ),
    ModelDescriptor(
        id="spleeter:2stems",
        display_name="Spleeter 2-stem",
        engine="spleeter",
        architecture="Spleeter",
        supported_stems=("vocals", "instrumental"),
        license="MIT code; pretrained-model terms remain upstream",
        repository_url="https://github.com/deezer/spleeter",
    ),
    ModelDescriptor(
        id="umxhq",
        display_name="Open-Unmix UMXHQ",
        engine="openunmix",
        architecture="Open-Unmix",
        supported_stems=("vocals", "drums", "bass", "other"),
        license="Code MIT; verify pretrained-weight license upstream",
        repository_url="https://github.com/sigsep/open-unmix-pytorch",
    ),
)


def list_models(engine: str | None = None, query: str | None = None) -> list[ModelDescriptor]:
    models = list(_MODELS)
    if engine:
        models = [model for model in models if model.engine == engine]
    if query:
        needle = query.casefold()
        models = [
            model
            for model in models
            if needle in model.id.casefold()
            or needle in model.display_name.casefold()
            or any(needle in stem.casefold() for stem in model.supported_stems)
        ]
    return models


def get_model(model_id: str) -> ModelDescriptor:
    for model in _MODELS:
        if model.id == model_id:
            return model
    raise KeyError(model_id)
