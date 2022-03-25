import pytest
from typer.testing import CliRunner
from bumpCversion import app


runner = CliRunner()

@pytest.fixture(name='doxydir')
def doxydir():
    with open('./tests/test_version/Doxyfile', 'r', errors="ignore",encoding='utf-8', newline= '') as input:
        content = input.read()
    return content
    
def test_dry():
    result = runner.invoke(
        app, ["dry-run", "./sample_files/.bump.cfg", "naibsp", "minor", "True"])
    assert result.exit_code == 0
    assert "Current version" in result.stdout

def test_doxy(doxydir):
    assert 'PROJECT_NAME' in doxydir


