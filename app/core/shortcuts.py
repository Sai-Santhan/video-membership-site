from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core import config

settings = config.get_settings()

templates = Jinja2Templates(directory=str(settings.templates_dir))


def render(request, template_name, context=None, status_code: int = 200, cookies=None):
    if cookies is None:
        cookies = {}
    if context is None:
        context = {}
    ctx = context.copy()
    ctx.update({"request": request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str, status_code=status_code)
    if len(cookies.keys()) > 0:
        # Set HTTPONLY cookies
        for key, value in cookies.items():
            response.set_cookie(key=key, value=value, httponly=True)
    # To set secure cookies, use the following:
    # response.set_cookie(key=key, value=value, httponly=True, secure=True)
    # To delete cookies, use the following:
    # for key in request.cookies.keys():
    #   response.delete_cookie(key)
    return response
