# Linescan Monitoring Service

Simple FastAPI service to monitor camera connectivity using ICMP ping.

## 🚀 Features

-   Read camera IP from `config.ini`
-   Check camera connectivity via ping
-   Lightweight and suitable for edge devices (Jetson, mini PC, etc.)
-   Simple JSON API response
-   No Swagger / ReDoc exposed

------------------------------------------------------------------------

## 📁 Project Structure

. ├── main.py ├── config.ini └── README.md

------------------------------------------------------------------------

## ⚙️ Configuration

Edit `config.ini`:

``` ini
[CAMERA]
ip = 192.168.200.23
```

You can change the IP without modifying the source code.

------------------------------------------------------------------------

## ▶️ Run the Service

### Development Mode

``` bash
python main.py
```

Or:

``` bash
uvicorn main:app --host 0.0.0.0 --port 9001 --reload
```

------------------------------------------------------------------------

### Production Mode (Recommended)

``` bash
uvicorn main:app --host 0.0.0.0 --port 9001 --workers 2
```

------------------------------------------------------------------------

## 🌐 API Endpoints

### 1️⃣ Root Endpoint

GET /

Response:

``` json
{
  "status": true,
  "message": "service status linescan"
}
```

------------------------------------------------------------------------

### 2️⃣ Check Camera Status

GET /linescan

Response Example:

``` json
{
  "camera_ip": "192.168.200.23",
  "status": "OK",
  "message": "Connected"
}
```

If disconnected:

``` json
{
  "camera_ip": "192.168.200.23",
  "status": "NOT OK",
  "message": "Disconnected"
}
```

------------------------------------------------------------------------

## 📦 Requirements

-   Python 3.8+
-   FastAPI
-   Uvicorn

Install dependencies:

``` bash
pip install fastapi uvicorn
```

------------------------------------------------------------------------

## 🔒 Notes

-   ICMP ping must be allowed on the target device
-   If ping is blocked, service will return `NOT OK`
-   For production systems, consider replacing ping with TCP port check

------------------------------------------------------------------------

## 👨‍💻 Author

Ali Mustofa
