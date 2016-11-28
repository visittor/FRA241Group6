from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from pyramid.response import Response
from ..models import (User,
                      Project,
                      Obligation,
                      )
import os
import transaction
import uuid
import shutil
# fuck
@view_config(route_name = 'select_cost',renderer = '../templates/cost.pt')
def select_cost(request):
    if request.user.role == "Admin":
        project_list = request.db_session.query(Project)
    elif request.user.role == "Student":
        project_list = request.user.own_project
    elif request.user.role == "Teacher":
        project_list = request.user.own_project
    elif request.user.role == "GOD":
        project_list = request.user.own_project
    return dict(project_list = project_list)

@view_config(route_name = 'cost',renderer = '../templates/cost.pt',permission = "access")
def cost(request):
    project = request.context.project
    projectID = project.id
    obligation_list = request.context.obligation_list
    project_list = request.context.project_list
    if "save_cost" in request.params:
        with transaction.manager:
            for i in obligation_list:
                request.db_session.delete(i)
        count_DB = 1
        while True:
            name_inParam_DB1 = "D_B1_"+str(count_DB)
            name_inParam_DB2 = "D_B2_" + str(count_DB)
            name_inParam_DB3 = "D_B3_" + str(count_DB)
            name_inParam_DB4 = "D_B4_" + str(count_DB)
            if name_inParam_DB1 in request.params:
                with transaction.manager:
                    oblig = Obligation(type = "bill",
                                       description = request.params.get(name_inParam_DB1,""),
                                       cost = request.params.get(name_inParam_DB2,""),
                                       status = request.params.get(name_inParam_DB4,""),
                                       project_id = projectID
                                       )
                    if request.params.get(name_inParam_DB4,"") != "T":
                        oblig.status = "F"
                    request.db_session.add(oblig)
                store_file(request,name_inParam_DB3)
            else:
                break
            count_DB += 1
            obligation_list = request.db_session.query(Obligation).filter_by(project_id = projectID).filter_by(type = "bill")
            return dict(project=project,
                        obligation_list=obligation_list,
                        project_list=project_list,
                        )

    return dict(project = project,
                obligation_list = obligation_list,
                project_list = project_list,
                )

@view_config(route_name='bar')
def show_current_route_pattern(request):
    introspector = request.registry.introspector
    route_name = request.matched_route.name
    route_intr = introspector.get('routes', route_name)
    return Response(str(route_intr['pattern']))

def store_file(request,paramsName):
    filename = request.POST[paramsName].filename

    input_file = request.POST[paramsName].file
    file_path = os.path.join(request.static_url('FRA241PROJECT:static/'), '%s.mp3' % uuid.uuid4())
    temp_file_path = file_path + '~'
    input_file.seek(0)
    with open(temp_file_path, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)

    os.rename(temp_file_path, file_path)