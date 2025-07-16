# 1) Builder stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files for dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . ./

ARG NEXT_PUBLIC_MANAGEMENT_API_URL
ARG NEXT_PUBLIC_WS_URL
ARG NEXTAUTH_URL
ARG NEXTAUTH_SECRET
ARG DARKSCRY_DEBUG=false

RUN echo "NEXT_PUBLIC_MANAGEMENT_API_URL=$NEXT_PUBLIC_MANAGEMENT_API_URL" >> .env.production
RUN echo "NEXT_PUBLIC_WS_URL=$NEXT_PUBLIC_WS_URL" >> .env.production
RUN echo "NEXTAUTH_URL=$NEXTAUTH_URL" >> .env.production
RUN echo "NEXTAUTH_SECRET=$NEXTAUTH_SECRET" >> .env.production

# 3) Build Next.js in production mode unless debugging
RUN if [ "$DARKSCRY_DEBUG" != "true" ]; then npm run build; fi

# 2) Final runner stage
FROM node:18-alpine AS runner

WORKDIR /app

# Copy full source for dev mode and build output for production
COPY --from=builder /app /app
COPY start.sh ./start.sh
RUN chmod +x ./start.sh

EXPOSE 3000

CMD ["./start.sh"]
