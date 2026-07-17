# Unitree Go2 Intelligent Middleware

An offline AI middleware for the **Unitree Go2 X ("Asty")** robot dog, providing natural language interaction, speech synthesis, structured task planning, and robot motion control through a modular architecture.

The project combines **Natural Language Processing (NLP)**, **Large Language Models (LLMs)**, **speech technologies**, and the **Unitree WebRTC Connect SDK** to create an intelligent human–robot interaction system capable of understanding spoken instructions and executing robot behaviours safely and efficiently.

---

## Overview

This project forms part of the development of an intelligent middleware layer for the Unitree Go2 X robot.

Instead of tightly coupling AI models with robot hardware, the system separates:

- AI reasoning
- Robot control
- User interface

into independent modules that communicate using structured data.

This architecture makes the system easier to maintain, test, extend and deploy.

---

# Features

- 🎤 Offline speech recognition (Whisper)
- 🧠 Local Large Language Model reasoning (Gemma 3 via Ollama)
- 📋 Structured JSON task planning
- 🗣 Offline speech synthesis (Piper)
- 🤖 Motion control using the Unitree WebRTC Connect SDK
- 🔊 Robot speech playback over WebRTC
- 💬 PySide6 desktop interface
- ⚙ Modular AI and Robot services
- 🔄 Background processing using Qt worker threads
- 🌐 Fully offline execution

---

# System Architecture

```
                    ┌─────────────────────────────┐
                    │        PySide6 GUI          │
                    │                             │
                    │ Chat • Microphone • Status  │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │     Assistant Worker        │
                    │     (Background Thread)     │
                    └──────────────┬──────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
    Whisper STT              Ollama (Gemma 3)          Piper TTS
 Speech Recognition       Planning & Reasoning      Speech Synthesis
          │                        │                        │
          └────────────────────────┴────────────────────────┘
                                   │
                                   ▼
                     Shared Communication Layer
                     ├── shared/audio/echo.wav
                     └── shared/action.json
                                   │
                      ┌────────────┴────────────┐
                      ▼                         ▼
               Robot Audio Service      Action Controller
                  (WebRTC)             (Motion Commands)
                      │                         │
                      └────────────┬────────────┘
                                   ▼
                           Unitree Go2 X
```

---

# Design Philosophy

The middleware follows a **loosely coupled architecture**.

Rather than allowing AI models to directly control robot hardware, the AI subsystem generates structured outputs that are consumed by an independent Robot Service.

The AI only produces:

- `echo.wav`
- `action.json`

The Robot Service monitors these outputs and executes them independently.

Advantages include:

- Loose coupling
- Improved robustness
- Easier debugging
- Safer hardware interaction
- Independent component development
- Simplified testing

---

# AI Pipeline

```
User Speech
      │
      ▼
 Whisper
      │
Speech → Text
      │
      ▼
 Robot Planner
      │
 Structured JSON
      │
      ▼
 Piper
      │
 Speech Audio
      │
      ▼
 echo.wav
```

Example planner output:

```json
{
    "speech": "Alright, I'll stand up.",
    "confidence": 0.99,
    "actions": [
        {
            "action": "stand"
        }
    ]
}
```

The planner never controls the robot directly.

Its sole responsibility is converting natural language into structured execution plans.

---

# Robot Pipeline

The Robot Service operates independently from the AI.

Audio pipeline:

```
Watch shared/audio/

↓

Play speech through WebRTC

↓

Delete audio file
```

Motion pipeline:

```
Watch action.json

↓

Parse JSON

↓

Execute actions

↓

Delete file
```

This separation ensures that failures in one subsystem do not directly affect the other.

---

# Why Structured JSON?

Natural language is ambiguous. Instead of executing raw text, the LLM generates deterministic structured output.

Example:

```json
{
    "speech":"I'll move backwards then jump.",
    "confidence":0.98,
    "actions":[
        {
            "action":"backward",
            "distance":2
        },
        {
            "action":"jump"
        }
    ]
}
```

Benefits:

- Deterministic execution
- Confidence scoring
- Multi-step task planning
- Easy validation
- Extensible command format

---

# Technologies

| Component | Technology |
|------------|------------|
| GUI | PySide6 |
| Speech Recognition | OpenAI Whisper |
| Large Language Model | Ollama (Gemma 3) |
| Speech Synthesis | Piper |
| Robot Communication | **Unitree WebRTC Connect SDK** |
| Programming Language | Python |

---

# Unitree WebRTC Connect SDK

Robot communication is built on top of the **Unitree WebRTC Connect SDK**.

The SDK provides:

- WebRTC communication
- Robot motion commands
- Audio streaming
- Real-time control
- Access to robot APIs

Rather than implementing low-level communication protocols, this project extends the SDK with an AI middleware responsible for natural language understanding and high-level task planning.

---

# Why Local AI?

All AI models execute locally.

Advantages include:

- Offline operation
- No API costs
- Lower latency
- Improved privacy
- Suitable for field robotics

No cloud services are required during normal operation.

---

# Desktop Interface

The operator console is implemented using **PySide6**.

Current functionality includes:

- Chat interface
- Voice interaction
- Planner confidence
- Planned robot actions
- System status

Future work includes:

- Live camera feed
- Robot telemetry
- Battery monitoring
- Wi-Fi status
- LiDAR visualisation
- Mapping
- Navigation

---

# Threading Model

The graphical interface remains responsive by performing AI processing inside a dedicated worker thread.

```
GUI Thread

↓

Signals

↓

Assistant Worker

↓

Whisper

↓

Ollama

↓

Piper

↓

Signals

↓

GUI Updates
```

---

# Project Structure

```
go2-intelligent-middleware/

│
├── ai/
│   ├── whisper_service.py
│   ├── robot_planner.py
│   ├── llm.py
│   ├── tts.py
│   └── echo_service.py
│
├── robot/
│   ├── robot_connection.py
│   ├── action_controller.py
│   ├── speaker.py
│   └── main.py
│
├── gui/
│   ├── app.py
│   ├── worker.py
│   ├── main_window.py
│   ├── chat_widget.py
│   └── status_panel.py
│
└── shared/
    ├── audio/
    └── action.json
```

---

# Supported Robot Actions

The middleware currently supports:

- Stand
- Sit
- Forward
- Backward
- Left
- Right
- Rotate Left
- Rotate Right
- Jump
- Jump Forward
- Stretch
- Dance
- Hello
- Finger Heart
- Stop

Multiple actions can be chained naturally.

Example:

> "Move backwards, rotate left and then sit down."

---

# Installation

1. Clone the repository

```bash
git clone https://github.com/fredcodess/unitree-go2-intelligent-middleware.git
cd unitree-go2-intelligent-middleware
```

---

## 2. Create a Python environment (recommended)

```bash
python -m venv .venv
```

Activate the environment.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```
---

## 3. Install the project dependencies

```bash
pip install -r requirements.txt
```
---

## 4. Install and start Ollama

Install Ollama from:

https://ollama.com

Pull the required language model:

```bash
ollama pull gemma3
```

Start the Ollama server:

```bash
ollama serve
```
Leave this terminal running.
---

# Running the Project

The application requires **two terminals**.

## Terminal 1 — Ollama

Start the local LLM server:

```bash
ollama serve
```
---

## Terminal 2 — Voice Assistant

Activate the Python environment (if necessary):

```bash
source .venv/bin/activate
```

Run the application:

```bash
python run.py
```

The application will automatically:

1. Launch the PySide6 desktop interface.
2. Start the AI service.
3. Start the Robot Service.
4. Connect to the Unitree Go2 X via the Unitree WebRTC Connect SDK.
5. Wait for voice commands.
---

# Current Status

## ✅ Completed

- Offline speech recognition
- Local LLM reasoning
- Structured JSON planner
- Offline speech synthesis
- Robot speech playback
- Robot motion execution
- PySide6 operator console
- Modular middleware architecture
- Unitree WebRTC integration
---

# Research Focus

This middleware explores the integration of:

- Natural Language Processing
- Human–Robot Interaction
- Large Language Models
- Structured Task Planning
- Real-Time Robotics
- Offline AI Systems

The objective is to provide an extensible foundation for intelligent robot assistants while maintaining a modular architecture suitable for future research and development.
---

# Acknowledgements

This work was developed as part of the internship:

**Development of Middlewares for a Unitree Go2 X Robot Dog**

School of Engineering and Physical Sciences  
**Aston University**  
2026

Supervised by **Dr. Zhuangzhuang Dai**

The project builds upon the **Unitree WebRTC Connect SDK**, extending it with an AI middleware layer for natural language interaction and intelligent task planning.
---

## Future Vision

This voice assistant represents one component of a broader middleware platform being developed for **Asty**, a Unitree Go2 X robot dog.

The long-term vision is to integrate:

- SLAM
- LiDAR-based navigation
- ROS 2 (DDS) interoperability
- Vision-language models
- Autonomous task planning
- Multi-modal perception

into a unified intelligent robotics framework capable of natural interaction and autonomous operation.
