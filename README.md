# Semora AI

AI-powered research lab matching for Purdue University students.

## Structure

```
semora/
├── frontend/    # Next.js (TypeScript) + Tailwind + shadcn/ui
├── backend/     # FastAPI (Python) + Uvicorn
├── infra/       # Docker, deployment configs
└── .github/     # CI/CD workflows
```

## Quick Start

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables

See `frontend/.env.example` and `backend/.env.example` for required keys.
