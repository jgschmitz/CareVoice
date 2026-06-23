# 🩺 CareVoice AI

A healthcare-focused voice assistant that combines speech recognition, AI reasoning, optional text-to-speech, and persistent conversational memory powered by MongoDB Atlas.

---

## Overview

CareVoice AI demonstrates how healthcare organizations can leverage voice interfaces and AI to create more natural member experiences.

Users speak naturally into a microphone, Whisper transcribes the conversation, OpenAI generates a contextual response, and MongoDB Atlas stores conversational state for continuity across interactions.

The goal is not simply voice interaction it is the creation of a persistent healthcare memory layer that enables personalized experiences over time. If your phone is connected to your laptop you will have the option to use that as the mic also! 

---

## Architecture

```text
🎙️ Voice Input
        ↓
🎙️ Whisper Transcription
        ↓
🧠 OpenAI Reasoning
        ↓
📚 MongoDB Atlas Conversation State
        ↓
🏥 Personalized Member Experience
        ↓
🔊 Optional Text-to-Speech
```

---

## Key Features

- Real-time voice capture
- Faster-Whisper speech-to-text transcription
- OpenAI-powered conversational responses
- MongoDB Atlas conversation persistence
- Session-based interaction history
- Optional text-to-speech playback
- Streamlit healthcare-themed UI

---

## Why It Matters

Healthcare organizations have traditionally relied on portals, forms, and call centers.

Voice AI enables a different model:

- Members speak naturally
- AI understands intent
- Context persists across interactions
- Experiences become increasingly personalized

This prototype demonstrates how voice, AI, and persistent memory can work together to improve member engagement and navigation.

---

## Technology Stack

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| Speech Recognition | Faster-Whisper |
| AI Model | OpenAI GPT |
| Conversational Memory | MongoDB Atlas |
| Audio Processing | SoundFile |
| Text-to-Speech | Edge TTS |
| Language | Python |

---

## Installation

### Install Dependencies

```bash
pip install streamlit
pip install audio-recorder-streamlit
pip install faster-whisper
pip install soundfile
pip install openai==0.28.*
pip install edge-tts
pip install pymongo
```

Or:

```bash
pip install streamlit audio-recorder-streamlit faster-whisper soundfile openai==0.28.* edge-tts pymongo
```

---

## Configuration

### OpenAI

```python
OPENAI_API_KEY = "YOUR_API_KEY"
openai.api_key = OPENAI_API_KEY
```

### MongoDB Atlas

```python
from pymongo import MongoClient

client = MongoClient("YOUR_MONGODB_ATLAS_URI")
db = client.carevoice
conversations = db.conversations
```

---

## Running the Application

```bash
python3 -m streamlit run app.py --server.fileWatcherType=poll
```

---

## Example Workflow

1. User clicks Record
2. User speaks naturally
3. Whisper transcribes audio
4. Transcript is sent to OpenAI
5. AI generates a contextual response
6. Conversation state is stored in MongoDB Atlas
7. Response is displayed and optionally spoken back to the user

---

## Future Enhancements

- Retrieval-Augmented Generation (RAG)
- Clinical knowledge base integration
- Provider directory search
- Benefits navigation
- Care management workflows
- FHIR integration
- Longitudinal member memory
- Multi-modal healthcare interactions

---

## Demo Vision

```text
🗣️ Members speak naturally
🎙️ Whisper transcribes conversations
🧠 AI understands intent
📚 MongoDB Atlas maintains longitudinal context
🏥 Personalized healthcare experiences
```

---

## Business Value

This prototype demonstrates a simple but important concept:

- Members speak naturally
- AI understands intent
- MongoDB Atlas maintains longitudinal context
- Healthcare organizations deliver more personalized experiences

The opportunity isn't voice alone—it's combining voice, AI, and persistent context to create a healthcare memory layer that improves every interaction over time.
