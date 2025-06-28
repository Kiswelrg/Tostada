#!/bin/bash

# Jenkins-friendly Tostada Cleanup Setup Script
# This script is designed to be run from Jenkins CI/CD pipeline

set -e  # Exit on any error

# Environment variables (set these in Jenkins)
PROJECT_PATH="${TOSTADA_PROJECT_PATH:-/opt/tostada}"
PYTHON_PATH="${TOSTADA_PYTHON_PATH:-/opt/tostada/venv/bin/python}"
APP_USER="${TOSTADA_USER:-www-data}"
CLEANUP_SCHEDULE="${TOSTADA_CLEANUP_SCHEDULE:-0 2 * * *}"
LOG_FILE="${TOSTADA_LOG_FILE:-/var/log/tostada-cleanup.log}"

echo "=== Tostada Cleanup Cron Setup (Jenkins) ==="
echo "Project Path: $PROJECT_PATH"
echo "Python Path: $PYTHON_PATH"
echo "App User: $APP_USER"
echo "Schedule: $CLEANUP_SCHEDULE"
echo "Log File: $LOG_FILE"
echo "=============================================="

# Validation
if [[ ! -d "$PROJECT_PATH" ]]; then
    echo "ERROR: Project path does not exist: $PROJECT_PATH"
    echo "Set TOSTADA_PROJECT_PATH environment variable"
    exit 1
fi

if [[ ! -f "$PYTHON_PATH" ]]; then
    echo "ERROR: Python executable not found: $PYTHON_PATH"
    echo "Set TOSTADA_PYTHON_PATH environment variable"
    exit 1
fi

if [[ ! -f "$PROJECT_PATH/manage.py" ]]; then
    echo "ERROR: Django manage.py not found in: $PROJECT_PATH"
    exit 1
fi

# Test cleanup command
echo "Testing cleanup command..."
cd "$PROJECT_PATH"
if sudo -u "$APP_USER" "$PYTHON_PATH" manage.py cleanup_expired --dry-run; then
    echo "✓ Cleanup command test passed"
else
    echo "✗ Cleanup command test failed"
    exit 1
fi

# Setup log file
LOG_DIR=$(dirname "$LOG_FILE")
sudo mkdir -p "$LOG_DIR"
sudo touch "$LOG_FILE"
sudo chown "$APP_USER:$APP_USER" "$LOG_FILE"
sudo chmod 644 "$LOG_FILE"

# Create cron entry
CRON_ENTRY="$CLEANUP_SCHEDULE cd $PROJECT_PATH && $PYTHON_PATH manage.py cleanup_expired >> $LOG_FILE 2>&1"

echo "Installing cron job for user: $APP_USER"
(sudo -u "$APP_USER" crontab -l 2>/dev/null | grep -v "cleanup_expired" || true; echo "$CRON_ENTRY") | sudo -u "$APP_USER" crontab -

echo "✓ Cron job installed successfully"

# Verify cron job
echo "Current cron jobs for $APP_USER:"
sudo -u "$APP_USER" crontab -l | grep cleanup_expired || echo "No cleanup_expired jobs found"

# Create convenience scripts
SCRIPTS_DIR="$PROJECT_PATH/scripts"
sudo mkdir -p "$SCRIPTS_DIR"

# Manual run script
cat > /tmp/run_cleanup.sh << EOF
#!/bin/bash
cd "$PROJECT_PATH"
exec "$PYTHON_PATH" manage.py cleanup_expired "\$@"
EOF

sudo mv /tmp/run_cleanup.sh "$SCRIPTS_DIR/run_cleanup.sh"
sudo chmod +x "$SCRIPTS_DIR/run_cleanup.sh"
sudo chown "$APP_USER:$APP_USER" "$SCRIPTS_DIR/run_cleanup.sh"

# Status check script
cat > /tmp/cleanup_status.sh << EOF
#!/bin/bash
echo "=== Tostada Cleanup Status ==="
echo "Cron jobs for $APP_USER:"
sudo -u "$APP_USER" crontab -l | grep cleanup_expired || echo "No cleanup jobs found"
echo ""
echo "Recent log entries:"
tail -10 "$LOG_FILE" 2>/dev/null || echo "No log file found"
echo ""
echo "Test dry run:"
cd "$PROJECT_PATH" && "$PYTHON_PATH" manage.py cleanup_expired --dry-run
EOF

sudo mv /tmp/cleanup_status.sh "$SCRIPTS_DIR/cleanup_status.sh"
sudo chmod +x "$SCRIPTS_DIR/cleanup_status.sh"

echo ""
echo "=== Setup Complete ==="
echo "Manual cleanup: sudo -u $APP_USER $SCRIPTS_DIR/run_cleanup.sh"
echo "Check status: $SCRIPTS_DIR/cleanup_status.sh"
echo "View logs: tail -f $LOG_FILE"
echo ""
echo "Jenkins Environment Variables Used:"
echo "  TOSTADA_PROJECT_PATH=$PROJECT_PATH"
echo "  TOSTADA_PYTHON_PATH=$PYTHON_PATH"
echo "  TOSTADA_USER=$APP_USER"
echo "  TOSTADA_CLEANUP_SCHEDULE=$CLEANUP_SCHEDULE"
echo "  TOSTADA_LOG_FILE=$LOG_FILE"