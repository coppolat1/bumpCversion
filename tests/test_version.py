import pytest
from bumpCversion import parse_args

@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help(capsys, option):
    parse_args(option)
    output = capsys.readouterr()
    assert "usage" in output


@pytest.mark.parametrize("dryrun", (None, "--dry-run"))
def test_dry(capsys, dryrun):
    output = capsys.readouterr()
    print('')
    assert "Current version =" in output

