from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core import config

settings = config.get_settings()

templates = Jinja2Templates(directory=str(settings.templates_dir))


def render(request, template_name, context=None, status_code: int = 200):
    if context is None:
        context = {}
    ctx = context.copy()
    ctx.update({"request": request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str, status_code=status_code)
    # Set HTTPONLY cookies
    return response
