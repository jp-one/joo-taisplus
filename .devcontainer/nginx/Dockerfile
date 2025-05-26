FROM nginx:alpine

# Generate self-signed SSL certificate and key
ARG SSL_DAYS=365
ARG SSL_SUBJECT="/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"
RUN apk add --no-cache openssl
RUN mkdir -p /etc/nginx/ssl
RUN openssl req -x509 -nodes -days ${SSL_DAYS} -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/server.key \
    -out /etc/nginx/ssl/server.crt \
    -subj ${SSL_SUBJECT}

# Expose ports
EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
