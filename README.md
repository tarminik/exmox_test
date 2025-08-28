# Moon Robot Control API

A FastAPI application for controlling a remotely operated robot on the Moon's surface. The robot can move, rotate, and avoid obstacles while tracking all commands and positions in a PostgreSQL database.

## Features

- **Position Tracking**: Robot maintains current coordinates (X, Y) and direction (NORTH, SOUTH, EAST, WEST)
- **Command Execution**: Supports movement and rotation commands:
  - `F` - Move forward one unit
  - `B` - Move backward one unit  
  - `L` - Rotate left 90 degrees
  - `R` - Rotate right 90 degrees
- **Obstacle Avoidance**: Robot stops before hitting known obstacles
- **Database Persistence**: All positions and command executions are stored in PostgreSQL
- **Environment Configuration**: Initial position and obstacles configurable via environment variables

## Requirements

- Python 3.8+
- PostgreSQL database
- Dependencies listed in `requirements.txt`

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd exmox_test
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Copy the provided `.env` file or create your own:
   ```bash
   START_X=4
   START_Y=2
   START_DIRECTION=WEST
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/moonrobot
   OBSTACLES={(1,4), (3,5), (7,4)}
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb moonrobot
   
   # Tables will be created automatically on first run
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## API Endpoints

### Get Current Position
```http
GET /position
```

**Response:**
```json
{
  "x": 4,
  "y": 2,
  "direction": "WEST"
}
```

### Execute Commands
```http
POST /execute
```

**Request:**
```json
{
  "commands": "FLFFFRFLB"
}
```

**Response:**
```json
{
  "initial_position": {
    "x": 4,
    "y": 2,
    "direction": "WEST"
  },
  "final_position": {
    "x": 1,
    "y": 4,
    "direction": "NORTH"
  },
  "obstacle_hit": null,
  "message": "Commands executed successfully"
}
```

**Response (with obstacle):**
```json
{
  "initial_position": {
    "x": 0,
    "y": 4,
    "direction": "EAST"
  },
  "final_position": {
    "x": 0,
    "y": 4,
    "direction": "EAST"
  },
  "obstacle_hit": "(1,4)",
  "message": "Stopped due to obstacle at (1,4)"
}
```

## Testing

The project includes comprehensive tests using pytest with async support.

### Run all tests
```bash
pytest
```

### Run tests with coverage
```bash
pytest --cov=app --cov-report=html
```

### Run specific test files
```bash
# Test position endpoint
pytest tests/test_position_endpoint.py

# Test command execution
pytest tests/test_command_execution.py

# Test obstacle handling
pytest tests/test_obstacle_handling.py

# Test robot service logic
pytest tests/test_robot_service.py

# Test command logic units
pytest tests/test_command_logic.py
```

### Test Categories

- **Unit Tests**: Test individual functions and methods (`test_robot_service.py`, `test_command_logic.py`)
- **Integration Tests**: Test API endpoints with database (`test_position_endpoint.py`, `test_command_execution.py`)
- **Feature Tests**: Test obstacle detection and complex scenarios (`test_obstacle_handling.py`)

## Development

### Project Structure
```
exmox_test/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── robot_service.py     # Core robot logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_position_endpoint.py
│   ├── test_command_execution.py
│   ├── test_obstacle_handling.py
│   ├── test_robot_service.py
│   └── test_command_logic.py
├── alembic/                 # Database migrations
├── requirements.txt
├── .env                     # Environment configuration
└── README.md
```

### Database Schema

**robot_positions**
- `id` - Primary key
- `x`, `y` - Coordinates
- `direction` - Robot facing direction
- `created_at` - Timestamp

**command_executions**
- `id` - Primary key
- `command_string` - Executed commands
- `initial_x`, `initial_y`, `initial_direction` - Starting position
- `final_x`, `final_y`, `final_direction` - Ending position
- `obstacle_hit` - Obstacle coordinates if hit
- `executed_at` - Timestamp

## Configuration

### Environment Variables

- `START_X` - Initial X coordinate (default: 4)
- `START_Y` - Initial Y coordinate (default: 2)  
- `START_DIRECTION` - Initial direction (default: WEST)
- `DATABASE_URL` - PostgreSQL connection string
- `OBSTACLES` - Set of obstacle coordinates in format `{(x1,y1), (x2,y2)}`

### Example Configurations

**Different starting position:**
```bash
START_X=0
START_Y=0
START_DIRECTION=NORTH
```

**Custom obstacles:**
```bash
OBSTACLES={(2,3), (5,7), (1,1)}
```

## API Documentation

When running the application, interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
