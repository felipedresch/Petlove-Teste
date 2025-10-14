import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que registra todas as requisições HTTP no arquivo de log TXT.
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        method = request.method
        path = request.url.path
        status_code = 500
        error_msg = None
    
        try:
            response: Response = await call_next(request)
            status_code = response.status_code
            return response
        
        except Exception as e:
            error_msg = str(e)
            raise
        
        finally:
            duration_ms = (time.time() - start_time) * 1000
            
            try:
                logger.log_request(
                    method=method,
                    path=path,
                    status_code=status_code,
                    duration_ms=duration_ms,
                    error=error_msg)
            except Exception:
                pass

