from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from ..models import User,Project

@view_config(route_name = "checkStatus", renderer = "../templates/checkstatus.pt",permission = "access")
def checkStatus(request):
    context = request.context
    return dict(status = context.status,
                dictComment =context.dictComment,
                )