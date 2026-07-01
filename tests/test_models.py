import pytest

from omnistem.core.model_registry import get_model, list_models


def test_model_search_by_stem() -> None:
    results = list_models(query="guitar")
    assert any(model.id == "htdemucs_6s" for model in results)


def test_model_filter_by_engine() -> None:
    results = list_models(engine="spleeter")
    assert results
    assert all(model.engine == "spleeter" for model in results)


def test_unknown_model_raises() -> None:
    with pytest.raises(KeyError):
        get_model("not-real")
