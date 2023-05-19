# Stage 1: Build Python environment
FROM python AS python-builder

# Set the working directory
WORKDIR /app


# Use the official Nginx base image
FROM nginx

# Copy the Python code from the previous stage
COPY --from=python-builder /app /app


# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the modified Nginx configuration files to the container
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d/


# Expose the Nginx port
EXPOSE 81

# Start Nginx when the container launches
CMD nginx -g  'daemon off;'

