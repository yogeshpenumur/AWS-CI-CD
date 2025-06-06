# Use Ubuntu as the base image
FROM ubuntu:latest

# Set environment variable to avoid interaction during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install Apache
RUN apt-get update && \
    apt-get install -y apache2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy HTML file to Apache default root directory
COPY index.html /var/www/html/index.html

# Expose port 80 for HTTP
EXPOSE 80

# Start Apache in the foreground
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
