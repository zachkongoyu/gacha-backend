# Gacha Backend

Multi-service backend for a gacha game system built with FastAPI, PostgreSQL, Redis, and OAuth authentication.

## Architecture

This project follows a microservices architecture with the following services:

- **Auth Service** (`/services/auth`): OAuth authentication, JWT token issuance
- **Gacha Service** (`/services/gacha`): Gacha pull mechanics with pity system
- **Inventory Service** (`/services/inventory`): User inventory management
- **AI Service** (`/services/ai`): AI content generation job management
- **Asset Service** (`/services/asset`): CDN and asset URL management

### Shared Libraries

- **shared/settings.py**: Centralized configuration using pydantic-settings
- **shared/database.py**: Async PostgreSQL connection pooling with asyncpg
- **shared/auth.py**: JWT token creation and validation utilities

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for local development)
- pip or uv for package management

## Local Development Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd gacha-backend
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and configure:
- Database credentials
- Redis URL
- JWT secret key (change the default!)
- OAuth provider credentials (Google, GitHub, etc.)

### 3. Start PostgreSQL and Redis

```bash
docker compose up -d
```

This starts:
- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`

### 4. Install Python dependencies

```bash
pip install -e .
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

### 5. Run a service

Each service can be run independently:

```bash
# Auth service (port 8001)
uvicorn services.auth.main:app --reload --port 8001

# Gacha service (port 8002)
uvicorn services.gacha.main:app --reload --port 8002

# Inventory service (port 8003)
uvicorn services.inventory.main:app --reload --port 8003

# AI service (port 8004)
uvicorn services.ai.main:app --reload --port 8004

# Asset service (port 8005)
uvicorn services.asset.main:app --reload --port 8005
```

### 6. Access the API documentation

Each service exposes interactive API docs:

- Auth: http://localhost:8001/docs
- Gacha: http://localhost:8002/docs
- Inventory: http://localhost:8003/docs
- AI: http://localhost:8004/docs
- Asset: http://localhost:8005/docs

## API Endpoints

### Auth Service

- `GET /auth/login` - Initiate OAuth login flow
- `GET /auth/callback` - OAuth callback handler (exchanges code for JWT)
- `POST /auth/verify` - Verify JWT token

### Gacha Service

- `POST /pull?count=1` - Perform gacha pull(s) (1 or 10)
- `GET /rates` - Get gacha rates and pity information
- `GET /banner` - Get current banner details

### Inventory Service

- `GET /inventory` - List user's inventory items
- `GET /inventory/{item_id}` - Get item details
- `POST /inventory/{item_id}/enhance` - Enhance/level up item

### AI Service

- `POST /jobs` - Create AI generation job
- `GET /jobs/{job_id}` - Get job status and results
- `GET /jobs` - List user's jobs
- `GET /models` - List available AI models

### Asset Service

- `GET /assets/{asset_id}` - Get asset URLs
- `GET /assets` - List available assets
- `POST /assets/upload` - Get upload URL for new asset
- `GET /assets/{asset_id}/versions` - List asset versions
- `DELETE /assets/{asset_id}` - Delete asset

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8002/pull?count=1
```

## Vercel Deployment

The project is configured for deployment on Vercel with serverless functions.

### Configuration

The `vercel.json` file configures:
- Python runtime for each service
- Route mapping from `/service/...` to `/api/service.py`

### Environment Variables

Configure these in your Vercel project settings:

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET_KEY` - Secret key for JWT signing
- `OAUTH_CLIENT_ID` - OAuth client ID
- `OAUTH_CLIENT_SECRET` - OAuth client secret
- `OAUTH_AUTHORIZE_URL` - OAuth authorization endpoint
- `OAUTH_TOKEN_URL` - OAuth token endpoint
- `OAUTH_USERINFO_URL` - OAuth userinfo endpoint
- `OAUTH_REDIRECT_URI` - OAuth callback URL

### Deploy

```bash
vercel
```

Or connect your GitHub repository to Vercel for automatic deployments.

## Development

### Code Formatting

```bash
black .
```

### Linting

```bash
ruff check .
```

### Project Structure

```
gacha-backend/
├── api/                    # Vercel serverless function entrypoints
│   ├── auth.py
│   ├── gacha.py
│   ├── inventory.py
│   ├── ai.py
│   └── asset.py
├── services/               # Microservices
│   ├── auth/
│   │   └── main.py
│   ├── gacha/
│   │   └── main.py
│   ├── inventory/
│   │   └── main.py
│   ├── ai/
│   │   └── main.py
│   └── asset/
│       └── main.py
├── shared/                 # Shared utilities
│   ├── settings.py
│   ├── database.py
│   └── auth.py
├── .env.example           # Environment template
├── docker-compose.yml     # Local dev services
├── pyproject.toml         # Project configuration
├── vercel.json           # Vercel deployment config
└── README.md
```

## Notes

- This is a stub implementation with placeholder responses
- Database schema migrations are not included (add Alembic for production)
- OAuth configuration requires setting up a provider (Google, GitHub, etc.)
- Redis is configured but not yet utilized (ready for caching/sessions)
- All sensitive configuration should be in environment variables, never committed

## License

[Add your license here]
