# AI Hub Post Voting Tool

A small full-stack app where users can:
- Post text
- Upvote/downvote posts
- Read posts sorted by score and recency

The frontend is static and can be deployed to **GitHub Pages**. The backend is a **FastAPI** API with **SQLite** storage and can be called from Python.

## Project layout

- `docs/` — static frontend for GitHub Pages
- `backend/` — FastAPI API + SQLite database
- `client/` — small Python client example

## Local run

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend

Serve `docs/` as static files (any static server):

```bash
python -m http.server 5500 --directory docs
```

Open `http://localhost:5500` and set API URL to `http://localhost:8000`.

## API

- `GET /api/health`
- `GET /api/posts`
- `POST /api/posts` with JSON `{ "text": "..." }`
- `POST /api/posts/{post_id}/vote` with JSON `{ "delta": 1 }` or `{ "delta": -1 }`

## Python usage

```python
from client.api_client import ApiClient

api = ApiClient("http://localhost:8000")
post = api.create_post("Hello from Python")
api.vote(post["id"], 1)
print(api.list_posts())
```

## Deploy

### Frontend to GitHub Pages

- Push repo to GitHub.
- In repo settings, enable Pages from GitHub Actions.
- Workflow at `.github/workflows/pages.yml` deploys `docs/`.

### Backend

Deploy backend separately (Render/Railway/Fly/any Python host). This repo includes:
- `backend/Dockerfile`
- `backend/render.yaml`

After deployment, set the frontend API URL to your backend URL.

## Can I deploy the backend using GitHub?

Yes, but **not on GitHub Pages** (Pages only hosts static files).

You can still use GitHub as your deployment source in two common ways:

1. **Connect your GitHub repo to a backend host** (Render, Railway, Fly.io, etc.) and deploy from the `backend/` folder.
2. **Use GitHub Actions** to trigger deployments to your backend host when you push to `main`.

In short: GitHub is great for source + CI/CD, while the running FastAPI backend must live on a backend-capable platform.

### Which GitHub Action deployment template should I pick?

From the templates you listed, these are the best matches for this FastAPI backend:

- **Deploy a Python app to an Azure Web App** → Best "no container" option for this repo.
- **Deploy a container to an Azure Web App** → Best if you want to use `backend/Dockerfile`.
- **Build and Deploy to Cloud Run** (or **Deploy to Cloud Run from Source**) → Good managed container option on Google Cloud.
- **Deploy to Amazon ECS** → Good AWS container option (more setup, very flexible).
- **Build and Deploy to GKE / AKS / OpenShift / ACK / IBM K8s / Tencent TKE** → Kubernetes options (powerful, but usually more complex than needed for a small app).

Templates that are **not a fit** for this backend:
- Azure **Static Web Apps** (static frontend only, no long-running FastAPI service)
- Azure **Functions** templates (serverless function model, not a direct drop-in for this ASGI app as-is)
- Node/.NET/Java/PHP-specific app templates (wrong runtime stack)

### Recommended path (simplest)

1. Keep using GitHub Pages for `docs/` frontend.
2. Deploy backend with either:
   - Render using `backend/render.yaml`, or
   - Azure Web App using **Deploy a Python app to an Azure Web App** template.
3. Set the frontend API URL to your deployed backend URL.


### What about GitHub Pages templates like Jekyll/Hugo/Next.js/Astro/etc.?

Those templates are for building and deploying **frontend/static sites** only.
They do **not** host a running FastAPI backend process.

For this repo specifically:
- **Most recommended:** **Static HTML** (because your frontend is already plain files in `docs/`).
- **Also valid if you migrate frontend stacks:** Jekyll, Hugo, Next.js static export, mdBook, Astro, Gatsby, Nuxt static output.
- **Not needed right now:** Jekyll/Hugo/etc. templates unless you plan to rebuild the frontend in those frameworks.

So the practical split remains:
1. Use a GitHub Pages/static-site template for `docs/` frontend.
2. Use Azure Web App / Render / Cloud Run / ECS / Kubernetes for the FastAPI backend.

