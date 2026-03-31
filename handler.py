import runpod
import subprocess
from pathlib import Path
import uuid
import base64
import os

def handler(job):
    job_input = job["input"]
    prompt = job_input.get("text", "")
    
    if not prompt:
        return {
            "status": "error",
            "message": "No text prompt provided"
        }
    
    # DÜZGÜN YOL - ACE-Step-1.5 qovluğu
    ace_step_path = Path("/app/ACE-Step-1.5")
    
    if not ace_step_path.exists():
        return {
            "status": "error",
            "message": f"ACE-Step directory not found at {ace_step_path}"
        }
    
    # infer.py faylını yoxla
    infer_py = ace_step_path / "infer.py"
    
    if not infer_py.exists():
        # Alternativ yolları yoxla
        possible_paths = [
            ace_step_path / "inference.py",
            ace_step_path / "run.py",
            ace_step_path / "main.py",
            Path("/app/acestep/infer.py"),
            Path("/app/infer.py")
        ]
        
        for path in possible_paths:
            if path.exists():
                infer_py = path
                break
        
        if not infer_py.exists():
            # Faylları listele
            files = list(ace_step_path.glob("*.py"))
            return {
                "status": "error",
                "message": f"infer.py not found. Available py files: {[f.name for f in files]}"
            }
    
    output_file = Path(f"/tmp/{uuid.uuid4()}.wav")
    
    # Komanda - düzgün yol ilə
    cmd = [
        "python",
        str(infer_py),
        "--text", prompt,
        "--output", str(output_file)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(ace_step_path),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT: {result.stdout[:500]}")
        if result.stderr:
            print(f"STDERR: {result.stderr[:500]}")
        
        if result.returncode != 0:
            return {
                "status": "error",
                "message": f"Command failed: {result.stderr}"
            }
        
        if not output_file.exists():
            return {
                "status": "error",
                "message": f"Output file not created: {output_file}"
            }
        
        with open(output_file, "rb") as f:
            audio_data = f.read()
        
        audio_base64 = base64.b64encode(audio_data).decode()
        output_file.unlink()
        
        return {
            "status": "success",
            "audio": audio_base64,
            "size_bytes": len(audio_data)
        }
        
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Command timeout after 120 seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

runpod.serverless.start({"handler": handler})
