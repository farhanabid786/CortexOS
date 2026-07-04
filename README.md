# CortexOS: Autonomous Multi-Agent Software Engineering Platform

CortexOS is a state-of-the-art visual software blueprinting and engineering platform driven by a sequential 10-agent pipeline. It automatically parses user prompts, analyzes security constraints, models database systems, designs backend API endpoints, establishes frontend layouts, maps QA testing scopes, drafts STRIDE threat reports, compiles setup instructions, and scores architectural quality before packaging final markdown/zip artifacts.

---

## 📂 Project Directory Structure

Below is the layout of the CortexOS codebase, organized by module components:

```text
Capstone Project/
├── backend/                       # FastAPI Backend Application
│   ├── app/
│   │   ├── agents/                # 10-Agent Pipeline Orchestration
│   │   │   ├── base.py            # Base Agent API wrapper & logging
│   │   │   ├── orchestrator.py    # Background pipeline sequencer
│   │   │   ├── requirement_analyst.py # Scans security & parses scope
│   │   │   ├── product_manager.py # Generates objectives & User Stories
│   │   │   ├── software_architect.py # Designs tech stacks & directories
│   │   │   ├── database_engineer.py # Formulates schema & constraints
│   │   │   ├── backend_engineer.py # Configures endpoint specifications
│   │   │   ├── frontend_engineer.py # Defines context & routing tree
│   │   │   ├── qa_engineer.py     # Writes Unit/Integration/E2E test checklists
│   │   │   ├── security_analyst.py # Generates STRIDE models
│   │   │   ├── documentation_agent.py # Builds setup & deployment guides
│   │   │   └── review_agent.py    # Gates blueprint validation (0-100 Score)
│   │   ├── api/                   # REST API Endpoint Routers
│   │   │   ├── audit.py           # System-wide administrative audit logs
│   │   │   ├── auth.py            # OAuth2 JWT login & account setup
│   │   │   ├── blueprints.py      # Retreives compiled JSON & markdown outputs
│   │   │   ├── deps.py            # FastAPI dependency injections
│   │   │   ├── logs.py            # Real-time agent logs for current projects
│   │   │   └── projects.py        # Manages project creation & deletion
│   │   ├── core/                  # Core Systems Configuration
│   │   │   ├── config.py          # App & Env Config loaders
│   │   │   ├── database.py        # SQLAlchemy Async engine setup
│   │   │   └── security.py        # Passwords, JWT keys, prompt injection
│   │   ├── models.py              # SQLAlchemy Database Schema definitions
│   │   ├── schemas.py             # Pydantic validation models
│   │   └── main.py                # FastAPI Application entry point
│   ├── .env                       # Backend local environment keys
│   ├── .env.example               # Backend template configuration
│   ├── requirements.txt           # Python backend dependencies
│   └── Dockerfile                 # Slim-builder multi-stage docker image
├── frontend/                      # Vite + React + TypeScript Frontend
│   ├── src/
│   │   ├── components/            # UI components (visualizer, markdown, logs)
│   │   │   ├── AgentTimeline.tsx  # Interactive step progress tracker
│   │   │   ├── ArchitectureVisualizer.tsx # Tech stack & directories rendering
│   │   │   ├── CodeViewer.tsx     # JSON & data view panel
│   │   │   ├── MarkdownViewer.tsx # Custom markdown renderer
│   │   │   └── Navbar.tsx         # Dashboard header navigation
│   │   ├── context/               # Global state contexts
│   │   │   ├── AuthContext.tsx    # Session & Profile manager
│   │   │   └── ThemeContext.tsx   # Light/Dark display system
│   │   ├── pages/                 # Full Page Views
│   │   │   ├── AuthPage.tsx       # Secure Register/Login screen
│   │   │   ├── BlueprintPage.tsx  # Dynamic multi-agent workspace console
│   │   │   ├── Dashboard.tsx      # Main project panel & metrics
│   │   │   ├── LandingPage.tsx    # Interactive marketing landing page
│   │   │   └── WizardPage.tsx     # Form wizard for launching pipelines
│   │   ├── App.tsx                # Client Routing layout config
│   │   ├── main.tsx               # Client bootstrap index
│   │   └── index.css              # Custom styling definitions
│   ├── package.json               # Node script list & versions
│   ├── tailwind.config.js         # CSS configuration rules
│   ├── tsconfig.json              # TypeScript compilation rules
│   ├── vite.config.ts             # Bundler settings
│   └── Dockerfile                 # Production Nginx host image
├── mcp_server/                    # CortexOS FastMCP Server Integration
│   └── server.py                  # Custom tool handler (file, git, export, shell)
├── docker-compose.yml             # Global orchestration services file
└── README.md                      # Detailed setup guide (this file)
```

---

## 🚀 How to Run the Project

You can run CortexOS using either **Local Development Mode** (lightweight SQLite db) or **Docker Orchestrated Mode** (highly scalable PostgreSQL DB).

---

### Method A: Local Development Mode (Recommended for testing)

#### 1. Setup Backend
1. Open a PowerShell/bash terminal inside the `backend` folder.
2. Create and activate a python virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Verify `backend/.env` exists and contains correct settings. The database file `cortexos.db` will be initialized automatically in SQLite format on startup.
5. Start the FastAPI backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   The backend API is now running at `http://localhost:8000`. Swagger docs are available at `http://localhost:8000/docs`.

---

#### 2. Setup Frontend
1. Open a new terminal inside the `frontend` folder.
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the React/Vite development server:
   ```bash
   npm run dev
   ```
   The frontend UI will be running at `http://localhost:5173` (or `http://localhost:3000`). Open this in your browser to view CortexOS.

---

#### 3. Setup MCP Server (Optional)
CortexOS integrates an Model Context Protocol (MCP) server so external agents can read, run builds, and commit blueprints.
1. Run with Python:
   ```bash
   pip install mcp
   python mcp_server/server.py
   ```

---

### Method B: Docker Orchestrated Mode (Production ready)

This method spins up 3 containers simultaneously: a PostgreSQL database, the FastAPI backend, and an Nginx container hosting the static frontend assets.

1. Make sure Docker and Docker Compose are installed on your machine.
2. Run the following command in the project root directory:
   ```bash
   docker compose up --build
   ```
3. Once running:
   - **Frontend UI:** Open `http://localhost:3000`
   - **Backend API Docs:** Open `http://localhost:8000/docs`
   - **PostgreSQL Database:** Exposed internally inside the docker network (or port `5432` on localhost).

---

## 🔒 Security Scanner Note
The platform scans the prompt for jailbreak patterns and blocks them. To test, enter any software specification prompt longer than 10 characters (e.g., *"Build an inventory manager with Stripe integration"*). Avoid using injection keywords like *"ignore previous instructions"* as these will trigger security logs and be blocked.
