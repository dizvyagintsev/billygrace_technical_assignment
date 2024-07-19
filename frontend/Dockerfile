# Stage 1: Build the react application
FROM node:16 AS build

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
ENV GENERATE_SOURCEMAP=false

# Build the application
RUN yarn build

# Stage 2: Serve the react application
FROM node:16 AS serve

# Install serve globally
RUN yarn global add serve

# Copy the build output from the build stage
COPY --from=build /app/build /app/build

# Expose port 3000
EXPOSE 3000

WORKDIR /app

# Serve the application
CMD ["serve", "-s", "build"]
