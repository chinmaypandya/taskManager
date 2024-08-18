from fastapi import FastAPI
from features.auth.routes.router import auth_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI()

app.include_router(auth_router)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

