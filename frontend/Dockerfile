# syntax=docker.io/docker/dockerfile:1

# Loosely based on example from
# https://raw.githubusercontent.com/vercel/next.js/refs/heads/canary/examples/with-docker/Dockerfile

#FROM node:18-alpine AS base
FROM node:22-bookworm AS base

##
## "deps" - fetch node_modules etc
##
FROM base AS deps

# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine
# to understand why libc6-compat might be needed.
#RUN apk add --no-cache libc6-compat

WORKDIR /pyaicam-view

# All the top level configs (needed this early?)
COPY pyaicam-view/eslint.config.mjs .
COPY pyaicam-view/next-env.d.ts .
COPY pyaicam-view/next.config.ts .
COPY pyaicam-view/package.json .
COPY pyaicam-view/package-lock.json .
COPY pyaicam-view/tsconfig.json .

RUN npm clean-install


##
## "builder" - add sources, build the thing
##
FROM base AS builder

WORKDIR /pyaicam-view
#COPY --from=deps /pyaicam-view/node_modules ./node_modules
#COPY --from=deps /pyaicam-view/package.json .
#COPY --from=deps /pyaicam-view/package-lock.json .
COPY --from=deps /pyaicam-view .
COPY pyaicam-view/public ./public
COPY pyaicam-view/src ./src

# No sharing.
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Standalone build ==>
# https://nextjs.org/docs/pages/api-reference/config/next-config-js/output#automatically-copying-traced-files
# ==> Necessary bits end up here:
# .next/standalone/server.js	-- Run instead of `next start`
# .next/standalone/node_modules -- 
# .next/static/{css,media,*}	-- Expected to be served by CDN
# public/{*.svg}		-- Needed here, but build does not.


##
## "runner" - extract built parts needed to deploy
##
FROM base AS runner

WORKDIR /pyaicam-view

# No sharing.
ENV NEXT_TELEMETRY_DISABLED=1

# Create a complete standalone deployment:
# .next/standalone	=> .next/standalone
# .next/static		=> .next/standalone/.next/static
# public		=> .next/standalone/public
COPY --from=builder --chown=nextjs:nodejs /pyaicam-view/.next/standalone ./.next/standalone
COPY --from=builder --chown=nextjs:nodejs /pyaicam-view/.next/static ./.next/standalone/.next/static
COPY --from=builder --chown=nextjs:nodejs /pyaicam-view/public ./.next/standalone/public

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

ENV NODE_ENV=production
ENV HOSTNAME="0.0.0.0"
ENV PORT=3000

EXPOSE 3000

# "run `node server.js`"
CMD ["node", ".next/standalone/server.js"]
