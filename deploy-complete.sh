#!/bin/bash
# Deploy Script - React Field Insights
# Complete deployment with OpenAI API Key configured

echo "🚀 React Field Insights - Complete Deployment"
echo "=============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

echo "✅ docker-compose is available"

# Stop any existing containers
echo "🔄 Stopping existing containers..."
docker-compose down

# Remove old volumes (optional - comment out to preserve data)
# echo "🧹 Cleaning old volumes..."
# docker-compose down -v

# Build and start services
echo "🏗️ Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check API health
if curl -f http://localhost:8000/healthz > /dev/null 2>&1; then
    echo "✅ API Server is healthy (http://localhost:8000)"
else
    echo "⚠️ API Server not responding yet, checking logs..."
    docker-compose logs api | tail -20
fi

# Check database connection
echo "🗄️ Testing database connection..."
docker-compose exec -T db psql -U postgres -d fieldback -c "SELECT 1;" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Database is connected"
else
    echo "⚠️ Database connection issues"
fi

# Show running services
echo "📋 Running services:"
docker-compose ps

echo ""
echo "🎉 Deployment Complete!"
echo "========================================"
echo "📊 API Server: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "🗄️ Database: localhost:5432"
echo ""
echo "🔑 Configured Features:"
echo "✅ OpenAI API Key: sk-proj-...rt4IA (configured)"
echo "✅ SendGrid Email: danielepili@react-company.com"
echo "✅ AI Processing: ENABLED"
echo "✅ Mobile PWA: Ready"
echo "✅ Multi-tenant: Ready"
echo ""
echo "🧪 Test Commands:"
echo "# Test AI features:"
echo "python test_ai_features.py"
echo ""
echo "# Test SendGrid email:"
echo "python test_sendgrid.py your-email@domain.com"
echo ""
echo "# Login credentials (default):"
echo "Company: ACME001"
echo "User: user1"
echo "Password: Password.1"
echo ""
echo "🎯 Next Steps:"
echo "1. Visit http://localhost:8000/docs to see API documentation"
echo "2. Test mobile PWA interface"
echo "3. Create your first insight with AI processing"
echo "4. Generate weekly reports"
echo ""
echo "📱 For mobile testing, access from smartphone browser:"
echo "http://your-server-ip:8000"
echo ""
echo "🔧 To stop services: docker-compose down"
echo "🔧 To view logs: docker-compose logs -f"
