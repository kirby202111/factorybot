import os

import uvicorn
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    uvicorn.run(
        "factorybot.app:create_app",
        factory=True,
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", "8100")),
        reload=os.getenv("UVICORN_RELOAD", "true").lower() in ("1", "true", "yes"),
    )


if __name__ == "__main__":
    main()
