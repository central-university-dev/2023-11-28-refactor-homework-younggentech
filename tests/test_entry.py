import pathlib
from pathlib import Path
from renamer.entry import update_classname
FIXTURE_PATH = "./tests/fixtures/"


def test_rename():
    got = update_classname(
        FIXTURE_PATH + "source.py",
        "A",
        "B",
    )

    assert got == Path(FIXTURE_PATH + "expected.py").read_text()
    assert pathlib.Path(FIXTURE_PATH + "source_refactorred_.py").exists()


def test_rename_with_imports():
    update_classname(
        FIXTURE_PATH + "source.py",
        "A",
        "B",
        FIXTURE_PATH
    )
    f_got = pathlib.Path(FIXTURE_PATH + "import_source_refactorred_.py")
    assert f_got.exists()
    assert f_got.read_text() == pathlib.Path(FIXTURE_PATH + "import_expected.py").read_text()
