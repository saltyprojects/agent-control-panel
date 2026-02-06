#!/bin/bash
set -e

# Agent Control Panel Deployment to Railway
RAILWAY_TOKEN="c4ed3cb5-5d14-4a4b-a23b-9cff27608bb7"
PROJECT_ID="43a7422e-842f-476e-a6bb-f5214e9a74a8"
ENV_ID="40ab4801-4fbd-4ab5-b715-8887f1bb987f"
REPO="saltyprojects/agent-control-panel"

echo "🚂 Deploying Agent Control Panel to Railway..."

# 1. Create new service
echo "📦 Creating new service..."
SERVICE_ID=$(curl -s -X POST https://backboard.railway.app/graphql/v2 \
  -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation { serviceCreate(input: { projectId: \\\"$PROJECT_ID\\\", name: \\\"web\\\" }) { id name } }\"}" \
  | jq -r '.data.serviceCreate.id')

if [ "$SERVICE_ID" == "null" ] || [ -z "$SERVICE_ID" ]; then
  echo "❌ Failed to create service"
  exit 1
fi

echo "✅ Service created: $SERVICE_ID"

# 2. Connect GitHub repo
echo "🔗 Connecting GitHub repo..."
curl -s -X POST https://backboard.railway.app/graphql/v2 \
  -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation { serviceInstanceUpdate(serviceId: \\\"$SERVICE_ID\\\", input: { source: { repo: \\\"$REPO\\\" } }) }\"}" > /dev/null

echo "✅ Repo connected"

# 3. Trigger deployment
echo "🚀 Deploying..."
curl -s -X POST https://backboard.railway.app/graphql/v2 \
  -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation { serviceInstanceDeploy(serviceId: \\\"$SERVICE_ID\\\", environmentId: \\\"$ENV_ID\\\") }\"}" > /dev/null

echo "✅ Deployment triggered"

# 4. Create/generate domain
echo "🌐 Creating domain..."
DOMAIN=$(curl -s -X POST https://backboard.railway.app/graphql/v2 \
  -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation { serviceDomainCreate(input: { serviceId: \\\"$SERVICE_ID\\\", environmentId: \\\"$ENV_ID\\\" }) { domain } }\"}" \
  | jq -r '.data.serviceDomainCreate.domain')

if [ "$DOMAIN" == "null" ] || [ -z "$DOMAIN" ]; then
  echo "⚠️  Domain creation failed or already exists"
else
  echo "✅ Domain: https://$DOMAIN"
fi

echo ""
echo "🎉 Deployment complete!"
echo "Service ID: $SERVICE_ID"
echo "Check status in ~2 minutes at:"
echo "https://railway.app/project/$PROJECT_ID"
