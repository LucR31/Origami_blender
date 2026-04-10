import subprocess
import os

env = os.environ.copy()

env["PYTHONPATH"] = "/Users/lucas/Desktop/Origami_blender:" + env.get("PYTHONPATH", "")

subprocess.run([
    "/Applications/Blender.app/Contents/MacOS/Blender",
    "-b",
    "--python",
    "/Users/lucas/Desktop/Origami_blender/tests/run_tests.py"
], env=env)