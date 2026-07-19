# Stage 1: Build static React + Vite application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package lock and configurations
COPY package*.json ./

# Install packages
RUN npm ci

# Copy source code files
COPY . .

# Build arguments to pass Vite environment variables at build-time
ARG VITE_API_URL=http://localhost:8000/api/v1
ENV VITE_API_URL=$VITE_API_URL

# Build client production bundle
RUN npm run build

# Stage 2: Serve React app with Nginx
FROM nginx:stable-alpine

# Copy custom Nginx SPA configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy production built dist directory from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
