# Stage 1: Build the react application
FROM node:21-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and yarn.lock
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install

## Copy the rest of the application
COPY . .

ARG API_BASE_URL
ENV REACT_APP_API_BASE_URL=$API_BASE_URL
ENV GENERATE_SOURCEMAP=true

# Build the application
RUN yarn build

# Stage 2: Serve the React application using nginx
FROM nginx:alpine AS serve

# Copy the build output from the build stage
COPY --from=build /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

# Start nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
