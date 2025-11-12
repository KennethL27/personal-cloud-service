#!/bin/bash

set -e

echo "🚀 Setting up production environment on Raspberry Pi..."

# Create .env.production
cat > .env.production << EOF
ENVIRONMENT=production
EXTERNAL_DRIVE_PATH=${EXTERNAL_DRIVE_PATH}
DOMAIN_NAME=${DOMAIN_NAME}
SSL_EMAIL=${SSL_EMAIL}
DATABASE_NAME=personal_app.db
BACKEND_PORT=8000
FRONTEND_PORT=3000
NGINX_HTTP_PORT=80
NGINX_HTTPS_PORT=443
NEXT_PUBLIC_API_URL=https://${DOMAIN_NAME}/api
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
EOF

# Create src/.env for backend
cat > src/.env << EOF
DATABASE_URL=sqlite:///personal_app.db
STORAGE_PATH=/mnt/storage1
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
JWT_SECRET_KEY=${JWT_SECRET_KEY}
JWT_ALGORITHM=${JWT_ALGORITHM}
ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}
ALLOWED_EMAILS=${ALLOWED_EMAILS}
FIRST_USER_EMAIL=${FIRST_USER_EMAIL}
FIRST_USER_NAME=${FIRST_USER_NAME}
ENVIRONMENT=production
EOF

# Load production environment
export $(cat .env.production | grep -v '#' | xargs)

# Generate nginx config for production
echo "📝 Generating nginx configuration..."
./scripts/generate-nginx-config.sh

# Create certbot directories
mkdir -p certbot/conf certbot/www

# Check if SSL certificate exists
if [ ! -f "certbot/conf/live/${DOMAIN_NAME}/fullchain.pem" ]; then
    echo "🔒 Obtaining SSL certificate..."
    
    # Start nginx temporarily for certbot
    docker-compose up -d nginx
    
    # Get certificate
    docker-compose run --rm certbot certonly --webroot \
        --webroot-path=/var/www/certbot \
        --email ${SSL_EMAIL} \
        --agree-tos \
        --no-eff-email \
        -d ${DOMAIN_NAME} -d www.${DOMAIN_NAME}
    
    # Reload nginx with SSL
    docker-compose restart nginx
fi

# Build and start all services
echo "🐳 Building and starting Docker containers..."
docker-compose --profile production down
docker-compose --profile production up -d --build

# Clean up old images
docker system prune -af

echo "✅ Production environment is ready!"
echo ""
echo "🌐 Access your app at: https://${DOMAIN_NAME}"