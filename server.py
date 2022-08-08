import uvicorn
import os

if __name__ == '__main__':
    os.system('docker-compose up -d')
    uvicorn.run('src.main:app', port=5000, reload=True)
