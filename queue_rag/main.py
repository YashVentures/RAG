from .server import app
import uvicorn


def main():
    uvicorn.run(app, port = 8000, host = "127.0.0.1")

main()  