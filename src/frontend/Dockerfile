FROM docker.uclv.cu/node:lts-alpine AS builder

# Declaring env
ENV NODE_ENV production

# Setting up the work directory
WORKDIR /app

# Installing dependencies
COPY ./package.json /app/package.json
COPY ./postcss.config.js /app/postcss.config.js 
COPY ./tailwind.config.js /app/tailwind.config.js
COPY ./tsconfig.json /app/tsconfig.json
RUN npm install

# Copying all the files in our project
COPY ./public /app/public
COPY ./src /app/src

# Building our application
RUN npm run build

# Fetching the latest nginx image
FROM docker.uclv.cu/nginx

# Copying built assets from builder
COPY --from=builder /app/build /usr/share/nginx/html

# Copying our nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf