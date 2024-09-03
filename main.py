from fastapi import FastAPI
from middlewares.limiter import limiter
from features.auth.routes.router import auth_router
from features.teams.routes.router import team_router
from features.requests.routes.router import request_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from errors.exceptions import RequestException
from errors.handler import request_exception_handler

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(RequestException, request_exception_handler)

app.include_router(auth_router)
app.include_router(team_router)
app.include_router(request_router)


