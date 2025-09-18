from app import create_app
from app.config import Config

if __name__ == "__main__":
    config = Config.from_env()
    app = create_app(config)
    app.run(host="0.0.0.0", port=5000, debug=False)
