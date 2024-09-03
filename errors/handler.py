from fastapi import Request
from fastapi.responses import JSONResponse

def request_exception_handler(request: Request, exc):
    return JSONResponse(
        content={
            'error':exc.message,
            'hint': exc.hint
        },
        status_code=exc.status_code
    )