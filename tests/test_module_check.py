"""
Test for module_check.py

Ensures that importing module_check does not produce side effects (printing)
"""
import subprocess
import sys


def test_module_check_no_side_effect():
    """Test that importing module_check produces no output"""
    # Run Python with import of module_check and capture output
    result = subprocess.run(
        [sys.executable, '-c', 'import module_check'],
        capture_output=True,
        text=True,
        cwd='/home/runner/work/adiftools-dev/adiftools-dev'
    )
    
    # Should have no stdout when importing
    assert result.stdout == '', f"Expected no output, but got: {result.stdout}"
    assert result.returncode == 0


def test_module_check_main_produces_output():
    """Test that running module_check as __main__ produces expected output"""
    result = subprocess.run(
        [sys.executable, 'module_check.py'],
        capture_output=True,
        text=True,
        cwd='/home/runner/work/adiftools-dev/adiftools-dev'
    )
    
    # Should produce output when run as main
    assert result.stdout.strip() != '', "Expected output when run as __main__"
    assert 'adiftools' in result.stdout
    assert result.returncode == 0
