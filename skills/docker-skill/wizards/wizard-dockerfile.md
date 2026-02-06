# Wizard: Dockerfile

Assistant interactif pour creer un Dockerfile optimise.

## Questions

1. **Langage/Runtime** : Node.js, Python, Go, Rust, .NET, PHP, Java, static
2. **Version** : Version du runtime
3. **Type d'app** : API, web, worker, CLI
4. **Multi-stage** : Oui/Non (recommande pour production)
5. **Package manager** : npm, yarn, pnpm, pip, poetry, cargo, etc.
6. **Port expose** : Port de l'application
7. **User non-root** : Oui (recommande)

## Best practices appliquees

- Image de base alpine quand possible
- Multi-stage build pour reduire la taille
- Layer caching optimise (COPY package files avant code)
- User non-root pour la securite
- .dockerignore genere
- Healthcheck integre
- Labels OCI standards

## Template Node.js

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:20-alpine
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
WORKDIR /app
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs . .
USER nodejs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "src/index.js"]
```

## Template Python

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
RUN useradd -m -r appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
