# Base stage for common dependencies
FROM node:22-alpine AS base

WORKDIR /app

# Development stage
FROM base AS development

COPY ./package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

# Build stage for production
FROM base AS builder

ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

COPY ./package*.json ./
RUN npm ci --only=production

COPY . .

RUN npm run build

# Production stage with nginx
FROM nginx:alpine AS production

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

RUN adduser -D -H -u 1001 appuser && \
    mkdir -p /tmp/nginx /var/cache/nginx && \
    chown -R appuser:appuser \
        /tmp/nginx \
        /var/cache/nginx \
        /usr/share/nginx/html \
        /etc/nginx

USER appuser

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]