import pytest
from typer.testing import CliRunner
from bumpCversion import app
from filetypes import SemanticVersionNumber
# import magic

runner = CliRunner()

@pytest.fixture(name='doxydir')
def doxydir():
    with open('./tests/test_version/Doxyfile', 'r', errors="ignore",encoding='utf-8', newline= '') as input:
        content = input.read()
    return content

# @pytest.fixture(name='doxyfile')
# def doxyfile():
#     ret_val = magic.from_file('Doxyfile')
#     return ret_val

@pytest.fixture(name='version_num')
def version_num():
    version = SemanticVersionNumber(1, 2, 3)
    return version


def test_dry():
    result = runner.invoke(
        app, ["dry-run", "./sample_files/.bump.cfg", "naibsp", "minor"])
    assert result.exit_code == 0
    assert "Current version" in result.stdout

# def test_doxy_type(doxyfile):
#     x = 0
#     assert x == 0

def test_doxy_vaild(doxydir):
    assert 'PROJECT_NAME' in doxydir

def test_version(version_num):
    assert version_num.major == 1
    assert version_num.minor == 2
    assert version_num.patch == 3

def test_bump_major(version_num):
    version_num.bump("major", False)
    assert version_num.major == 2

def test_bump_minor(version_num):
    version_num.bump("minor", False)
    assert version_num.minor == 3

def test_bump_patch(version_num):
    version_num.bump("patch", False)
    assert version_num.patch == 4

def test_bump_major_reset(version_num):
    version_num.bump("major", True)
    assert version_num.major == 2
    assert version_num.minor == 0
    assert version_num.patch == 0

def test_bump_minor_reset(version_num):
    version_num.bump("minor", True)
    assert version_num.minor == 3
    assert version_num.patch == 0

def test_bump_patch_reset(version_num):
    version_num.bump("patch", True)
    assert version_num.patch == 4
    


