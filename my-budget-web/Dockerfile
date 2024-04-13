# Stage 1: Build the Svelte application
FROM node:18-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . ./

# Expose port 3000 for the container
EXPOSE 3000

# Build the application
RUN npm run build

FROM nginx
COPY --from=build /app/build /usr/share/nginx/html