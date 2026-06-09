# SnapVidAI (vidsnapai)

An automated web application designed to convert sequential image uploads and descriptions into high-quality short video reels using Flask, ElevenLabs text-to-speech, and FFmpeg.

## Architecture Overview

To prevent video rendering tasks from freezing the web server, this application uses a split-process architecture:
1. **Frontend Server (`main.py`)**: A lightweight Flask interface that collects user files, structures target directories, and logs pending requests into a queue.
2. **Background Processor (`generate_process.py`)**: A persistent asynchronous background worker that dynamically polls for new content, calls ElevenLabs to generate natural voiceovers, and compiles final videos using FFmpeg.

---

## Prerequisites

Before setting up the project, ensure your local development environment has the following system dependencies installed:

* **Python 3.8+**
* **FFmpeg**: Must be globally installed on your operating system and added to your system's path variables (`PATH`) so it can be called seamlessly via command line processes.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone [https://github.com/ravi-u4/vidsnapai.git](https://github.com/ravi-u4/vidsnapai.git)
cd vidsnapai
2. Install Python Dependencies
It is recommended to use a virtual environment before installing packages. Install all mandatory frameworks via the dependencies manifest:

Bash
pip install -r requirements.txt
3. Configure Environment Credentials
Do not push private keys to production versions. Copy your unique API access profile by creating a file named .env in the root folder of the project:

Code snippet
ELEVENLABS_API_KEY=your_secret_elevenlabs_api_key_here
Running the Application
Because the project relies on parallel queue processing, you will need to open two separate terminal windows to run the complete environment stack.

Process 1: Launch the Flask Web Interface
In your first terminal window, start the user-facing server:

Bash
python snapvidai/main.py
Once running, navigate to http://127.0.0.1:5000 in your preferred web browser to access the frontend dashboard.

Process 2: Launch the Video Rendering Queue
In your second terminal window, initiate the background worker script:

Bash
python snapvidai/generate_process.py
The worker will actively monitor incoming assets every 4 seconds, compile matching localized voiceovers, and output the final video segments.

Project Structure & Data Handling
Plaintext
snapvidai/
│
├── snapvidai/
│   ├── static/
│   │   └── reels/               # Auto-generated: Stores final rendered MP4 files
│   ├── templates/               # UI HTML layouts
│   ├── config.py                # Environment management script
│   ├── main.py                  # Primary Flask application routing entry point
│   ├── generate_process.py      # Background worker and rendering script
│   └── text_to_audio.py         # ElevenLabs audio generator utility
│
├── .env                         # Hidden: Local secret credentials configuration (IGNORED BY GIT)
├── .gitignore                   # Local file tracking rules for deployment security
└── requirements.txt             # Registered project dependency versions

Note: Folder hierarchies such as user_uploads/ and static/reels/ are automatically validated and constructed upon program startup if they are missing from a clean environment.