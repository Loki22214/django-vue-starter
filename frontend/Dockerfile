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

COPY ./package*.json ./
RUN npm ci --only=production

COPY . .

RUN npm run build

# Production stage with nginx
FROM nginx:alpine AS production

COPY --from=builder /app/dist /usr/share/nginx/html

RUN adduser -D -g '' -u 1001 appuser && \
    mkdir -p /var/cache/nginx /var/run /var/log/nginx && \
    chown -R appuser:appuser /usr/share/nginx/html /var/cache/nginx /var/run /var/log/nginx && \
    chmod -R 755 /usr/share/nginx/html /var/cache/nginx /var/run /var/log/nginx && \
    # Modify default nginx to run on port 5173 and remove user directive
    sed -i 's/listen\s*80;/listen 5173;/g' /etc/nginx/conf.d/default.conf && \
    sed -i 's/^user.*$//g' /etc/nginx/nginx.conf && \
    sed -i 's/pid \/run\/nginx.pid/pid \/var\/run\/nginx.pid/g' /etc/nginx/nginx.conf

USER appuser

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]