# Build stage
FROM node:24-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage using Nginx
FROM nginx:stable-alpine
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Run nginx
CMD ["nginx", "-g", "daemon off;"]
