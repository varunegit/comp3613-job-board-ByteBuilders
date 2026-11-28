from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from . import templates


router = APIRouter(prefix="", tags=["Lifecycle Demo"])


@router.get("/lifecycle", response_class=HTMLResponse, include_in_schema=False)
async def lifecycle_demo(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="lifecycle.html",
        context={},
    )
