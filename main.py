import subprocess
import uvicorn
import configparser
import re
from fastapi import FastAPI, HTTPException
from pathlib import Path

app = FastAPI(docs_url=None, redoc_url=None)

CONFIG_PATH = Path(__file__).parent / "config.ini"


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    try:
        camera_ip = config["CAMERA"]["ip"]
        timeout = config["CAMERA"].getint("timeout", fallback=3)  # default 3 sec
        return camera_ip, timeout
    except KeyError:
        return None, None


def ping_host(ip: str, timeout: int = 3):
    """
    Return:
        status (str)
        message (str)
        latency (float or None)
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            capture_output=True,
            text=True,
            timeout=timeout + 1  # safety timeout
        )

        if result.returncode == 0:
            # Flexible regex (support integer or float)
            match = re.search(r'time=(\d+\.?\d*)', result.stdout)
            latency = float(match.group(1)) if match else None
            return "OK", "Connected", latency

        else:
            return "NOT OK", "Host Unreachable", None

    except subprocess.TimeoutExpired:
        return "NOT OK", "Ping Timeout", None

    except Exception as e:
        return "ERROR", f"Ping Execution Failed: {str(e)}", None


@app.get('/')
def read_root():
    return {
        "status": True,
        "message": "service status linescan"
    }


@app.get('/linescan')
def status_linescan():
    camera_ip, timeout = load_config()

    if not camera_ip:
        raise HTTPException(
            status_code=500,
            detail="Camera IP not found in config.ini"
        )

    status, message, latency = ping_host(camera_ip, timeout)

    return {
        "camera_ip": camera_ip,
        "timeout_seconds": timeout,
        "status": status,
        "message": message,
        "latency_ms": latency
    }


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9001,
        reload=True,
        workers=1,
    )
