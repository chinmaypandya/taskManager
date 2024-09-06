from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import RequestException

def request_exception_handler(request: Request, exc: RequestException):
    return JSONResponse(
        content={
            'error':exc.message,
            'hint': exc.hint
        },
        status_code=exc.status_code
    )

def server_exception_handler(request: Request, exc: Exception):
    message = ''.join(*exc.args)
    return JSONResponse(
        content={
            'error': message
        },
        status_code=500
    )