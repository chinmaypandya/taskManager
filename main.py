from fastapi import FastAPI
from features.auth.routes.router import auth_router
from features.teams.routes.router import team_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth_router)
app.include_router(team_router)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

