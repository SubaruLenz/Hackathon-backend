# Docker Setup with Tailscale

This guide explains how to run the FastAPI application using Docker with Tailscale integration.

## Prerequisites

1. **Tailscale Account**: Sign up at [tailscale.com](https://tailscale.com)
2. **Tailscale Auth Key**: Generate a reusable auth key from [Tailscale Admin Console](https://login.tailscale.com/admin/settings/keys)
   - Click "Generate auth key"
   - Check "Reusable" and "Ephemeral" (optional, for containers)
   - Copy the key (starts with `tskey-auth-`)

## Setup Instructions

### 1. Create Environment File

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` and add:
- `TAILSCALE_AUTH_KEY`: Your Tailscale auth key
- Database configuration (choose one option):
  - **Option 1**: Use `DATABASE_URL` (full connection string)
    ```
    DATABASE_URL=postgresql://user:password@host:5432/dbname
    ```
  - **Option 2**: Use individual variables (recommended if you don't have DATABASE_URL)
    ```
    DB_HOST=your-db-host
    DB_PORT=5432
    DB_USER=your-db-user
    DB_PASSWORD=your-db-password
    DB_NAME=your-db-name
    ```

### 2. Build and Start Containers

```bash
docker-compose up -d
```

### 3. Get Your Tailscale IP

Once the containers are running, get the Tailscale IP assigned to your container:

```bash
docker exec budget-tracker-tailscale tailscale ip -4
```

Or check the Tailscale admin console at [login.tailscale.com/admin/machines](https://login.tailscale.com/admin/machines)

### 4. Access Your API

From any device on your Tailscale network:

- **API Base**: `http://<tailscale-ip>:8000`
- **API Docs**: `http://<tailscale-ip>:8000/docs`
- **Health Check**: `http://<tailscale-ip>:8000/health`

## Container Architecture

The setup uses two containers:

1. **tailscale**: Runs Tailscale daemon and creates the VPN connection
2. **api**: Runs your FastAPI application, sharing the network namespace with Tailscale

The API container uses `network_mode: "service:tailscale"` to share the Tailscale network, allowing it to be accessible via the Tailscale IP.

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f tailscale
```

### Stop Services
```bash
docker-compose down
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build
```

### Check Tailscale Status
```bash
docker exec budget-tracker-tailscale tailscale status
```

### Get Tailscale IP
```bash
docker exec budget-tracker-tailscale tailscale ip -4
```

## Troubleshooting

### Run Automated Troubleshooting Script
```bash
./troubleshoot.sh
```

This script will check container status, logs, Tailscale connectivity, and network configuration.

### Container won't start
- Verify your `TAILSCALE_AUTH_KEY` is correct in `.env`
- Check logs: `docker-compose logs tailscale`
- Ensure the auth key is reusable (not one-time use)
- Verify the auth key hasn't expired

### Can't ping or access API from other devices

**Step 1: Verify Tailscale is connected**
```bash
docker exec budget-tracker-tailscale tailscale status
```
You should see your device listed. If not, check the logs:
```bash
docker logs budget-tracker-tailscale
```

**Step 2: Get the Tailscale IP**
```bash
docker exec budget-tracker-tailscale tailscale ip -4
```
If this returns nothing, Tailscale isn't connected. Check:
- Auth key is valid
- Container logs for errors
- Tailscale admin console: https://login.tailscale.com/admin/machines

**Step 3: Verify API is listening**
```bash
docker exec budget-tracker-tailscale netstat -tlnp | grep 8000
# or
docker exec budget-tracker-tailscale ss -tlnp | grep 8000
```

**Step 4: Check from another device on Tailscale network**
- Ensure both devices are logged into the same Tailscale account
- Verify the other device can see your container in `tailscale status`
- Try pinging the Tailscale IP from the other device
- Check firewall rules on both devices

**Step 5: Test API from inside container**
```bash
docker exec budget-tracker-tailscale curl http://localhost:8000/health
```

**Step 6: Common fixes**
- Restart containers: `docker-compose restart`
- Rebuild if needed: `docker-compose up -d --build`
- Check host firewall: `sudo ufw status` (may need to allow Tailscale interface)
- Verify Tailscale subnet routes if using custom routing

### Database Connection Issues
- If using a database in another container, ensure it's on the same Tailscale network
- Update `DB_HOST` to use the Tailscale IP or hostname of the database container
- Verify database credentials in `.env`
- Test database connection from inside the container:
  ```bash
  docker exec budget-tracker-api python -c "from app.database.base import get_database_url; print(get_database_url())"
  ```

## Security Notes

- The Tailscale auth key is stored in `.env` - **never commit this file to git**
- Only devices on your Tailscale network can access the API
- Tailscale encrypts all traffic between devices
- Consider using Tailscale ACLs for additional access control

