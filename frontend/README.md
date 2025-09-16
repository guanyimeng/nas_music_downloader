# NAS Music Downloader — Frontend (React + Vite)

This is the React single-page application (SPA) that provides a user interface for the NAS Music Downloader backend (FastAPI). It supports user authentication, queuing downloads by URL, and viewing live/paginated download status.

- Tech stack: React 18, TypeScript, Vite, React Router, Axios
- Auth: JWT Bearer tokens returned by the backend via `/auth/login` (OAuth2PasswordRequestForm)
- API integration: Relative paths (`/auth`, `/api`) by default, proxied in dev (Vite) and in production (Nginx in container)

## Features

- Login/Register, persisted JWT in `localStorage`
- Start a new download by URL (POST `/api/download`)
- Recent activity with live polling (GET `/api/downloads`)
- History page with pagination (GET `/api/downloads?page=&per_page=`)
- Logout and protected routes

## Requirements

- Node.js 18+ (Node 20+ recommended)
- npm (comes with Node)
- Backend running at `http://localhost:8000` (or reachable URL). In dev mode, Vite proxies `/auth` and `/api` to this target.

If you prefer containers, see Docker instructions below or run everything via the root `docker-compose.yml` (recommended).

## Local Development (Vite)

1) Install dependencies
```
cd nas_music_downloader/frontend
npm install
```

2) Start the dev server
```
npm run dev
```
- Opens at http://localhost:5173
- Vite proxy routes `/auth` and `/api` to http://localhost:8000 (configured in `vite.config.ts`)

3) Optional: override API base
- The app uses relative paths by default. If you need to hit a different backend (not on localhost), set an env var at build time:
```
VITE_API_BASE_URL=https://your-backend.example.com npm run dev
```
- When `VITE_API_BASE_URL` is unset, Axios baseURL is `""` and Vite/Nginx proxy handle routing to the backend.

## Scripts

- `npm run dev` — start Vite dev server on port 5173 (with proxy)
- `npm run build` — build the production site to `dist/`
- `npm run preview` — preview the built site locally on port 5173

## Project Structure

```
frontend/
├── Dockerfile                # Multi-stage build, serves via Nginx
├── nginx.conf                # Nginx config that proxies /auth,/api to backend
├── index.html                # Vite HTML entry
├── package.json              # Dependencies and scripts
├── tsconfig.json             # TypeScript config
├── vite.config.ts            # Vite config + dev proxy
└── src/
   ├── App.tsx                # Routes and nav
   ├── index.css              # Basic styling
   ├── main.tsx               # App bootstrap
   ├── types.ts               # API types
   ├── api/
   │  └── client.ts           # Axios client & API wrappers
   ├── components/
   │  └── ProtectedRoute.tsx  # Route guard
   ├── pages/
   │  ├── Download.tsx        # URL input + start + live status
   │  ├── History.tsx         # Paginated history
   │  ├── Login.tsx           # Login form
   │  └── Register.tsx        # Registration form
   └── state/
      └── AuthContext.tsx     # Auth state, token storage, me/logout
```

## Routing and Auth

- Protected routes are wrapped by `ProtectedRoute` and require a valid JWT (stored in `localStorage` as `token`).
- On login, backend returns `{ access_token, token_type }`. We store the token and then call `/auth/me` to fetch user info.
- Axios interceptor attaches `Authorization: Bearer <token>` for all requests when a token is present.

## Docker (Frontend Only)

You can containerize and run just the frontend. Note that you still need a backend reachable from the container.

Build the frontend image:
```
cd nas_music_downloader/frontend
docker build -t nas-music-frontend .
```

Run it:
```
docker run --rm -p 3000:80 --name nas-music-frontend nas-music-frontend
```
- App available at http://localhost:3000
- Nginx proxies `/auth` and `/api` to `http://backend:8000` (when used in the root docker-compose with a `backend` service). If running this container standalone, set up networking so `backend` resolves, or modify `nginx.conf` accordingly.

## Using with Root Docker Compose (Recommended)

From the repository root:
```
docker compose up -d --build
```
- Frontend served at http://localhost:3000
- Backend API at http://localhost:8000

See root README for environment variables like `DOWNLOADS_HOST_PATH` to mount your NAS path.

## Troubleshooting

- “npm is not recognized…” — install Node.js from https://nodejs.org and ensure npm is on PATH.
- TS/JS import errors in editor — run `npm install` to pull types and dev dependencies.
- CORS errors in browser — in dev, requests are proxied by Vite to the backend. Ensure backend runs at http://localhost:8000. Backend CORS allows http://localhost:5173 and http://localhost:3000.
- 401 Unauthorized — ensure you logged in successfully and the token is in `localStorage`. If your backend `SECRET_KEY` changes, previous tokens become invalid; log in again.
- Reverse proxy/SSL — if you place the app behind an external proxy with SSL, set `VITE_API_BASE_URL` accordingly during build or update `nginx.conf` to proxy to your backend hostname.

## License

MIT — see project root for details.
