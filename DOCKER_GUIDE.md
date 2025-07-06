# Docker Compose Development Guide

## Overview
This Docker Compose setup provides a focused environment for the TTS Engine with clean environment variable management.

## Current Services
- **tts-engine**: Your TTS engine with all dependencies and dedicated environment configuration

## Future Services (Ready to Add)
- **backend**: API server for the TTS engine
- **frontend**: Web interface for the TTS system

## Getting Started

### 1. Environment Setup
The TTS engine uses a dedicated environment file (`engine.env`) that contains all engine-specific variables:

```bash
# The engine.env file is already configured with sensible defaults
# You can modify it directly without needing to copy from a template

# Optional: Create a .env file for Docker Compose variables (like ports)
cp .env.example .env
```

### 2. Configuration Files
- **`engine.env`**: TTS engine specific environment variables
- **`.env`** (optional): Docker Compose level variables like ports
- **`docker-compose.yml`**: Uses `engine.env` directly via `env_file`

### 2. Build and Start Services
```bash
# Build and start the TTS engine
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 3. Development Workflow

#### Working with the TTS Engine
```bash
# Enter the TTS engine container
docker-compose exec tts-engine bash

# Check environment variables
docker-compose exec tts-engine env | grep TTS

# Run Python scripts inside the container
docker-compose exec tts-engine python examples/coqui_example.py

# Install additional packages
docker-compose exec tts-engine pip install package-name
```

#### Environment Configuration
```bash
# Edit engine-specific settings
# Modify engine.env directly

# Edit Docker Compose level settings (optional)
# Modify .env file

# Restart to apply changes
docker-compose restart tts-engine
```

#### Logs and Debugging
```bash
# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs tts-engine

# Follow logs in real-time
docker-compose logs -f tts-engine
```

### 4. Adding New Services

#### Backend Service
1. Create `backend/` directory with your API code
2. Add `backend/Dockerfile`
3. Uncomment the backend service in `docker-compose.yml`
4. Update ports and environment variables as needed

#### Frontend Service
1. Create `frontend/` directory with your web app
2. Add `frontend/Dockerfile`
3. Uncomment the frontend service in `docker-compose.yml`
4. Configure API endpoints to connect to backend

#### Database Service
1. Uncomment the postgres service in `docker-compose.yml`
2. Create `database/init.sql` if you need initial schema
3. Update connection strings in your backend service

## Commands Reference

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# Stop and remove volumes (careful!)
docker-compose down -v

# Rebuild services
docker-compose build

# View running services
docker-compose ps

# Scale a service (run multiple instances)
docker-compose up --scale tts-engine=2

# Execute commands in running container
docker-compose exec tts-engine python your_script.py

# View resource usage
docker-compose top
```

## Volumes
- `tts-models`: Persistent storage for TTS models (survives container restarts)
- `tts-output`: Persistent storage for generated audio files
- `./engine`: Mounted for live code editing
- `./sample_data`: Shared sample data

## Environment Variables
All TTS engine environment variables are managed in `engine.env`:
- `TTS_ENV`: Environment mode (development/production)
- `TTS_DEVICE`: Device for inference (auto/cpu/cuda/mps)
- `TTS_WORKERS`: Number of worker processes
- `TTS_MODEL_CACHE_DIR`: Model storage location
- `TTS_DEFAULT_MODEL`: Default TTS model to use
- And more...

## Networks
All services communicate through the `tts-network` bridge network.

## Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in `docker-compose.yml` if 8000, 8001, 3000 are in use
2. **Permission issues**: Ensure Docker has access to your project directory
3. **Build failures**: Check Dockerfile syntax and requirements.txt

### Reset Everything
```bash
# Stop all containers and remove volumes
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Clean rebuild
docker-compose build --no-cache
docker-compose up
```

## Build Optimization

### .dockerignore Files
The project includes optimized `.dockerignore` files to ensure fast and secure builds:

- **`engine/.dockerignore`**: Excludes development files, dependencies, models, and outputs from the engine build
- **`.dockerignore`**: Root-level exclusions for the entire project

### What's Excluded from Docker Builds:
- Virtual environments (`.venv/`, `venv/`)
- Development tools and IDEs (`.vscode/`, `.idea/`)
- Git repository (`.git/`)
- Documentation files (`*.md`)
- Test files and coverage reports
- Environment configuration files (handled separately)
- Model files and outputs (handled by Docker volumes)
- Python cache and build artifacts

### Build Benefits:
- **Faster builds**: Smaller build context
- **Better security**: No sensitive files in image layers
- **Consistent images**: Only production code included
- **Better caching**: Docker layer caching works optimally
