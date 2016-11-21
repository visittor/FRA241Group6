# from .models.Project import Project
# from .models.User import User
# from  .models.Proposal import (Proposal,
#                                 )
# from sqlalchemy.orm.exc import NoResultFound
# from pyramid.httpexceptions import (
#     HTTPNotFound,
#     HTTPFound,
# )
# from pyramid.security import (
#     Allow,
#     Everyone,
# )
from views.view_factory import *
# import datetime
# import transaction
# import time

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('test','/test')
    config.add_route('login','/login')
    config.add_route('logout','/logout')
    config.add_route('plusButton','/plusButton')
    config.add_route('addProject','/add_project')
    config.add_route('proposal','/add_proposal/{project_id}/{type_project}',factory=proposal_factory)
    config.add_route('teacherProject','/teacherProject',factory = teacher_project_factory)
    config.add_route('inspectProject','/teacherProject/{project_id}',factory = inspect_foctory)
    config.add_route('myProject','/myProject')

# def proposal_factory(request):
#     try:
#         project = request.db_session.query(Project).filter_by(id = request.matchdict["project_id"]).first()
#     except NoResultFound:
#         return HTTPFound(location=request.route_url("addProject"))
#     projectId = project.id
#     if project.proposal is None:
#         with transaction.manager:
#             proposal = Proposal( Reason = '',
#                                 objective='',
#                                 owner_for_proposal = '',
#                                 member_for_proposal = '',
#                                 advisor_for_proposal = '',
#                                 evaluation_index = '',
#                                 profit = '',
#                                 type_of_activity = '',
#                                 cost = '',
#                                 delicate_budget = '',
#                                 schedule = '',
#                                 previouse_result = '',
#                                 activity_comparition = '',
#                                 )
#             proposal.parent_id = projectId
#             request.db_session.add(proposal)
#     project.proposal = request.db_session.query(Proposal).filter_by(parent_id = projectId).first()
#     return AddProposal(project)
#
#
#
# class AddProposal(object):
#     def __init__(self,project):
#         self.project = project
#         print "\n\n\n\n\n\n\nin class",self.project.owner_id,"\n\n\n\n\n\n\n\n"
#
#     def __acl__(self):
#         a = [
#             (Allow,Everyone,'nor_access'),
#             (Allow,'role:Student','not_access'),
#             (Allow,'role:Teach','not_access'),
#             (Allow,'role:GOD','not_access'),
#             (Allow,str(self.project.owner_id),'edit'),
#         ]
#         print "\n\n\n\n\n\n\n\nacl",a,"\n\n\n\n\n\n\n"
#         return a
# def teacher_project_factory(request):
#     with transaction.manager:
#         project_list = request.user.advisee_project
#         for i in project_list:
#             if i.status is None or len(i.status.split(unichr(171))) == 0:
#                 i.status = 'F'+unichr(171)+'F'+unichr(171)+'F'+unichr(171)+'F'+unichr(171)
#     project_list = request.user.advisee_project
#     id = request.user.id
#     return TeacherProject(project_list,id)
#
# class TeacherProject(object):
#     def __init__(self,project_list,id):
#         self.project_list = project_list
#         self.id = id
#
#     def __acl__(self):
#         return [
#             (Allow,Everyone,'deny')
#             (Allow,'role:Teacher','deny'),
#             (Allow,'role:GOD','deny'),
#             (Allow,str(self.id),'access')
#         ]



