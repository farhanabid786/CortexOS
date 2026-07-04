# CortexOS: Autonomous Multi-Agent Software Engineering Platform

CortexOS is a state-of-the-art visual software blueprinting and engineering platform driven by a sequential 10-agent AI pipeline. It automatically analyzes software requirements, designs architectures, generates backend and frontend blueprints, creates database schemas, performs security analysis, produces testing strategies, and compiles complete project documentation.

---

# 🌐 Live Demo

### Frontend (Vercel)

https://cortex-os-umber.vercel.app/

### Backend API (Render)

https://cortexos-backend-p8li.onrender.com/

### Swagger API Documentation

https://cortexos-backend-p8li.onrender.com/docs

---

# 🚀 Features

- 🔐 JWT Authentication
- 🤖 10-Agent AI Pipeline
- 📋 Project Management
- 🏗 Software Architecture Generation
- 🗄 Database Schema Design
- ⚙ Backend API Blueprint Generation
- 🎨 Frontend UI Blueprint Generation
- 🧪 QA Test Planning
- 🛡 STRIDE Threat Modeling
- 📖 Documentation Generation
- 📊 Architecture Quality Scoring
- 📜 Audit Logging

---

# 📂 Project Structure

```text
Capstone Project/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── mcp_server/
│
├── docker-compose.yml
│
└── README.md
```

---

# ⚙ Local Development

## Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs on

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 🌐 Environment Variables

## Backend (.env)

```env
DATABASE_URL=...
SECRET_KEY=...
OPENAI_API_KEY=...
```

---

## Frontend (.env)

```env
VITE_API_BASE_URL=https://cortexos-backend-p8li.onrender.com/api
```

> For local development:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

---

# 🔑 Authentication Endpoints

| Method | Endpoint |
|---------|----------|
| POST | `/api/auth/register` |
| POST | `/api/auth/login` |
| GET | `/api/auth/me` |

---

# 📦 Project APIs

| Method | Endpoint |
|---------|----------|
| GET | `/api/projects` |
| POST | `/api/projects` |
| GET | `/api/projects/{project_id}` |
| DELETE | `/api/projects/{project_id}` |

---

# 📘 Blueprint APIs

```
GET /api/blueprints/{project_id}
```

---

# 📜 Logs

```
GET /api/logs/{project_id}
```

---

# 🔍 Audit Logs

```
GET /api/audit
```

---

# 🐳 Docker

```bash
docker compose up --build
```

Services

- Frontend
- Backend
- PostgreSQL

---

# 🛠 Tech Stack

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS

## Backend

- FastAPI
- SQLAlchemy
- SQLite / PostgreSQL
- JWT Authentication

## AI

- Multi-Agent Architecture
- OpenAI GPT Models

---

# 📷 API Documentation

Swagger UI

https://cortexos-backend-p8li.onrender.com/docs

---

# 🌍 Live Deployment

### Frontend

https://cortex-os-umber.vercel.app/

### Backend

https://cortexos-backend-p8li.onrender.com/

---

# 👨‍💻 Author

**Farhan Abid**

Built for the 5 Day Intense Vibe COding Hackathon powered by Kaggle and Google
Autonomous Multi-Agent Software Engineering Platform
