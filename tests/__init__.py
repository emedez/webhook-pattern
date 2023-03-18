import os
import sys

file_dir = os.path.dirname(__file__)
app_dir = os.path.abspath(os.path.join(
    file_dir,
    "..",
    "app",
))
print(app_dir)
sys.path.insert(0, app_dir)
