# -- coding: utf-8 --
from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from pyramid.renderers import render
from pyramid.response import Response
from ..models.User import User
from ..models.Project import (Project,
                             Comment,)
import transaction

@view_config(route_name = "teacherProject", renderer = "../templates/pageTeacher1.pt",permission = "access")
def teacherProject(request):
    project_list = request.context.project_list
    uncheck_project = []
    checked_project = []
    index = 0 if request.user.role == "Teacher" else 2
    for i in project_list:
        if i.status.split(unichr(171))[index] == "F" :
            uncheck_project.append(i)
        elif i.status.split(unichr(171))[index] == "T" :
            checked_project.append(i)
    return dict(uncheck_project = uncheck_project,
                checked_project = checked_project,
                user = request.user,
                )

@view_config(route_name = "adminProject", renderer = "../templates/Adminpage1.pt",permission = "access")
def adminProject(request):
    project_list = request.context.project_list
    uncheck_project = []
    checked_project = []
    for i in project_list:
        status = i.status.split(unichr(171))
        print "\n\n\n\n\n\n\n\n\n\n",status,"\n\n\n\n\n\n\n\n\n\n"
        if status[1] == "F":
            uncheck_project.append(i)
        elif status[1] == "T":
            checked_project.append(i)
    if "x" in request.params:
        count = 0
        for i in checked_project:
            if str(i.id) in request.params:
                i.is_recommend = "T"
                count += 1
            else:
                i.is_recommend = "F"

        return HTTPFound(location=request.route_url('home'))
    return dict(uncheck_project = uncheck_project,
                checked_project = checked_project,
                user = request.user,
                )

@view_config(route_name = "inspectProject" , permission = "access")
def inspectProject(request):
    project = request.context.project
    comment = request.context.comment
    commentID = comment.id
    if "save" in request.params or "send-comment" in request.params:
        comment.text = request.params.get("message","")
    print "\n\n\n\n\n\n\n\n\n\n","send-comment" in request.params,"\n\n\n\n\n\n\n\n"
    if "send-comment" in request.params:
        status = [i for i in project.status.split(unichr(171))]
        if request.user.role == "Admin":
            status[1] = 'T'
        elif request.user.role == "GOD":
            status[2] = 'T'
        else:
            status[0] = 'T'
        project.status = unichr(171).join(status)
        print "\n\n\n\n\n\n\n\n\n\nfuck yeah\n\n\n\n\n\n\n\n"
        if request.user.role == "Teacher" or request.user.role == "GOD":
            return HTTPFound(location=request.route_url("teacherProject"))
        else:
            return HTTPFound(location=request.route_url("adminProject"))
    comment = request.db_session.query(Comment).filter_by(id = commentID).first()
    if project.type == "camp":
        dict2return = dict(project = project,
                            comment = comment,
                            OJ_ = [i for i in project.proposal.objective.split(unichr(171)) if i!=""],
                         PR_ = [i for i in project.proposal.owner_for_proposal.split(unichr(171)) if i != ''],
                            PM_ = [i for i in project.proposal.member_for_proposal.split(unichr(171)) if i!= ''],
                           Bnf_ = [i for i in project.proposal.profit.split(unichr(171)) if i != ''],
                           BGT_ = [i for i in project.proposal.cost.split(unichr(171)) if i!=''],
                           DB_=[i.split(unichr(172)) for i in project.proposal.delicate_budget.split(unichr(171)) if len(i.split(unichr(172))) == 3 and '' not in i.split(unichr(172))],
                           Sch_=[i.split(unichr(172)) for i in project.proposal.schedule.split(unichr(171)) if len(i.split(unichr(172))) == 2 and '' not in i.split(unichr(172))],
                           )
        split_calibration = project.proposal.activity_comparition.split(",")
        dict_type = {u"ด้านพัฒนาทักษะทางวิชาการและวิชาชีพ": 1, u"ด้านกีฬาและการส่งเสริมสุขภาพ": 2,
                     u"ด้านบำเพ็ญประโยชน์และรักษาสิ่งแวดล้อม": 3, u"ด้านทำนุบำรุงศิลปะและวัฒนธรรม": 4,
                     u"ด้านนันทนาการและการพัฒนาบุคลิกภาพ": 5, u"ด้านความภูมิใจ ความรัก ความผูกพันธ์มหาวิทยาลัย": 6}
        if split_calibration == u"กิจกรรมที่ไม่นับหน่วยชั่วโมง":
            dict2return.update(dict(myradio2="checked"))

        else:
            dict2return.update(dict(myradio1="checked"))
            for i in range(1, len(split_calibration) - 1):
                if split_calibration[i].split(":")[0] in dict_type:
                    if dict_type[split_calibration[i].split(":")[0]] == 1:
                        dict2return.update(dict(Checkbox1=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 2:
                        dict2return.update(dict(Checkbox2=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 3:
                        dict2return.update(dict(Checkbox3=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 4:
                        dict2return.update(dict(Checkbox4=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 5:
                        dict2return.update(dict(Checkbox5=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 6:
                        dict2return.update(dict(Checkbox6=split_calibration[i].split(":")[1]))
        return Response(render("../templates/pageTeacher2formcamp.pt",dict2return,request=request))
    elif project.type == "competitive":
        dict2return = dict(project=project,
                           comment=comment,
                           OJ_=[i for i in project.proposal.objective.split(unichr(171)) if i != ""],
                           project_Bene=[i for i in project.proposal.profit.split(unichr(171)) if i != ''],
                           PR_=[i for i in project.proposal.owner_for_proposal.split(unichr(171)) if i != ''],
                           project_advisor=project.proposal.advisor_for_proposal.split(unichr(172)) if len(project.proposal.advisor_for_proposal.split(unichr(172)))==3 else [u'ยังไม่ใส่',u'ย่อาจารย์ที่ปรึกษาหรือ',u'ใส่์ที่ปรึกษาที่ไม่มีอยู่ในระบบ'],
                           PM_=[i for i in project.proposal.member_for_proposal.split(unichr(171)) if i != ''],
                           DB_=[i.split(unichr(172)) for i in project.proposal.delicate_budget.split(unichr(171)) if
                                len(i.split(unichr(172))) == 3 and '' not in i.split(unichr(172))],
                           project_criteria = [i for i in project.proposal.success_criteria.split(unichr(171)) if i!=''],
                           )
        return Response(render("../templates/pageTeacher2Compettion.pt", dict2return,request=request))
    elif project.type == "volunteer":
        dict2return = dict(project=project,
                           comment = comment,
                           OJ_=[i for i in project.proposal.objective.split(unichr(171)) if i != ""],
                           project_advisor=project.proposal.advisor_for_proposal.split(unichr(172)),
                           PR_=[i for i in project.proposal.owner_for_proposal.split(unichr(171)) if i != ''],
                           PM_=[i for i in project.proposal.member_for_proposal.split(unichr(171)) if i != ''],
                           project_criteria=[i for i in project.proposal.success_criteria.split(unichr(171)) if i!=''],
                           project_Bene=[i for i in project.proposal.profit.split(unichr(171)) if i != ''],
                           DB_=[i.split(unichr(172)) for i in project.proposal.delicate_budget.split(unichr(171)) if
                                len(i.split(unichr(172))) == 3 and '' not in i.split(unichr(172))],
                           Sch_=[i.split(unichr(172)) for i in project.proposal.schedule.split(unichr(171)) if
                                 len(i.split(unichr(172))) == 2 and '' not in i.split(unichr(172))],

                           )
        return Response(render("../templates/pageTeacher2Volunteer.pt", dict2return,request=request))
    else:
        return Response('<body>May be it is a god\'s business, no human kind can access this kind of content.</body>')