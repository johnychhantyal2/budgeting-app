# Stage 1: Build the Svelte application
FROM node:18 AS build-stage

WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Expose port 3000 for the container
EXPOSE 3000

# Stage 2 is omitted since you're serving directly from the build container
CMD ["node","-r","dotenv/config", "build"]
