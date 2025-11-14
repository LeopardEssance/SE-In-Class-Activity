# Smart Home IoT System

A full-stack IoT system with FastAPI backend and React frontend for managing smart home devices, featuring light control with brightness adjustment and task scheduling.

## Features

- **User Authentication** - Login/logout functionality with session management
- **Device Management** - Add, view, and remove IoT devices (Lights, Thermostats, Security Cameras)
- **Light Control** - Real-time brightness adjustment with interactive slider
- **Task Scheduler** - Schedule device actions with date/time selection
- **Real-time Updates** - Auto-refresh device status every 5 seconds
- **Design Patterns** - Singleton (DeviceFactory), Observer (NotificationService), Factory Pattern

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation using Python type hints
- **Uvicorn** - ASGI server
- **In-memory storage** - No database required

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Modern styling with gradients and animations

## Project Structure

```
SE-In-Class-Activity/
├── app/
│   ├── models/
│   │   ├── user.py              # User authentication model
│   │   ├── device.py            # Device base class & Light subclass
│   │   ├── dashboard.py         # Device management controller
│   │   ├── scheduler.py         # Task scheduling system
│   │   ├── device_factory.py   # Factory pattern for device creation
│   │   └── notification_service.py  # Observer pattern implementation
│   └── main.py                  # FastAPI application & endpoints
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LoginPage.jsx    # User authentication UI
│   │   │   ├── Dashboard.jsx    # Main dashboard view
│   │   │   ├── DeviceCard.jsx   # Reusable device component
│   │   │   ├── LightControl.jsx # Brightness control interface
│   │   │   └── Scheduler.jsx    # Task scheduling UI
│   │   ├── services/
│   │   │   └── api.js           # API client with Axios
│   │   ├── styles/              # Component-specific CSS
│   │   └── App.jsx              # Main React component
│   └── package.json
└── requirements.txt             # Python dependencies
```

## Installation & Setup

### Backend Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the FastAPI server:**
```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install Node dependencies:**
```bash
npm install
```

3. **Run the development server:**
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

### Health Check
- `GET /` - API health status

## Usage Guide

### 1. Login
- Open http://localhost:5173
- Enter credentials (admin / password123)
- Click "Login"

### 2. View Devices
- After login, see the dashboard with 2 default lights
- Devices auto-refresh every 5 seconds

### 3. Control Lights
- Click on any light card
- Use the brightness slider (0-100%)
- Toggle on/off with the button
- Use quick-set buttons (25%, 50%, 75%, 100%)

### 4. Add Devices
- Click "Add Device" button
- Select device type (Light/Thermostat/Security Camera)
- Enter device name
- Click "Add Device"

### 5. Schedule Tasks
- Click "Show Scheduler"
- Click "Schedule New Task"
- Select device and action
- Set date and time
- Click "Schedule Task"

### 6. Delete Devices/Tasks
- Click the × button on any device or task card
- Confirm deletion

## Design Patterns Implemented

### 1. Singleton Pattern
**File:** [app/models/device_factory.py](app/models/device_factory.py)
- Ensures only one DeviceFactory instance exists
- Global point of access via `get_instance()`

### 2. Factory Pattern
**File:** [app/models/device_factory.py](app/models/device_factory.py)
- `create_device()` method creates different device types
- Encapsulates device creation logic

### 3. Observer Pattern
**File:** [app/models/notification_service.py](app/models/notification_service.py)
- NotificationService maintains list of subscribers
- Notifies observers when events occur

### 4. Inheritance
**File:** [app/models/device.py](app/models/device.py)
- `Device` abstract base class
- `Light` extends Device with brightness control
- Proper use of `super()` for initialization

## SOLID Principles

- **Single Responsibility:** Each class has one clear purpose
- **Open/Closed:** Device class is open for extension (Light, Thermostat)
- **Liskov Substitution:** Light can replace Device wherever needed
- **Interface Segregation:** Specific methods for each device type
- **Dependency Inversion:** High-level Dashboard depends on Device abstraction

## Error Handling

- Backend: HTTP status codes with detailed error messages
- Frontend: Try-catch blocks with user-friendly error displays
- Input validation: Pydantic models ensure type safety
- Session validation: All endpoints check authentication

## Development Notes

- No database: Uses in-memory dictionaries and lists
- No middleware: Simple authentication with session IDs
- CORS enabled: Frontend can communicate with backend
- Production-ready code structure with proper type hints
- Comprehensive docstrings for all classes and methods

## Testing the API

Use the Swagger UI at http://localhost:8000/docs to test endpoints interactively:

1. Login via `/auth/login`
2. Copy the `session_id` from response
3. Use session_id in subsequent requests
4. Test device control and scheduling

## Future Enhancements

- Database integration (SQLite/PostgreSQL)
- WebSocket for real-time updates
- User registration
- Device automation rules
- Mobile responsive design improvements
- Unit and integration tests

## License

MIT License - Educational Project