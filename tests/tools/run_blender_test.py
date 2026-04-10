from pathlib import Path
import subprocess
import os

ROOT = Path(__file__).resolve().parents[1]

env = os.environ.copy()
env["PYTHONPATH"] = str(ROOT) + ":" + env.get("PYTHONPATH", "")

subprocess.run([
    "/Applications/Blender.app/Contents/MacOS/Blender",
    "-b",
    "--python",
    str(ROOT / "run_tests.py")
], env=env)
