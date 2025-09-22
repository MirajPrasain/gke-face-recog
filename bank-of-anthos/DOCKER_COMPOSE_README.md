# Bank of Anthos - Docker Compose Setup

This Docker Compose configuration allows you to run Bank of Anthos locally for development and testing purposes.

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB of available RAM
- Ports 8081-8086 and 5432-5433 available on your system

## Quick Start

1. **Clean up any existing containers:**
   ```bash
   docker compose down -v
   ```

2. **Start all services:**
   ```bash
   docker compose up -d
   ```

3. **Check that all services are running:**
   ```bash
   docker ps
   ```

4. **Access the application:**
   - Frontend: http://localhost:8086
   - User Service: http://localhost:8081
   - Contacts Service: http://localhost:8082
   - Ledger Writer: http://localhost:8083
   - Balance Reader: http://localhost:8084
   - Transaction History: http://localhost:8085

## Services

The following services are included:

- **frontend** (Python) - Web interface on port 8086
- **userservice** (Python) - User authentication service on port 8081
- **contacts** (Python) - Contact management service on port 8082
- **ledgerwriter** (Java) - Transaction processing service on port 8083
- **balancereader** (Java) - Balance reading service on port 8084
- **transactionhistory** (Java) - Transaction history service on port 8085
- **accounts-db** (PostgreSQL) - User accounts database on port 5432
- **ledger-db** (PostgreSQL) - Transaction ledger database on port 5433

## Demo Login

The application comes with demo data enabled. You can log in using:
- **Username:** testuser
- **Password:** bankofanthos

## Troubleshooting

### Java Services Not Starting
The Java services (ledgerwriter, balancereader, transactionhistory) may fail to start due to Google Cloud dependencies. This is expected in a local development environment without proper Google Cloud credentials.

### Port Conflicts
If you encounter port conflicts, you can modify the port mappings in the `docker-compose.yml` file.

### Platform Warnings
You may see warnings about platform mismatches (linux/amd64 vs linux/arm64). This is normal and shouldn't affect functionality.

## Stopping the Services

To stop all services:
```bash
docker compose down
```

To stop and remove all data volumes:
```bash
docker compose down -v
```

## Development Notes

- Tracing and metrics are disabled for local development to avoid Google Cloud dependencies
- The JWT keys are extracted from the Kubernetes secrets for authentication
- All services use the same network for inter-service communication
- Database data persists in Docker volumes
