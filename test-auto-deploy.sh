#!/bin/bash
set -e

echo "=== Testing Railway Auto-Deploy ==="
echo ""

# Get current deployed commit
BEFORE=$(curl -s https://agent-control-panel-production.up.railway.app | grep -o "Build: [a-f0-9]\{7\}" | head -1 | cut -d' ' -f2)
echo "Current deployed: $BEFORE"
echo ""

# Make a test change
echo "<!-- Auto-deploy test: $(date +%s) -->" >> public/landing.html
git add public/landing.html
git commit -m "Test: Auto-deploy verification $(date +%s)"
git push origin main

TEST_COMMIT=$(git rev-parse --short HEAD)
echo "Test commit pushed: $TEST_COMMIT"
echo "Waiting 2 minutes for auto-deploy..."
echo ""

sleep 120

# Check if new commit deployed
AFTER=$(curl -s https://agent-control-panel-production.up.railway.app | grep -o "Build: [a-f0-9]\{7\}" | head -1 | cut -d' ' -f2)
echo "Now deployed: $AFTER"
echo ""

if [ "$AFTER" = "$TEST_COMMIT" ]; then
  echo "✅ SUCCESS! Auto-deploy is working!"
  echo "Railway automatically deployed commit $TEST_COMMIT from GitHub"
  exit 0
else
  echo "❌ FAILED! Auto-deploy not working."
  echo "Expected: $TEST_COMMIT"
  echo "Got: $AFTER"
  exit 1
fi
