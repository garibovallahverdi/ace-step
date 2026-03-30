import subprocess
from pathlib import Path

OUTPUT = Path("output.wav")

def generate_audio(text: str):
    cmd = [
        "python",
        "acestep/infer.py",   # repo içindəki script
        "--text", text,
        "--output", str(OUTPUT)
    ]

    print("Running ACE-Step locally...")
    subprocess.run(cmd, check=True)

    if OUTPUT.exists():
        print("✅ Audio generated:", OUTPUT)
    else:
        print("❌ Failed")

if __name__ == "__main__":
    generate_audio("Salam! Bu real fix-dir 🚀")
