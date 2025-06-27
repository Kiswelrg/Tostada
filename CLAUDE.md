# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tostada is a Discord-like chat application built with Django backend and Vue.js frontend. It features real-time messaging, channels, servers, file attachments, and a custom tool system.

## Architecture

### Backend (Django)
- **Main project**: `/Tostada/` - Django project configuration
- **Apps**:
  - `account/` - User authentication and profiles with custom AUser model
  - `message/` - Chat messages with DirectMessage and ChatMessage models
  - `tool/` - Server/channel management with complex permission system
  - `attachment/` - File upload handling
  - `media/` - Media file management
  - `project/` - Global settings and snowflake ID generation

### Frontend (Vue.js)
- **Location**: `/ttd/` directory
- **Framework**: Vue 3 with Vite build system
- **Styling**: Tailwind CSS with SCSS
- **Icons**: FontAwesome + custom SVG system
- **State**: Local state management with session utilities

### Key Features
- **Real-time messaging**: Uses Django Channels with Redis for WebSocket support
- **Snowflake IDs**: Custom ID generation system for all entities
- **Permission system**: Complex role-based permissions (see `tool/models.py` AuthBits)
- **File handling**: Separate attachment and media systems with automatic scaling
- **Tool system**: Extensible tool architecture in `/tool/servers/`

## Development Commands

### Backend (Django)
```bash
# Start development server
python manage.py runserver 127.0.0.1:8001

# Run from project root
./run.sh

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Install dependencies
pip install -r envs/requirements.txt
```

### Frontend (Vue.js)
```bash
# Navigate to frontend directory
cd ttd/

# Development server
npm run dev

# Build for production
npm run build

# Mock API server
npm run backend

# Icon utilities
npm run convert-svg       # Convert single SVG to Vue component
npm run convert-all       # Convert all SVGs to Vue components
npm run unregister-icon   # Remove icon registration
```

## Key Configuration

### Backend Settings
- **Database**: SQLite (development)
- **Redis**: Required for WebSocket channels (127.0.0.1:6379)
- **Static files**: Served from `/ttd/dist/static/` in production
- **Media uploads**: Stored in `/upload/media/` and `/upload/attachment/`
- **Time zone**: Asia/Chongqing

### Frontend Configuration
- **Dev server**: Proxies `/api` requests to Django backend
- **Build output**: `/ttd/dist/`
- **Environment variables**: Use `.env` files for VITE_BACKEND_URL

## Database Models

### Core Models
- **AUser**: Extends Django User with avatar, cover images, and snowflake IDs
- **ChatMessage**: Channel messages with JSON content, mentions, and tool integration
- **DirectMessage**: Private messages between users
- **Server**: Discord-like servers with roles and permissions
- **ChannelOfChat**: Text channels within servers
- **CategoryInServer**: Channel organization

### Important Relationships
- Messages use snowflake IDs as primary keys
- Complex permission system with bitwise operations
- File attachments linked to messages via foreign keys
- User roles and permissions are server-specific

## File Structure Conventions

### Backend
- Models define database structure with custom managers
- Views handle API endpoints (mostly function-based)
- URLs use namespaced patterns with API prefix support
- Utilities in `/UtilGlobal/` for shared functionality

### Frontend
- Components in `/src/components/` organized by feature
- Views/pages in `/src/i/` for main application
- Utilities in `/src/util/` for shared functions
- Assets organized by component type in `/src/assets/`

## Testing

- Django tests in each app's `tests.py`
- No specific test runner configured - use standard Django testing
- Frontend testing setup not configured

## Dependencies

### Backend Key Packages
- Django 5.0.7 with channels for WebSocket support
- channels-redis for Redis integration
- Pillow for image processing
- django-cors-headers for CORS handling

### Frontend Key Packages
- Vue 3 with Vue Router
- Vite for build tooling
- Tailwind CSS for styling
- FontAwesome for icons
- VueUse for composition utilities

## Development Notes

- WebSocket connections require Redis server running
- File uploads are handled separately for attachments vs media
- Custom snowflake ID system used throughout instead of auto-incrementing IDs
- Permission system uses bitwise operations for role management
- Frontend uses extensive proxy configuration for API calls during development