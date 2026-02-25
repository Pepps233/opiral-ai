# Semora AI — Implementation Plan

## Step 1: Infrastructure & External Services Setup
- [ ] Create Supabase project; run SQL to create tables: `labs`, `sessions`, `match_logs`, `email_logs`
- [ ] Enable Supabase Storage bucket `resumes`
- [ ] Create Pinecone index (`semora-labs`, dimension=1536, metric=cosine)
- [ ] Provision managed Redis (Upstash or Railway)
- [ ] Copy `.env.example` → `.env` in both `frontend/` and `backend/`; fill in all keys
- [ ] Scaffold Next.js app: `npx create-next-app@latest frontend --typescript --tailwind --app`
- [ ] Install shadcn/ui: `npx shadcn-ui@latest init` inside `frontend/`

**Supabase SQL schema:**
```sql
create table labs (
  lab_id text primary key,
  professor text,
  department text,
  research_areas text[],
  contact_email text,
  description text
);

create table sessions (
  session_id uuid primary key default gen_random_uuid(),
  parsed_resume jsonb,
  created_at timestamptz default now()
);

create table match_logs (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references sessions(session_id),
  lab_ids text[],
  created_at timestamptz default now()
);

create table email_logs (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references sessions(session_id),
  lab_id text,
  opening text,
  created_at timestamptz default now()
);
```

---

## Step 2: Resume Upload & PDF Storage
**Files:** `backend/app/api/v1/endpoints/resume.py`, `backend/app/services/pdf_parser.py`

- [ ] Implement `POST /api/v1/resume/upload`:
  1. Validate file is PDF, max 5MB
  2. Upload raw PDF to Supabase Storage (`resumes/{uuid}.pdf`)
  3. Extract text with `pdfplumber` (`pdf_parser.py`)
  4. Enqueue background task: parse + embed (Step 3)
  5. Return `session_id` immediately (optimistic response)
- [ ] Add file size/type validation middleware

---

## Step 3: Resume Parsing & Embedding Pipeline
**Files:** `backend/app/services/resume_parser.py`, `backend/app/services/embeddings.py`

- [ ] Complete `resume_parser.py`: call GPT-4o with structured JSON output prompt
- [ ] Store `ParsedResume` in Supabase `sessions` table (keyed by `session_id`)
- [ ] Complete `embeddings.py`: generate embedding for resume query text
- [ ] Store embedding transiently (in-memory or Redis with 24h TTL)
- [ ] Expose `GET /api/v1/resume/{session_id}` to poll parsed status

---

## Step 4: Lab Database & Matching Engine
**Files:** `backend/app/services/embeddings.py`, `backend/scripts/seed_labs.py`

- [ ] Expand `backend/scripts/labs_data.json` with 30-50 real Purdue labs (professor, dept, research areas, description, email)
- [ ] Run `python -m scripts.seed_labs` to upsert labs into Supabase + generate + upsert Pinecone vectors
- [ ] Complete `POST /api/v1/match/`:
  1. Load `ParsedResume` from Supabase by `session_id`
  2. Re-embed or fetch cached resume embedding
  3. Query Pinecone top-K (K=10)
  4. Apply role-preference reweighting (boost labs matching `desired_roles`)
  5. Return top 5 `LabMatch` objects
  6. Log to `match_logs`
- [ ] Enforce daily match limit via Redis rate limiter (already wired)

---

## Step 5: AI Email Personalization
**Files:** `backend/app/services/email_generator.py`, `backend/app/api/v1/endpoints/email.py`

- [ ] Complete `POST /api/v1/email/generate`:
  1. Load `ParsedResume` from session
  2. Fetch lab metadata from Supabase by `lab_id`
  3. Call `email_generator.generate_opening()`
  4. Log to `email_logs`
  5. Return `opening` + `subject_line`
- [ ] Enforce daily email limit via Redis rate limiter
- [ ] Store prompt templates in `backend/app/services/prompts/` for easy tuning

---

## Step 6: Frontend — Upload & Results UI
**Files:** `frontend/app/` (Next.js App Router)

- [ ] **`/` (Home)**: Hero section + drag-and-drop PDF upload component
  - Uses `shadcn/ui` Card + Button
  - Calls `POST /api/v1/resume/upload` with `FormData`
  - Shows upload progress; polls `GET /api/v1/resume/{session_id}` until parsed
  - On success → redirect to `/matches?session={session_id}`
- [ ] **`/matches`**: Display ranked lab cards
  - Fetch `POST /api/v1/match/` on mount
  - Each card: professor, department, research areas, similarity score, "Generate Email" button
  - Disable button after daily limit hit (show 429 message)
- [ ] **Email modal**: On "Generate Email" click → call `POST /api/v1/email/generate` → show copyable result
- [ ] Add Tailwind global styles, Purdue gold color palette

---

## Step 7: Rate Limiting & Usage Tracking
**Files:** `backend/app/core/rate_limit.py`, `backend/app/core/redis.py`

- [ ] Verify Redis connection on app startup (health check)
- [ ] Finalize rate limit key strategy: `rate:{action}:{ip}:{YYYY-MM-DD}` with 24h TTL
- [ ] Add `X-RateLimit-Remaining` response headers
- [ ] Frontend: parse 429 responses and show user-friendly "come back tomorrow" message
- [ ] Optional: fingerprint by `User-Agent` + IP hash for harder spoofing

---

## Step 8: Deployment
**Files:** `backend/Dockerfile`, `infra/docker-compose.yml`, `.github/workflows/ci.yml`

- [ ] **Backend**: Deploy Docker image to Render/Railway/Fly.io; set all env vars
- [ ] **Frontend**: Deploy to Vercel; set `NEXT_PUBLIC_API_URL` to backend URL
- [ ] **Redis**: Use Upstash (serverless Redis) or Railway Redis add-on
- [ ] Configure Sentry DSN in backend for error tracking
- [ ] Add `NEXT_PUBLIC_API_URL` CORS origin to backend `settings.CORS_ORIGINS`
- [ ] Smoke test: upload real resume → parse → match → email end-to-end
- [ ] Set GitHub Actions secrets for CI

---

## Step 9: Polish & Launch
- [ ] Seed 30-50 real Purdue lab entries in `labs_data.json`
- [ ] Write unit tests for `pdf_parser`, `resume_parser`, `embeddings` (mock OpenAI calls)
- [ ] Add loading skeletons and error states to all frontend views
- [ ] Mobile-responsive layout audit
- [ ] Add analytics (Vercel Analytics or Plausible) — no PII collected
- [ ] Write `README.md` local dev quickstart
