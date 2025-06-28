# Periodic Cleanup Setup Guide

## Management Command

The cleanup command is located at: `tool/management/commands/cleanup_expired.py`

### Usage

```bash
# Test what would be deleted (dry run)
python manage.py cleanup_expired --dry-run

# Actually delete expired records
python manage.py cleanup_expired

# Customize timing parameters
python manage.py cleanup_expired --email-used-grace-minutes 5 --email-max-age-minutes 15
```

### Command Options

- `--dry-run`: Show what would be deleted without actually deleting
- `--email-used-grace-minutes N`: Minutes to wait after email verification is used (default: 1)
- `--email-max-age-minutes N`: Maximum age for email verification codes (default: 10)

## Cron Job Setup

### 1. Current Setting (Every 24 hours at 2 AM)
```bash
# Edit crontab
crontab -e

# Add this line:
0 2 * * * cd /Users/wxy/Projects/Web/Tostada && /Users/wxy/miniconda3/envs/ttd/bin/python manage.py cleanup_expired >> /tmp/cleanup.log 2>&1
```

### 2. Alternative Schedules

#### Every 6 hours
```bash
0 */6 * * * cd /Users/wxy/Projects/Web/Tostada && /Users/wxy/miniconda3/envs/ttd/bin/python manage.py cleanup_expired >> /tmp/cleanup.log 2>&1
```

#### Every 12 hours
```bash
0 */12 * * * cd /Users/wxy/Projects/Web/Tostada && /Users/wxy/miniconda3/envs/ttd/bin/python manage.py cleanup_expired >> /tmp/cleanup.log 2>&1
```

#### Every 2 days at 3 AM
```bash
0 3 */2 * * cd /Users/wxy/Projects/Web/Tostada && /Users/wxy/miniconda3/envs/ttd/bin/python manage.py cleanup_expired >> /tmp/cleanup.log 2>&1
```

#### Weekly (Sundays at 1 AM)
```bash
0 1 * * 0 cd /Users/wxy/Projects/Web/Tostada && /Users/wxy/miniconda3/envs/ttd/bin/python manage.py cleanup_expired >> /tmp/cleanup.log 2>&1
```

### 3. Cron Time Format Reference

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7, Sunday=0 or 7)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

### 4. Logging and Monitoring

#### View cleanup logs
```bash
tail -f /tmp/cleanup.log
```

#### Test cron job manually
```bash
cd /Users/wxy/Projects/Web/Tostada && /Users/wxy/miniconda3/envs/ttd/bin/python manage.py cleanup_expired --dry-run
```

## What Gets Cleaned Up

### InvitationCode
- **Expired codes**: Where `created_at + valid_duration_minutes` is in the past
- **Exhausted codes**: Where `remain_uses = 0` and `max_uses > 0`

### EmailVerificationCode  
- **Used codes**: After grace period (default 1 minute after `used_date`)
- **Old codes**: After max age (default 10 minutes after `created_at`)

## Manual Cleanup

```bash
# Run cleanup now
python manage.py cleanup_expired

# Run with custom settings
python manage.py cleanup_expired --email-used-grace-minutes 2 --email-max-age-minutes 20

# Test what would be deleted
python manage.py cleanup_expired --dry-run
```

## Jenkins Job Setup
Jenkins Integration: scripts/jenkins_cleanup_setup.sh

### 1. Current Setting (Every 24 hours at 2 AM)
Jenkins Environment Variables:
TOSTADA_PROJECT_PATH=/opt/tostada
TOSTADA_PYTHON_PATH=/opt/tostada/venv/bin/python
TOSTADA_USER=www-data
TOSTADA_CLEANUP_SCHEDULE="0 2 * * *"
TOSTADA_LOG_FILE=/var/log/tostada-cleanup.log

In your Jenkins pipeline:
stage('Setup Cleanup') {
    steps {
        sh './scripts/jenkins_cleanup_setup.sh'
    }
}

Both scripts:
- ✅ Validate paths and test the command
- ✅ Set up cron job for specified schedule
- ✅ Create log files with proper permissions
- ✅ Generate helper scripts for manual runs
