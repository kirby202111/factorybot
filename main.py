import os

import uvicorn
from dotenv import load_dotenv

from api import create_app

load_dotenv()

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8100")),
        reload=os.getenv("UVICORN_RELOAD", "true").lower() in ("1", "true", "yes"),
    )
