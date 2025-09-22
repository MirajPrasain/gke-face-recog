# Use Node LTS as base
FROM node:18-slim

# Install system dependencies for canvas
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    libjpeg-dev \
    libgif-dev \
    librsvg2-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
RUN npm install --production

# Copy source code
COPY . .

# Rebuild canvas module for the target platform
RUN npm rebuild canvas

# Build TypeScript
RUN npm install -g typescript
RUN npx tsc

# Expose port
EXPOSE 8080

# Run the compiled JS (dist/server.js)
CMD ["node", "dist/server.js"]
