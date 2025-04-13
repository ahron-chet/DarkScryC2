# 1) Builder stage
FROM node:18-alpine AS builder

WORKDIR /app

# Define build args for each variable you want to inject
ARG NEXT_PUBLIC_DJANGO_API_URL_V2
ARG NEXT_PUBLIC_WS_URL
ARG NEXTAUTH_URL
ARG NEXTAUTH_SECRET

# Copy package files for dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . ./

# 2) Write those variables to .env.production
#   (If you prefer .env.local or something else, adjust accordingly.)
RUN echo "NEXT_PUBLIC_DJANGO_API_URL_V2=$NEXT_PUBLIC_DJANGO_API_URL_V2" >> .env.production
RUN echo "NEXT_PUBLIC_WS_URL=$NEXT_PUBLIC_WS_URL" >> .env.production
RUN echo "NEXTAUTH_URL=$NEXTAUTH_URL" >> .env.production
RUN echo "NEXTAUTH_SECRET=$NEXTAUTH_SECRET" >> .env.production

# 3) Build Next.js in production mode
RUN npm run build

# 2) Final runner stage
FROM node:18-alpine AS runner

WORKDIR /app

# Copy only what's needed from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.env.production ./

EXPOSE 3000

CMD ["npm", "run", "start"]
