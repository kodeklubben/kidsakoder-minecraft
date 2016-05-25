"""
Unittests for testing internal functions
"""

import pytest
from flask_app import files


def test_join_path():
    """ Test if paths are joined correctly """
    result = files.safe_join_all('/test/path', 'more/path', 'one_path', 'even/more/path', 'filename.zip')
    assert result == '/test/path/more/path/one_path/even/more/path/filename.zip'

    result = files.safe_join_all('apath/', '/more//path', 'andstuff')
    assert result == 'apath/./more/./path/andstuff'
