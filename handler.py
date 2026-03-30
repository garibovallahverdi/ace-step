import runpod
import subprocess
from pathlib import Path
import uuid

def handler(job):
    job_input = job["input"]
    prompt = job_input.get("text", "Hello world")

    output_file = Path(f"/tmp/{uuid.uuid4()}.wav")

    cmd = [
        "python",
        "acestep/infer.py",
        "--text", prompt,
        "--output", str(output_file)
    ]

    try:
        subprocess.run(cmd, check=True)

        return {
            "status": "success",
            "file": str(output_file)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

runpod.serverless.start({"handler": handler})
