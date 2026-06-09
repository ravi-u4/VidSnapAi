# This file looks for new folders inside user uploads and converts them to reel if they are not already converted
import os 
from text_to_audio import text_to_speech_file
import time
import subprocess


def text_to_audio(folder):
    print("TTA - ", folder)
    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()
    print(text, folder)
    text_to_speech_file(text, folder)


def create_reel(folder):
    command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
    subprocess.run(command, shell=True, check=True)
    
    print("CR - ", folder)


if __name__ == "__main__":
    # This allows text_to_audio -> config.py to read your hidden ElevenLabs API key.
    from dotenv import load_dotenv
    load_dotenv()

    # Ensure necessary folders/files exist at execution runtime
    os.makedirs("user_uploads", exist_ok=True)
    os.makedirs(os.path.join("static", "reels"), exist_ok=True)
    
    if not os.path.exists("done.txt"):
        with open("done.txt", "w") as f:
            pass # Create empty file safely if it doesn't exist yet

    # Process Queue Loop
    while True:
        print("Processing queue...")
        with open("done.txt", "r") as f:
            done_folders = f.readlines()

        done_folders = [f.strip() for f in done_folders]
        folders = os.listdir("user_uploads") 
        
        for folder in folders:
            # Skip hidden operating system items like .DS_Store
            if folder.startswith('.'):
                continue
                
            if folder not in done_folders: 
                try:
                    text_to_audio(folder) # Generate the audio.mp3 from desc.txt
                    create_reel(folder)   # Convert the images and audio.mp3 inside the folder to a reel
                    
                    with open("done.txt", "a") as f:
                        f.write(folder + "\n")
                except Exception as e:
                    print(f"Error processing folder {folder}: {e}")
                    
        time.sleep(4)