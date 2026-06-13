from pathlib import Path

from scripts.run_all_examples import discover_examples, is_optional_example


def test_optional_marker_is_detected(tmp_path: Path) -> None:
    script = tmp_path / "example.py"
    script.write_text("# ci: optional-example\nprint('skip')\n", encoding="utf-8")
    assert is_optional_example(script) is True


def test_discovery_separates_runnable_and_optional_examples(tmp_path: Path) -> None:
    examples = tmp_path / "examples"
    examples.mkdir()
    runnable = examples / "runnable.py"
    optional = examples / "training.py"
    hidden = examples / "__init__.py"
    runnable.write_text("print('run')\n", encoding="utf-8")
    optional.write_text("# ci: optional-example\nprint('train')\n", encoding="utf-8")
    hidden.write_text("", encoding="utf-8")

    runnable_files, optional_files = discover_examples(tmp_path)

    assert runnable_files == [runnable]
    assert optional_files == [optional]
