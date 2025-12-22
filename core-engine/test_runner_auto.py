# Quick test script for test_runner
# This simulates user input to test the runner

import io
import sys

# Simulate user inputs
test_inputs = """

90mm
rohit
2_panel_slide
5
4
1
n

0
20
"""

# Redirect stdin
old_stdin = sys.stdin
sys.stdin = io.StringIO(test_inputs)

try:
    # Run the interactive test
    from test_runner import run_interactive
    run_interactive()
finally:
    # Restore stdin
    sys.stdin = old_stdin

print("\n[SUCCESS] Test runner executed successfully with new engine!")
