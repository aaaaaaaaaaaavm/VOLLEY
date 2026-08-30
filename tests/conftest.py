"""Put analysis/ and tools/ on the path so tests import the real modules.

The tests exercise the shipped code, not a copy of it. Nothing here defines a
model; if a test needs a number it asks the module that publishes it.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("analysis", "tools"):
    p = os.path.join(ROOT, d)
    if p not in sys.path:
        sys.path.insert(0, p)
