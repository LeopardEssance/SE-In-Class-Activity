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
- `GET /integrations/{name}` - Get a specific integration
- `POST /integrations/{name}/activate` - Activate an integration
- `POST /integrations/{name}/deactivate` - Deactivate an integration