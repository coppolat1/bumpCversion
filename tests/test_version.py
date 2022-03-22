import pytest
from bumpCversion import main, parse_args


@pytest.fixture
def my_parser():
    return parse_args("--dry-run")

@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help(capsys, option):
    try:
        main([option])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    assert "usage" in output


# @pytest.mark.parametrize("dryrun", (None, "--dry-run"))
# def test_arg(capsys, dryrun):
#     print_dry()
#     output = capsys.readouterr()
#     assert "Current version =" in output

# def test_something():
#         assert "Current" in my_parser