
# SeeForMe — AI Shopping Assistant

**Shop with greater confidence and independence.**

SeeForMe is a voice-first AI shopping assistant designed to help blind and low-vision users identify products and understand visible packaging information through spoken guidance.

## Problem Statement

Identifying products and reading packaging can be challenging for people with visual impairments. SeeForMe aims to make this experience more accessible through AI-powered image analysis and voice interaction.

## Key Features

- **AI-powered product identification:** Uses Gemma 4 to analyse uploaded product photographs.
- **Voice assistant:** Supports spoken commands for help, product scanning, and reading results aloud.
- **Accessible interface:** Includes keyboard-operable controls, visible focus indicators, and screen-reader labels.
- **Product information extraction:** Attempts to identify visible brand names, product details, sizes, prices, and caution information.
- **Spoken results:** Reads the generated product analysis aloud, with formatting symbols removed from speech.
- **Photo upload:** Provides an alternative when camera access is unavailable.
- **Error handling:** Provides guidance when an image cannot be analysed successfully.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| AI model | Gemma 4 |
| AI integration | Google Gen AI SDK |
| Image processing | Pillow |
| Frontend | HTML, CSS, JavaScript |
| Voice input | Browser Speech Recognition API |
| Speech output | Web Speech Synthesis API |

## How It Works

1. The user selects a product photograph.
2. The photograph is submitted to the FastAPI backend.
3. The backend sends the image and instructions to Gemma 4.
4. The model returns a description of the visible product information.
5. SeeForMe displays the result and can read it aloud.

## Setup Instructions

### Requirements

- Python 3.10 or newer
- A Google AI API key with access to the configured model
- An internet connection
- A supported browser for voice features

### 1. Clone the repository

```bash
git clone https://github.com/shirin-21-7/SeeForMe-Hackathon.git
cd SeeForMe-Hackathon
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project directory and add your own API key:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual key. Never publish your API key or commit the `.env` file.

### 5. Run the application

```bash
python -m uvicorn main:app --reload --port 8002
```

Open the following address in your browser:

http://127.0.0.1:8002

## Example Voice Commands

- “Help”
- “Choose a photo”
- “Open camera”
- “Scan this”
- “Read that again”
- “Stop speaking”

Voice recognition availability depends on browser support, microphone permissions, and connectivity.

## Accessibility Goals

SeeForMe is designed around voice-first interaction, keyboard navigation, clear control labels, spoken feedback, and alternative photo upload.

Further testing with blind and low-vision users is needed to validate usability and accessibility in real-world shopping situations.

## Important Limitations

- AI-generated product information may be incomplete or incorrect.
- Unreadable text may not be extracted accurately.
- Camera access depends on the user's device and browser.
- Product ingredients, prices, expiry dates, and safety information must be verified against the actual packaging.
- SeeForMe is a prototype and should not replace independent verification of important product details.

## Project

**SeeForMe — Making product information more accessible through AI and voice interaction.**
