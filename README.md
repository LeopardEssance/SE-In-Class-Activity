# SE-In-Class-Activity

## Running the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /integrations/` - Create a new integration
- `GET /integrations/` - Get all integrations
- `GET /integrations/stats` - Get integration statistics (connected count, total count)
- `GET /integrations/{name}` - Get a specific integration
- `POST /integrations/{name}/activate` - Activate an integration
- `POST /integrations/{name}/deactivate` - Deactivate an integration
- `POST /integrations/{name}/toggle` - Toggle connection status
- `GET /integrations/{name}/skills` - Get skills for an integration
- `POST /integrations/{name}/skills` - Add a skill to an integration

## Running Tests

Run all integration tests:
```bash
pytest it_test/smart_integration_devices_test.py -v
```

Run tests with coverage:
```bash
pytest it_test/smart_integration_devices_test.py --cov=app --cov-report=html
```