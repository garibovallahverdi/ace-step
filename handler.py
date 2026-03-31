import runpod
import subprocess
from pathlib import Path
import uuid
import base64

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

        with open(output_file, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode()

        return {
            "status": "success",
            "audio": audio_base64
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

runpod.serverless.start({"handler": handler})
