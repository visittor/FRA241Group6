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

from ..models import ( Project, User)
from  ..models.Proposal import (Proposal,
                                Objective,
                                Cost,
                                Previouse_result,
                                Owner_for_proposal,
                                Member_for_proposal,
                                Delicate_budget,
                                Schedule,
                                )
import datetime
import transaction

@view_defaults(route_name='proposal')
class Project_view():

    def __init__(self,request):
        self.request = request

    @view_config(route_name = 'addProject',renderer = "../templates/index.pt")
    def add_project(self,request):
        if self.request.params["project_title"] == '':
            return dict(alert='No project title',current_title = '')
        elif "volunteer-button" in self.request.params:
            return dict(flag = 'volunteer',current_title = self.request.params["project_title"])
        elif "competitive-button" in self.request.params:
            return dict(flag = 'competitive',current_title = self.request.params["project_title"])
        elif "camp-button" in self.request.params:
            return dict(flag = 'camp',current_title = self.request.params["project_title"])

        if "volunteer" in self.request.params:
            with transaction.manager:
                session = self.request.db_session
                project = Project(title=self.request.params["project_title"], type="volunteer")
                session.add(project)
            user = self.request.user
            project_list = self.request.db_session.query(Project).filter_by(title=self.request.params["project_title"]).filter_by(owner_id=user.id).order_by(Project.id)
            project = project_list[-1]
            headers = remember(self.request, user.id, project_id=project.id)
            return HTTPFound(location = self.request.route_url('proposal'),headers=headers)
        elif "competitive" in self.request.params:
            with transaction.manager:
                session = self.request.db_session
                project = Project(title = self.request.params["project_title"],type = "competitive")
                session.add(project)
            user = self.request.user
            project_list = self.request.db_session.query(Project).filter_by(title=self.request.params["project_title"]).filter_by(owner_id=user.id).order_by(Project.id)
            project = project_list[-1]
            headers = remember(self.request, user.id, project_id=project.id)
            return HTTPFound(location=self.request.route_url('proposal'), headers=headers)
        elif "camp" in self.request.params:
            with transaction.manager:
                session = self.request.db_session
                project = Project(title = self.request.paramsp["project_title"],type = "camp")
                session.add(project)
            user = self.request.user
            project_list = self.request.db_session.query(Project).filter_by(title=self.request.params["project_title"]).filter_by(owner_id=user.id).order_by(Project.id)
            project = project_list[-1]
            headers = remember(self.request, user.id, project_id=project.id)
            return HTTPFound(location=self.request.route_url('proposal'),headers=headers,type_project=project.type )

        return dict( current_title='')

    @view_config(route_name = 'proposal',match_param="type_project=formChamp",renderer = "../template/formChamp.pt")
    def form_champ(self,request):
        if "P_N" in self.request.params:
            project_title = self.request.params["P_N"]
        else:
            project_title = ''

        if "Year" in self.request.params:
            project_year = self.request.params["Year"]
        else:
            project_year = ''

        if "Date-start" in self.request.params:
            raw_date = self.request.params["Date-start"]
            if "/" not in raw_date:
                raw_date_start = 'Invalid format'
            split_date = raw_date_start.splite["/"]
            if len(split_date) != 3:
                raw_date_start = 'Invalid format'
            for i in split_date:
                if i.isdigit() == False:
                    raw_date_start = 'Invalid format'
                    break

            if raw_date_start != 'Invalid format':
                start_date = datetime.date(split_date[2],split_date[1],split_date[0])

            else:
                start_date = ''
        else:
            start_date = ''

        if "Date-finish" in self.request.params:
            raw_date_finish = self.request.params["Date-finsish"]
            if "/" not in raw_date_finish:
                raw_date_finish = 'Invalid format'
            split_finish_date = raw_date_finish.splite["/"]
            if len(split_finish_date) != 3:
                raw_date_finish = 'Invalid format'
            for i in split_finish_date:
                if i.isdigit() == False:
                    raw_date_finish = 'Invalid format'
                    break

            if raw_date_finish != 'Invalid format':
                finish_date = datetime.date(split_finish_date[2], split_finish_date[1], split_finish_date[0])

            else:
                finish_date = ''
        else:
            finish_date = ''

        if "P_P" in self.request.params:
            project_activity_location = self.request.params["P_P"]
        else:
            project_activity_location = ''

        if "Reason_Project" in self.request.params:
            project_reason = self.request.params["Reason_Project"]
        else:
            project_reason = ''

        count_OJ = 1
        list_OJ = []
        while True:
            name_inParam = "OJ"+str(count_OJ)
            if name_inParam in self.request.params:
                list_OJ.append(self.request.params[name_inParam])

            else:
                break
            count_OJ+=1

        if "Calibration" in self.request.params:
            project_Calibration = self.request.params["Calibration"]
        else:
            project_Calibration = ''

        count_P_R = 1
        list_PR = []
        while True:
            name_PR_inParam = "P_R"+str(count_P_R)
            if name_PR_inParam in self.request.params:
                list_PR.append(self.request.params[name_PR_inParam])

            else:
                break
            count_P_R+=1

        if "Duration" in self.request.params:
            project_duration = self.request.params["Duration"]
        else:
            project_duration = ''

        count_P_M = 1
        list_PM = []
        while True:
            name_PM_inParam = "P_M"+str(count_P_M)
            if name_PM_inParam in self.request.params:
                list_PM.append(self.request.params[name_PM_inParam])
            else:
                break
            count_P_M+=1

        if "evaluation" in self.request.params:
            project_evaluation = self.request.params["evaluation"]
        else:
            project_evaluation = ''

        if "Benefits" in self.request.params:
            project_profit = self.request.params["Benefits"]
        else:
            project_profit = ''

        count_BGT = 1
        list_BGT = []
        while True:
            name_BGT_inParam = "BGT"+str(count_BGT)
            if name_BGT_inParam in self.request.params:
                list_BGT.append(self.request.params[name_BGT_inParam])
            else:
                break
            count_BGT+=1

        count_DB = 1
        list_DB = []
        while True:
            name_DB1_inParam = "D_B1_"+str(count_DB)
            name_DB2_inParam = "D_B2_"+str(count_DB)
            name_DB3_inParam = "D_B3_"+str(count_DB)
            if name_DB1_inParam in self.request.params and name_DB2_inParam in self.request.params and name_DB3_inParam in self.request.params:
                list_DB.append([self.request.params[name_DB1_inParam],self.request.params[name_DB2_inParam],self.request.params[name_DB3_inParam]])
            else:
                break
            count_DB+=1

        count_schedule = 1
        list_schedule = []
        while True:
            name_schedule1_inParam = "schedule1_"+str(count_schedule)
            name_schedule2_inParam = "schedule2_" + str(count_schedule)
            if name_schedule1_inParam in self.request.params and name_schedule1_inParam in self.request.params:
                list_schedule.append([self.request.params[name_schedule1_inParam],self.request.params[name_schedule2_inParam]])
            else:
                break
            count_schedule+=1

        if "save_proposal" in self.request.params:
            try:
                proposal = request.db_session.query(Proposal).filter_by(parent_id=self.request.headers["project_id"]).first()
                if proposal is None:
                    is_exist = False
            except NoResultFound:
                return HTTPFound(location=self.request.route_url("addProject"))
            if is_exist == False:
                with transaction.manager:

                    proposal = Proposal(year = project_year,
                                        activity_location=project_activity_location,
                                        Reason = project_reason,
                                        activity_comparition = project_Calibration,
                                        duration = project_duration,
                                        evaluation_index = project_evaluation,
                                        profit = project_profit,
                                        )
                    project = request.db_session.query(Project).filter_by(id = self.request.headers["project_id"]).first()
                    if type(start_date) != str:
                        project.start_date = start_date
                    if type(finish_date) != str:
                        project.finish_date = finish_date
                    proposal.parent_project = project
                    for i in list_OJ:
                        obj = Objective(text = i)
                        proposal.objective.append(obj)
                    for i in list_PR:
                        PR = Owner_for_proposal(text = i)
                        proposal.owner_for_proposal.append(PR)
                    for i in list_PM:
                        PM = Member_for_proposal(text = i)
                        proposal.member_for_proposal.append(PM)
                    for i in list_BGT:
                        BGT = Cost(text = i)
                        proposal.cost.append(BGT)
                    for i in list_DB:
                        DB = Delicate_budget(order = i[0],descrip = i[1], value = i[2])
                        proposal.delicate_budget.append(DB)
                    for i in list_schedule:
                        sch = Schedule(time=i[0],descrip = i[1])
                        proposal.schedule.append(sch)

                    self.request.db_session.add(proposal)

        return dict(project_title = project_title,
                    project_year = project_year,
                    project_activity_location = project_activity_location,
                    project_reason = project_reason,
                    project_Calibration = project_Calibration,
                    project_duration = project_duration,
                    project_evaluation = project_evaluation,
                    project_profit = project_profit,
                    start_date = self.request.params["Date-start"],
                    finish_date = self.request.params["Date-finish"],
                    OJ = list_OJ,
                    PR = list_PR,
                    PM = list_PM,
                    BGT = list_BGT,
                    DB = list_DB,
                    Sch = list_schedule,
                   )







