from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from ..models import User
from ..models import Project
from ..scripts.extractDocxFile import get_docx_text

@view_config(route_name = "teacherProject", renderer = "../templates/pageTeacher1.pt",permission = "access")
def teacherProject(request):
    project_list = request.context.project_list
    uncheck_project = []
    checked_project = []
    for i in project_list:
        if i.status.split(unichr(171))[0] == "F":
            uncheck_project.append(i)
        elif i.status.split(unichr(171))[0] == "T":
            checked_project.append(i)
    return dict(uncheck_project = uncheck_project,
                checked_project = checked_project,
                user = request.user,
                )

@view_config(route_name = "inspectProject" , renderer = "../templates/pageTeacher2.pt",permission = "access")
def inspectProject(request):
    project = request.context.project
    # with open(request.static_url("FRA241PROJECT:static/docx/ScriptEng.docx"),"r") as text:
    #     pass
    # text = get_docx_text(request.static_url("FRA241PROJECT:static/docx/ScriptEng.docx"))
    return dict(project = project,
                # text = text,
                )