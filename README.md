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

# Project Structure

semora/
├── PLAN.md                          ← 9-step implementation plan
├── .gitignore
├── README.md
├── .github/workflows/ci.yml         ← GitHub Actions (lint + build)
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py                  ← FastAPI app + CORS
│   │   ├── core/
│   │   │   ├── config.py            ← Pydantic settings
│   │   │   ├── redis.py             ← Async Redis client
│   │   │   └── rate_limit.py        ← IP-based daily limits
│   │   ├── api/v1/endpoints/
│   │   │   ├── resume.py            ← POST /resume/upload
│   │   │   ├── match.py             ← POST /match/
│   │   │   └── email.py             ← POST /email/generate
│   │   ├── schemas/                 ← Pydantic request/response models
│   │   └── services/
│   │       ├── pdf_parser.py        ← pdfplumber text extraction
│   │       ├── resume_parser.py     ← GPT-4o structuring
│   │       ├── embeddings.py        ← OpenAI embed + Pinecone query
│   │       └── email_generator.py   ← GPT-4o email openings
│   └── scripts/
│       ├── seed_labs.py             ← Seed Supabase + Pinecone
│       └── labs_data.json           ← Purdue lab starter data
├── frontend/                        ← (to be scaffolded in Step 1)
└── infra/docker-compose.yml