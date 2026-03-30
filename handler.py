from pathlib import Path
import subprocess
import sys
import logging
import time
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Output file
OUTPUT_FILE = Path("/tmp/output.wav")

def check_acestep_installation():
    """Check if ACE-Step is properly installed"""
    try:
        result = subprocess.run(["acestep", "--help"], 
                              capture_output=True, 
                              text=True,
                              timeout=10)
        if result.returncode == 0:
            logger.info("ACE-Step is installed and accessible")
            return True
        else:
            logger.error(f"ACE-Step check failed: {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("ACE-Step command not found in PATH")
        return False
    except Exception as e:
        logger.error(f"Error checking ACE-Step: {e}")
        return False

def run_acestep(prompt: str = "Hello world", output_file: Optional[Path] = None) -> Path:
    """
    Run ACE-Step model to generate audio
    
    Args:
        prompt: Text to convert to speech
        output_file: Path to save audio file (default: /tmp/output.wav)
    
    Returns:
        Path to generated audio file
    """
    if output_file is None:
        output_file = OUTPUT_FILE
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Try different command formats based on ACE-Step version
    commands_to_try = [
        ["acestep", "--text", prompt, "--out", str(output_file)],
        ["ace-step", "--text", prompt, "--output", str(output_file)],
        ["python", "-m", "acestep", "--text", prompt, "--out", str(output_file)],
    ]
    
    for cmd in commands_to_try:
        try:
            logger.info(f"Trying command: {' '.join(cmd)}")
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True,
                                  timeout=300)  # 5 minute timeout
            if result.returncode == 0:
                logger.info(f"Audio generated successfully: {output_file}")
                if output_file.exists():
                    logger.info(f"File size: {output_file.stat().st_size} bytes")
                return output_file
            else:
                logger.warning(f"Command failed with return code {result.returncode}")
                logger.warning(f"stderr: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(cmd)}")
        except Exception as e:
            logger.error(f"Error running command: {e}")
    
    raise RuntimeError("All ACE-Step commands failed to generate audio")

def generate_speech_with_fallback(prompt: str) -> Path:
    """
    Generate speech with fallback options if ACE-Step fails
    """
    try:
        # First try ACE-Step
        return run_acestep(prompt)
    except Exception as e:
        logger.error(f"ACE-Step failed: {e}")
        logger.info("Attempting to use gTTS as fallback...")
        
        try:
            # Fallback to gTTS if available
            from gtts import gTTS
            output_file = OUTPUT_FILE
            tts = gTTS(text=prompt, lang='en')
            tts.save(str(output_file))
            logger.info(f"Fallback audio generated with gTTS: {output_file}")
            return output_file
        except ImportError:
            logger.error("gTTS not installed. Install with: pip install gtts")
            raise
        except Exception as e:
            logger.error(f"Fallback failed: {e}")
            raise

if __name__ == "__main__":
    prompt = "Salam! Bu bir test audio mesajıdır."
    
    # Check installation
    if not check_acestep_installation():
        logger.warning("ACE-Step not properly installed, will try fallback options")
    
    try:
        # Generate audio
        audio_file = generate_speech_with_fallback(prompt)
        logger.info(f"Successfully generated audio at: {audio_file}")
        
        # Verify file exists and has content
        if audio_file.exists() and audio_file.stat().st_size > 0:
            logger.info("Audio generation completed successfully")
        else:
            logger.error("Generated audio file is empty or missing")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Failed to generate audio: {e}")
        sys.exit(1)
