from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from ..models import User,Project

@view_config(route_name = 'home', renderer = '../templates/hometeacher.pt')
def home(request):
    if request.user is None:
        return HTTPFound(location=request.route_url('login'))
    user = request.user
    project_list = request.user.own_project
    project_recommend = request.db_session.query(Project).filter_by(is_recommend = "T")
    return dict(user= user,
                project_list = project_list,
                project_recommend=project_recommend,
                )

@view_config(route_name = 'test')
def test(request):
    session = request.db_session
    """do something"""""
    return dict(i = 'i')