# Build stage
FROM node:20-alpine AS build
WORKDIR /app

# Install deps
COPY package*.json ./
# Prefer lockfile when present; fall back to npm install
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copy source
COPY . .

# Allow passing a custom API base at build time if desired (empty means use relative paths)
ARG VITE_API_BASE_URL=
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# Build static site
RUN npm run build

# Runtime stage
FROM nginx:alpine
# Use our nginx config with API proxy to backend
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy built app
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

# Lightweight healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD wget -qO- http://127.0.0.1/ >/dev/null 2>&1 || exit 1
