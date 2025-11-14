# Smart Home IoT System

A full-stack IoT system with FastAPI backend and React frontend for managing smart home devices, featuring light control with brightness adjustment and task scheduling.

## Features

- **User Authentication** - Login/logout functionality with session management
- **Device Management** - Add, view, and remove IoT devices (Lights, Thermostats, Security Cameras)
- **Light Control** - Real-time brightness adjustment with interactive slider
- **Task Scheduler** - Schedule device actions with date/time selection
- **Notifications** - View system notifications for device events
- **Real-time Updates** - Auto-refresh device status every 5 seconds

## Tech Stack

### Backend
- FastAPI - Modern Python web framework
- Pydantic - Data validation
- Uvicorn - ASGI server

### Frontend
- React 18 - UI framework
- Vite - Build tool and dev server
- Axios - HTTP client

## Installation & Setup

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

The frontend will be available at: **http://localhost:5173**

## Default Credentials

- **Username:** `admin`
- **Password:** `password123`

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Devices
- `GET /devices` - List all devices
- `POST /devices` - Create new device
- `PUT /devices/{id}/light/brightness` - Set light brightness
- `POST /devices/{id}/toggle` - Toggle light on/off
- `DELETE /devices/{id}` - Remove device

### Scheduler
- `GET /schedule` - Get all scheduled tasks
- `POST /schedule` - Create scheduled task
- `DELETE /schedule/{id}` - Cancel task

### Notifications
- `GET /notifications` - Get system notifications

### Integrations
- `GET /integrations` - Get all integrations
- `POST /integrations` - Create integration
- `POST /integrations/{name}/toggle` - Toggle integration

## Usage Guide

1. **Login** - Open http://localhost:5173 and login with default credentials
2. **View Devices** - Dashboard shows all devices with auto-refresh every 5 seconds
3. **Control Lights** - Click on a light card to adjust brightness
4. **Add Devices** - Click "Add Device" to create new devices
5. **Schedule Tasks** - Click "Show Scheduler" to schedule device actions
6. **View Notifications** - Click "Show Notifications" to see system events

## Design Patterns

- **Singleton Pattern** - DeviceFactory ensures single instance
- **Factory Pattern** - DeviceFactory creates different device types
- **Observer Pattern** - NotificationService notifies subscribers of events
- **Inheritance** - Device base class with Light, Thermostat, SecurityCamera subclasses

## Testing

Use the Swagger UI at http://localhost:8000/docs to test endpoints interactively.

Run integration tests:
```bash
python -m pytest -q
```

## License

MIT License - Educational Project
