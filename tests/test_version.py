import pytest
from bumpCversion import main


@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help(capsys, option):
    try:
        main([option])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    assert "usage" in output


# @pytest.mark.parametrize("dryrun", (None, "--dry-run"))
# def test_dry(capsys, dryrun):
#     print_dry()
#     output = capsys.readouterr()
#     assert "Current version =" in output

