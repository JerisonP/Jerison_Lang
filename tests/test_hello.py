from pytest import CaptureFixture

from jerison_lang.hello_world import hello


def test_output(capsys: CaptureFixture):
    name = "Jerison"
    hello(name)
    captured = capsys.readouterr()
    assert captured.out == f"Hello {name}\n"
