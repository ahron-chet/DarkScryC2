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
ARG DARKSCRY_DEBUG=false

RUN echo "NEXT_PUBLIC_MANAGEMENT_API_URL=$NEXT_PUBLIC_MANAGEMENT_API_URL" >> .env.production
RUN echo "NEXT_PUBLIC_WS_URL=$NEXT_PUBLIC_WS_URL" >> .env.production

# 3) Build Next.js in production mode unless debugging
RUN if [ "$DARKSCRY_DEBUG" != "true" ]; then npm run build; fi

# 2) Final runner stage
FROM node:18-alpine AS runner

WORKDIR /app

COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/package-lock.json ./package-lock.json
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

RUN npm install --production

COPY start.sh ./start.sh
RUN chmod +x ./start.sh

EXPOSE 3000

CMD ["./start.sh"]
