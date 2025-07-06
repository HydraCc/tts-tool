# TTS Engine

This repository contains a modular Text-to-Speech (TTS) engine implemented in Python. The architecture supports plug-and-play TTS models, configurable pipelines, and audio synthesis and saving.

---

## Getting Started

You can run the project either using Docker (recommended for isolation) or locally (for faster iteration and debugging).

**NOTE**: At this stage, only the `engine` is available, but in the future `frontend` and `backend API` services will be implemented. Therefore, below instructions are only for interacting with the engine.

---

## Running with Docker

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Build and start the container (this could take about 5-6 minutes):

   ```bash
   $ docker compose up --build -d
    ```
    If already built before then just:
   ```bash
   $ docker compose up -d
    ```
2. Open a shell in the container:

   ```bash
   $ docker compose exec tts-engine bash
    ```
3. (Optional) Run a simple test:
    ```
    $ python -m engine.examples.coqui_example
    ```

## Running Locally (Python Environment)

### Prerequisites

- Python < 3.12 (due to the limitations of TTS library)
- `pip` and `venv`
### Steps
1. Navigate into `engine/` directory.
    ```bash
    $ cd engine 
    ```
2. Create a virtual environment (using python3.11) distribution:
    ```bash
    $ python3.11 -m venv .venv
    ```
    If this doesnt work then you need to use the official python3.11 executable. In MacOS/Linux, just run `$ which python`.
    ```bash 
    $ /path/to/Python311/python.exe -m venv .venv
    ``` 
3. Activate virtual environment:

    Windows:
    ```bash
    $ ./.venv/Scripts/activate
    ```
    MacOS:
    ```bash
    $ source ./venv/bin/activate
    ```
4. Install dependencies (takes 5-6 mins):
    ```bash
    pip install -r requirements.txt
    pip install -e
    ```
5. Run example script:
    ```bash
    $ python -m engine.examples.coqui_example
    ```
6. Check `sample_data` folder to for the `.wav` output. It should say "hello world"

## Projec Structure
```bash
tts-tool/
├── engine/                  ← Dev folder (Dockerfile, setup, venv)
│   ├── engine/              ← Actual Python package
│   │   ├── models/
│   │   ├── pipelines/
│   │   └── examples/
│   │       └── coqui_example.py
│   ├── requirements.txt
│   ├── setup.py
│   └── Dockerfile
├── docker-compose.yml
└── sample_data/
```