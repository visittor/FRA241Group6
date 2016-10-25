from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from ..models import User

@view_config(route_name = 'home', renderer = '../templates/index/indexby92.pt')
def home(request):
    if request.user is None:
        return HTTPFound(location=request.route_url('login'))

    user = request.user

    return dict(user= user)
