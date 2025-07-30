# 🐳 DOCKER ACCESS GUIDE - Fix Port Exposure

## 🚨 **ISSUE IDENTIFIED: Port Not Exposed**

You're running in Docker and the port 8000 is not exposed to your host machine. The server is running inside the container but not accessible from outside.

---

## 🔧 **SOLUTION: Expose the Port**

### **Option 1: If you can restart the Docker container**

Run your Docker container with port mapping:

```bash
# Stop current container
docker stop your-container-name

# Run with port mapping
docker run -p 8000:8000 your-image-name

# Or if using docker-compose, add to docker-compose.yml:
# ports:
#   - "8000:8000"
```

### **Option 2: If you can't restart the container**

You need to expose the port from inside the container:

```bash
# Connect to your running container
docker exec -it your-container-name bash

# Then run the server with proper binding
python3 manage.py runserver 0.0.0.0:8000
```

### **Option 3: Use Docker port forwarding**

```bash
# Forward port 8000 from container to host
docker port your-container-name 8000
```

---

## 🌐 **ACCESS URLs (after fixing port exposure)**

Once the port is properly exposed, use:

- `http://localhost:8000/`
- `http://127.0.0.1:8000/`

**NOT the container IPs (172.17.0.1, 172.30.0.2) - those are internal container IPs**

---

## 🔍 **VERIFY PORT EXPOSURE**

Check if port 8000 is exposed:

```bash
# From your host machine (not inside container)
netstat -tlnp | grep 8000
# or
ss -tlnp | grep 8000
```

You should see something like:
```
tcp        0      0 0.0.0.0:8000           0.0.0.0:*               LISTEN
```

---

## 🚀 **QUICK FIX COMMANDS**

### **From your host machine:**

1. **Find your container:**
   ```bash
   docker ps
   ```

2. **Expose the port:**
   ```bash
   docker run -p 8000:8000 your-image-name
   ```

3. **Or restart with port mapping:**
   ```bash
   docker stop your-container
   docker run -p 8000:8000 your-image-name
   ```

---

## 📱 **TEST AFTER FIXING**

Once port is exposed, test:

- `http://localhost:8000/`
- `http://127.0.0.1:8000/`

**Login Credentials:**
- **Super Admin:** `superadmin@university.com` / `superadmin123`
- **Regular Admin:** `admin@university.com` / `admin123`
- **Lecturer:** `lecturer@university.com` / `lecturer123`
- **Student:** `student@university.com` / `student123`

---

## 🆘 **NEED HELP?**

Tell me:
1. How you started the Docker container
2. The output of `docker ps`
3. Whether you can restart the container

**The server is running fine inside the container - we just need to expose the port!** 🎯