import pathlib
from pathlib import Path
from renamer.entry import update_classname


def test_rename():
    got = update_classname(
        './fixtures/source.py',
        'A',
        'B',
    )

    assert got == Path('./fixtures/expected.py').read_text()
    assert pathlib.Path('./fixtures/source_refactorred_.py').exists()


def test_rename_with_imports():
    update_classname(
        './fixtures/source.py',
        'A',
        'B',
        './fixtures/'
    )
    f_got = pathlib.Path('./fixtures/import_source_refactorred_.py')
    assert f_got.exists()
    assert f_got.read_text() == pathlib.Path('./fixtures/import_expected.py').read_text()
