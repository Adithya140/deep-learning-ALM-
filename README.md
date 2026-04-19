# NEURAL_LINK 🧬

A high-performance multimodal interface that bridges the gap between human speech, live visual data, and the Gemini 2.5 Flash model. 

## 🚀 Overview

**NEURAL_LINK** provides a seamless "eyes and ears" interface for generative AI. It uses real-time microphone recording combined with automatic camera frame capture to provide a fully context-aware conversational experience.

### Key Features

- **Unified Multimodal Input**: Stopping a voice recording automatically triggers a camera capture, sending both to Gemini.
- **Dynamic Context**: Maintains session history, allowing for fluid conversations about the visual environment.
- **Experimental Cyber-UI**: A premium, cyberpunk-inspired interface with live waveform visualization and a data log terminal.
- **Gemini 2.5 Flash Powered**: Leverages the speed and multimodal capabilities of the latest Gemini 2.5 models.
- **Privacy Focused**: Captured frames are treated as temporary localized data and handled efficiently.

---

## 🛠 Installation & Setup

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended)
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/fardeenKhadri/speech.git
   cd speech
   ```

2. **Setup Environment**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Install Dependencies**
   ```bash
   uv sync
   ```

4. **Run the Application**
   ```bash
   uv run main.py
   ```
   Access the interface at `http://127.0.0.1:5000`.

---

## 🎮 Interface Guide

- **ANALYZE_FEED**: Establish a neural link via a single visual capture.
- **INIT_RECORDING**:
   - **Click 1**: Start speaking.
   - **Click 2**: Stop recording. 
   - *Result*: The system automatically captures a frame from your camera and sends it with your speech to Gemini.
- **Sample Queries**:
   - *"What do you see on the screen?"*
   - *"Describe the object I am holding."*
   - *"Identify the colors in front of me."*

---

