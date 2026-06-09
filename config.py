import os
from dotenv import load_data, load_dotenv

# Load variables from the .env file
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")