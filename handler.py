from pathlib import Path
import subprocess

# Output fayl
OUTPUT_FILE = Path("output.wav")

def run_acestep(prompt="Hello world"):
    """
    RunPod ACE-Step model call
    Burada RunPod-un hazır environment-i istifadə olunur.
    """
    # Model CLI çağırışı (ACE-Step command-line)
    # ⚡ Note: RunPod-da ACE-Step CLI artıq quraşdırılıb
    cmd = [
        "acestep",           # ACE-Step binary
        "--text", prompt,
        "--out", str(OUTPUT_FILE)
    ]
    
    subprocess.run(cmd, check=True)
    print(f"Audio generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    prompt = "Salam! Bu bir test audio mesajıdır."
    run_acestep(prompt)
