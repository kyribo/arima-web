# Backend Setup

The backend is written in Go and uses Gin Framework + GORM.

## Setup

1. **Prerequisites**: Ensure you have Go 1.23+ installed.
2. **Dependencies**: Run the following command in this directory to install dependencies:
   ```bash
   go mod tidy
   ```
3. **Database**: Update `.env` with your PostgreSQL credentials.
4. **Run**:
   ```bash
   go run cmd/server/main.go
   ```

## API
- `GET /ping`: Health check.
