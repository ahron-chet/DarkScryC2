# frontend/Dockerfile

# 1) Builder stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy all source code into the builder
COPY . /app

# Build the Next.js app
RUN npm run build

# 2) Production stage (a smaller image)
FROM node:18-alpine AS runner

WORKDIR /app

# Copy only the build output and necessary files
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
# If you have static files, etc.

EXPOSE 3000

# The default command that runs Next.js in production mode
CMD ["npm", "run", "start"]
