# 🔧 Troubleshooting Guide - University Attendance System

## 🚨 "This site can't be reached" Error

If you're getting "This site can't be reached" in your browser, follow these steps:

### Step 1: Check Server Status
```bash
# Check if server is running
ps aux | grep python

# Test server locally
curl http://localhost:8000/
```

### Step 2: Try Different URLs
The server might be accessible through different IP addresses:

**Primary URLs:**
- `http://localhost:8000/`
- `http://127.0.0.1:8000/`

**Alternative URLs (if using containers/Docker):**
- `http://172.30.0.2:8000/`
- `http://172.17.0.1:8000/`

### Step 3: Restart Server
```bash
# Stop existing server
pkill -f "python3 manage.py runserver"

# Start server with proper settings
cd /workspace/Des
python3 manage.py runserver 0.0.0.0:8000
```

### Step 4: Check Network Configuration
```bash
# Get available IP addresses
hostname -I

# Test connectivity
curl -v http://localhost:8000/
```

## 🌐 Environment-Specific Solutions

### Docker/Container Environment
If you're running this in a Docker container:

1. **Use the container IP instead of localhost:**
   ```bash
   # Get container IP
   hostname -I
   ```

2. **Access via container IP:**
   - `http://[CONTAINER_IP]:8000/`
   - Example: `http://172.30.0.2:8000/`

### Local Development
If running locally:

1. **Check firewall settings**
2. **Ensure port 8000 is not blocked**
3. **Try different browsers**

### Cloud/Remote Environment
If running on a cloud server:

1. **Use the public IP address**
2. **Ensure security groups allow port 8000**
3. **Check if the server is bound to 0.0.0.0:8000**

## 🔧 Quick Fix Commands

### Restart Everything
```bash
# Stop all Python processes
pkill -f python

# Navigate to project
cd /workspace/Des

# Start server
python3 manage.py runserver 0.0.0.0:8000
```

### Check Server Logs
```bash
# Start server in foreground to see logs
python3 manage.py runserver 0.0.0.0:8000 --verbosity=2
```

### Test All Access Methods
```bash
# Test localhost
curl http://localhost:8000/

# Test 127.0.0.1
curl http://127.0.0.1:8000/

# Test container IP
curl http://172.30.0.2:8000/
```

## 📱 Available URLs Once Working

- **Home Page:** `http://localhost:8000/`
- **Login Portal:** `http://localhost:8000/login/`
- **Student Login:** `http://localhost:8000/student/login/`
- **Lecturer Login:** `http://localhost:8000/lecturer/login/`
- **Admin Login:** `http://localhost:8000/admin/login/`
- **Student Registration:** `http://localhost:8000/student/register/`

## 🔑 Login Credentials

**Super Admin:**
- Username: `superadmin@university.com`
- Password: `superadmin123`

**Regular Admin:**
- Username: `admin@university.com`
- Password: `admin123`

**Lecturer:**
- Username: `lecturer@university.com`
- Password: `lecturer123`

**Student:**
- Username: `student@university.com`
- Password: `student123`

## 🆘 Still Not Working?

1. **Check if you're in the right environment**
2. **Try accessing from a different browser**
3. **Check if antivirus/firewall is blocking the connection**
4. **Try accessing via IP address instead of localhost**
5. **Ensure the server is actually running and responding**

## 📞 Get Help

If none of the above solutions work, please provide:
1. Your operating system
2. How you're running the application (local/Docker/cloud)
3. The exact error message
4. The URL you're trying to access