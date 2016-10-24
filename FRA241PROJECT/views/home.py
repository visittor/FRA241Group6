from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

# @view_config(route_name = 'home')
# def home(request):
#     return HTTPFound(location=request.route_url('login'))