import subprocess
import uvicorn
import configparser
from fastapi import FastAPI, HTTPException
from pathlib import Path

app = FastAPI(docs_url=None, redoc_url=None)

CONFIG_PATH = Path(__file__).parent / "config.ini"


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    try:
        camera_ip = config["CAMERA"]["ip"]
        return camera_ip
    except KeyError:
        return None


@app.get('/')
def read_root():
    return {
        'status': True,
        'message': 'service status linescan'
    }


@app.get('/linescan')
def status_linescan():
    camera_ip = load_config()

    if not camera_ip:
        raise HTTPException(
            status_code=500,
            detail="Camera IP not found in config.ini"
        )

    try:
        output = subprocess.run(
            ['ping', '-c', '1', '-W', '1', camera_ip],
            capture_output=True,
            text=True
        )

        status = 'OK' if output.returncode == 0 else 'NOT OK'

        return {
            'camera_ip': camera_ip,
            'status': status,
            'message': 'Connected' if status == 'OK' else 'Disconnected'
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail='Failed ping camera'
        )


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=9001,
        reload=True,
        workers=1,
    )
