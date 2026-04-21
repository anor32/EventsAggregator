from .enpoints import  router
from fastapi import (
    FastAPI)
import uvicorn
import os
import sys
import json
import  logging
from typing   import   Dict,Any,Optional
app = FastAPI()
app.include_router(router)