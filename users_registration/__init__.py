import logging
import time

from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FAIRiCube Catalog")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message).1000s",
        level=gunicorn_logger.level,
        handlers=gunicorn_logger.handlers,
    )



import users_registration.views  # noqa
