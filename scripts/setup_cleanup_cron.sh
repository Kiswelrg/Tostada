#!/bin/bash

# Tostada Cleanup Cron Setup Script
# This script sets up a cron job to run the Django cleanup command periodically

set -e  # Exit on any error

# Configuration - MODIFY THESE VALUES FOR YOUR DEPLOYMENT
PROJECT_PATH="/opt/tostada"  # Change to your project path
PYTHON_PATH="/opt/tostada/venv/bin/python"  # Change to your Python path
SCHEDULE="0 2 * * *"  # Default: daily at 2 AM
LOG_FILE="/var/log/tostada-cleanup.log"
USER="www-data"  # Change to your app user

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Tostada Cleanup Cron Setup${NC}"
echo "=================================="

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root or with sudo
if [[ $EUID -ne 0 ]]; then
    print_error "This script must be run as root or with sudo"
    exit 1
fi

# Validate paths exist
if [[ ! -d "$PROJECT_PATH" ]]; then
    print_error "Project path does not exist: $PROJECT_PATH"
    print_info "Please update PROJECT_PATH in this script"
    exit 1
fi

if [[ ! -f "$PYTHON_PATH" ]]; then
    print_error "Python executable not found: $PYTHON_PATH"
    print_info "Please update PYTHON_PATH in this script"
    exit 1
fi

if [[ ! -f "$PROJECT_PATH/manage.py" ]]; then
    print_error "Django manage.py not found in: $PROJECT_PATH"
    exit 1
fi

# Test the cleanup command works
print_info "Testing cleanup command..."
cd "$PROJECT_PATH"
if sudo -u "$USER" "$PYTHON_PATH" manage.py cleanup_expired --dry-run > /dev/null 2>&1; then
    print_info "✓ Cleanup command test successful"
else
    print_error "✗ Cleanup command test failed"
    print_info "Please check your Django setup and database connectivity"
    exit 1
fi

# Create log directory if it doesn't exist
LOG_DIR=$(dirname "$LOG_FILE")
if [[ ! -d "$LOG_DIR" ]]; then
    print_info "Creating log directory: $LOG_DIR"
    mkdir -p "$LOG_DIR"
fi

# Ensure log file exists and has correct permissions
touch "$LOG_FILE"
chown "$USER:$USER" "$LOG_FILE"
chmod 644 "$LOG_FILE"

# Create the cron job entry
CRON_ENTRY="$SCHEDULE cd $PROJECT_PATH && $PYTHON_PATH manage.py cleanup_expired >> $LOG_FILE 2>&1"

print_info "Setting up cron job for user: $USER"
print_info "Schedule: $SCHEDULE (daily at 2 AM)"
print_info "Command: cd $PROJECT_PATH && $PYTHON_PATH manage.py cleanup_expired"
print_info "Log file: $LOG_FILE"

# Add cron job for the specified user
(sudo -u "$USER" crontab -l 2>/dev/null | grep -v "cleanup_expired"; echo "$CRON_ENTRY") | sudo -u "$USER" crontab -

print_info "✓ Cron job added successfully"

# Show current crontab
print_info "Current crontab for $USER:"
echo "---"
sudo -u "$USER" crontab -l | grep -E "(cleanup_expired|^#|^$)" || true
echo "---"

# Create a manual run script
MANUAL_SCRIPT="$PROJECT_PATH/scripts/run_cleanup.sh"
mkdir -p "$(dirname "$MANUAL_SCRIPT")"

cat > "$MANUAL_SCRIPT" << EOF
#!/bin/bash
# Manual cleanup script for Tostada
# Usage: ./run_cleanup.sh [--dry-run]

cd "$PROJECT_PATH"
exec "$PYTHON_PATH" manage.py cleanup_expired "\$@"
EOF

chmod +x "$MANUAL_SCRIPT"
chown "$USER:$USER" "$MANUAL_SCRIPT"

print_info "✓ Created manual run script: $MANUAL_SCRIPT"

echo ""
print_info "Setup complete! Next steps:"
echo "1. Test manual run: sudo -u $USER $MANUAL_SCRIPT --dry-run"
echo "2. View logs: tail -f $LOG_FILE"
echo "3. Modify schedule by editing crontab: sudo -u $USER crontab -e"
echo ""
print_info "Schedule options:"
echo "  Every 6 hours:  0 */6 * * *"
echo "  Every 12 hours: 0 */12 * * *"
echo "  Daily at 2 AM:  0 2 * * *"
echo "  Weekly:         0 2 * * 0"
echo ""
print_info "To change schedule, edit this script and re-run it"