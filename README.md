# atletIQ

An AI-powered personal training platform that leverages wearable device data (Garmin, Apple Watch) to create personalized fitness plans and provide intelligent coaching through conversational AI.

## Overview

atletIQ combines conversational AI with fitness tracking data to deliver personalized training guidance. The platform features a sophisticated multi-stage onboarding process that collects user profiles, integrates wearable data, and provides ongoing coaching through an intelligent agent system.

## Project Structure

```
atletIQ/
├── frontend/          # Next.js 15 landing page and integrations
├── backend/           # FastAPI backend with AI agent system
├── agents/            # Claude agent configurations
└── setup.cfg          # Project configuration
```

## Core Technology Stack

### Frontend
- **Next.js 15.5.6** - React framework with App Router
- **React 19.1.0** - UI library
- **TypeScript 5** - Type safety
- **Tailwind CSS 4** - Utility-first styling
- **shadcn/ui** - Reusable component library
- **Magic UI** - Advanced animations and effects
- **Motion (12.23.24)** - Animation library
- **Lucide React** - Icon system

### Backend
- **FastAPI** - Modern async Python web framework
- **Python 3.13+** - Core language
- **SQLAlchemy 2.0** - ORM and database toolkit
- **Alembic** - Database migrations
- **PostgreSQL 16** - Primary database
- **Redis 7** - Caching and message broker
- **Celery** - Distributed task queue
- **Anthropic Claude** - AI agent engine (claude-agent-sdk 0.1.4)
- **ElevenLabs** - Voice synthesis and transcription
- **Pydantic** - Data validation and settings
- **Uvicorn** - ASGI server

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **uv** - Fast Python package manager
- **Flower** - Celery monitoring
- **Sentry** - Error tracking and observability

## Core Implementation

### AI Agent System

The backend implements a sophisticated multi-agent system powered by Claude:

1. **Core Agent** (`backend/app/agent/engines/core_agent.py`)
   - Main conversational AI for fitness coaching
   - Supports MCP (Model Context Protocol) server configuration
   - Dynamic tool integration
   - Conversation history management

2. **Extractor Agent**
   - Extracts structured user profile data from conversational input
   - Processes demographics, fitness history, goals, and lifestyle factors

3. **Training & Fitness Index Agent**
   - Analyzes user profiles and wearable data
   - Generates personalized fitness assessments
   - Creates training recommendations

### Multi-Stage Conversation Flow

The chat service (`backend/app/services/chat.py`) implements a stateful conversation system:

1. **Onboarding** - Initial greeting and introduction
2. **Profile Extraction** - Collects user information through conversation
3. **Wearable Integration** - Connects Garmin/Apple Watch data
4. **Profile Analysis** - Generates fitness assessment
5. **Ongoing Coaching** - Personalized training guidance

### API Architecture

**Endpoints** (`backend/app/api/v1/`):
- `/api/v1/agent/query` - Chat with AI agent
- `/api/v1/telegram/webhook` - Telegram bot integration (text + voice)

### Database Models

Located in `backend/app/models/`:
- **ChatSession** - User conversation sessions
- **Conversation** - Message containers
- **Message** - Individual chat messages with roles

### Frontend Features

**Landing Page** (`frontend/components/landing-page.tsx`):
- Immersive video background with particle effects
- Responsive design with Magic UI animations
- Multi-platform messaging integration (Telegram, WhatsApp, etc.)
- Device authorization flow

**Integration Pages**:
- `frontend/app/integrations/success/` - Wearable authorization success
- `frontend/app/integrations/apple-health/` - Apple Health integration

## Getting Started

### Prerequisites

**Backend:**
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- Docker and Docker Compose
- PostgreSQL 16 (via Docker)
- Redis 7 (via Docker)

**Frontend:**
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/atletIQ.git
   cd atletIQ/backend
   ```

2. **Configure environment variables**

   Create `backend/config/.env` with required settings:
   ```bash
   # API Configuration
   PROJECT_NAME=atletIQ
   API_V1_STR=/api/v1
   DEBUG=True
   ENVIRONMENT=LOCAL

   # Database
   DATABASE_URL=postgresql+asyncpg://atlet-iq:atlet-iq@postgres:5432/atlet-iq

   # Claude Agent
   ANTHROPIC_API_KEY=your_anthropic_api_key
   CLAUDE_AGENT_ENABLE_STREAMING=False
   CLAUDE_AGENT_MODEL=claude-3-5-sonnet-20241022

   # ElevenLabs (for voice features)
   ELEVENLABS_API_KEY=your_elevenlabs_api_key

   # Telegram Bot (optional)
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_BOT_USERNAME=your_bot_username

   # Redis
   REDIS_URL=redis://redis:6379/0

   # MCP Servers (optional)
   CLAUDE_AGENT_MCP_SERVERS={}
   ```

3. **Build and run with Docker**
   ```bash
   make build
   make run
   ```

   This starts:
   - **API Server** - http://localhost:8000
   - **PostgreSQL** - localhost:5433
   - **Redis** - Internal network
   - **Celery Worker** - Background tasks
   - **Celery Beat** - Scheduled tasks
   - **Flower** - http://localhost:5555 (Celery monitoring)

4. **Run migrations**
   ```bash
   make migrate
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Flower dashboard: http://localhost:5555

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**

   Create `frontend/.env.local`:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

5. **Access the application**

   Open http://localhost:3000

### Alternative Backend Setup (Without Docker)

1. **Install dependencies with uv**
   ```bash
   cd backend
   uv sync
   ```

2. **Set up local PostgreSQL and Redis**

   Update `.env` with local connection strings

3. **Run migrations**
   ```bash
   uv run alembic upgrade head
   ```

4. **Start the API server**
   ```bash
   uv run fastapi dev app/main.py --port 8000
   ```

5. **Start Celery worker (separate terminal)**
   ```bash
   uv run celery -A app.core.celery worker -l info
   ```

6. **Start Celery beat (separate terminal)**
   ```bash
   uv run celery -A app.core.celery beat -l info
   ```

## Development Commands

### Backend (Makefile)

```bash
make help              # Show all available commands
make build             # Build Docker images
make run               # Run environment in detached mode
make up                # Run environment (attached)
make stop              # Stop running containers
make down              # Kill and remove containers
make migrate           # Apply database migrations
make create_migration  # Create new migration: make create_migration m="Description"
make downgrade         # Revert last migration
```

### Frontend

```bash
npm run dev            # Start development server
npm run build          # Build for production
npm run start          # Start production server
npm run lint           # Run ESLint
```

## Key Features

### AI-Powered Coaching
- Conversational AI using Claude Sonnet 4.5
- Context-aware responses with conversation history
- Multi-agent system for specialized tasks
- MCP server integration for enhanced capabilities

### Wearable Integration
- Garmin device support
- Apple Watch/Health integration
- Automated data synchronization
- Real-time fitness metrics

### Telegram Bot
- Text and voice message support
- Voice transcription with ElevenLabs
- Text-to-speech responses
- Asynchronous message processing

### Personalized Training
- Profile-based recommendations
- Fitness level assessment
- Goal-oriented planning
- Progress tracking

### Scalable Architecture
- Async/await throughout
- Celery task queue for background jobs
- Redis caching and message broker
- PostgreSQL for reliable data storage
- Docker containerization

## Database Migrations

Create a new migration after model changes:
```bash
cd backend
make create_migration m="Add user profile fields"
```

Apply migrations:
```bash
make migrate
```

Revert last migration:
```bash
make downgrade
```

## MCP Server Configuration

The backend supports Model Context Protocol (MCP) servers for enhanced agent capabilities. Configure via environment variables:

```bash
# Example MCP configuration
CLAUDE_AGENT_MCP_SERVERS='{"weather_api": {"type": "http", "url": "https://api.example.com/mcp", "headers": {"Authorization": "Bearer token"}}}'
```

Or programmatically:
```python
from app.agent.engines.core_agent import ClaudeAgent, create_mcp_http_server_config

agent = ClaudeAgent()
agent.add_mcp_server(
    "my_service",
    create_mcp_http_server_config(
        name="my_service",
        url="https://api.myservice.com/mcp",
        headers={"Authorization": "Bearer token"}
    )
)
```

## Project Configuration

### Backend Code Quality

The project uses strict Python linting (configured in `pyproject.toml`):
- **Ruff** - Fast Python linter with isort, pyflakes, and more
- **Type checking** - Strict type hints enforced
- **Line length** - 100 characters
- **Pre-commit hooks** - Automated checks before commits

### Frontend Configuration

- **TypeScript** - Strict mode enabled
- **ESLint** - Next.js recommended configuration
- **Tailwind CSS 4** - Latest version with PostCSS

## Architecture Highlights

### Backend Design Patterns
- **Dependency Injection** - FastAPI's Depends system
- **Repository Pattern** - CRUD operations in `backend/app/crud/`
- **Service Layer** - Business logic in `backend/app/services/`
- **Schema Validation** - Pydantic models in `backend/app/schemas/`
- **Exception Handling** - Centralized error handling
- **CORS Middleware** - Configured for cross-origin requests

### Agent System Features
- **Conversation History** - Automatic message persistence
- **Session Management** - UUID-based session tracking with external ID mapping
- **State Management** - In-memory session state for onboarding flow
- **Error Recovery** - Graceful fallbacks for agent errors
- **Streaming Support** - Optional response streaming

### Frontend Architecture
- **App Router** - Next.js 15 file-based routing
- **Server Components** - Default to SSR for performance
- **Client Components** - Interactive UI with 'use client'
- **Component Library** - Reusable UI components with shadcn/ui
- **Animation System** - Motion and Magic UI for smooth transitions

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Monitoring & Debugging

- **Flower**: http://localhost:5555 - Celery task monitoring
- **Logs**: Docker logs via `docker compose logs -f`
- **Debug Endpoints**: Mounted in DEBUG mode (see `backend/app/healthcheck/debug.py`)
- **Sentry**: Configured for non-local environments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run linting: `cd backend && uv run ruff check .`
5. Run tests: `make test`
6. Submit a pull request

## License

MIT

## Acknowledgments

- **Anthropic Claude** - AI agent capabilities
- **ElevenLabs** - Voice AI technology
- **shadcn/ui** - Beautiful UI components
- **Magic UI** - Advanced animations
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework
