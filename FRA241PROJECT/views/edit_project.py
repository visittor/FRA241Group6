from pyramid.httpexceptions import HTTPFound
from sqlalchemy.orm.exc import NoResultFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
    view_defaults,
)

from ..models.Project import Project
from ..models.User import User
from  ..models.Proposal import (Proposal,
                                )
import datetime
import transaction

@view_config(route_name = "select_project_edit",renderer = "../templates/edit_project.pt")
def select_project_edit(request):
    project_list = request.user.own_project
    return dict(project_list = project_list)