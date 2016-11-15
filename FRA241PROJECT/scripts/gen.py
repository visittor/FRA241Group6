#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import transaction
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import RGBColor

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from pyramid.scripts.common import parse_vars

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from ..models.meta import Base
from ..models import (
    get_session
)
from ..models import (Project,
                      User,
                      Equipment,
                      Obligation,
                      Member_table,
                      Member,
                      )

import datetime


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def Get_data(session, project_id):
    return session.query(Project).filter_by(id=project_id).one()


def Gen_Doc(doc_name='Doc.docx'
            , project_name_th=u''
            , project_name_en=u''
            , date_cap=u''
            , where=u''
            , rational=u''
            , purpose_list=list([])
            , profit=u''
            , owner_list=list([])
            , advisor_list=u''
            , member_list=list([])
            , activity_place=u''
            , type_of_activity=u''
            , cost_list=list([])
            , success_criteria=[]
            ):
    document = Document('FRA241PROJECT/static/Archetype_gendoc.docx')

    ######################################################################
    '''Create Style'''
    ######################################################################

    obj_styles = document.styles

    obj_charstyle = obj_styles.add_style('header', WD_STYLE_TYPE.CHARACTER)
    obj_font = obj_charstyle.font
    obj_font.size = Pt(16)
    obj_font.name = 'TH Sarabun New'
    obj_font.bold = True
    obj_font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    obj_charstyle = obj_styles.add_style('content', WD_STYLE_TYPE.CHARACTER)
    obj_font = obj_charstyle.font
    obj_font.size = Pt(16)
    obj_font.name = 'TH Sarabun New'
    obj_font.bold = False
    obj_font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    obj_charstyle = obj_styles.add_style('in table', WD_STYLE_TYPE.CHARACTER)
    obj_font = obj_charstyle.font
    obj_font.size = Pt(14)
    obj_font.name = 'TH Sarabun New'
    obj_font.bold = False
    obj_font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    ######################################################################

    document.add_picture('FRA241PROJECT/static/kmutt.png', width=Inches(0.99), height=Inches(0.99))
    logo = document.paragraphs[-1]
    logo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    proj_name = document.add_heading('', 0)
    proj_name.add_run(u'ข้อเสนอโครงการเข้าร่วม\n', style='header')
    proj_name.add_run(project_name_th + '\n', style='header') if len(project_name_th) != 0 else 0
    proj_name.add_run(project_name_en + '\n', style='header') if len(project_name_en) != 0 else 0
    proj_name.add_run(u'สถาบันวิทยาการหุ่นยนต์ภาคสนาม (ฟีโบ้) มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี\n', style='header')
    proj_name.add_run(u'ระหว่างวันที่ ' + date_cap + '\n', style='header')
    proj_name.add_run(u'ณ ' + where, style='header')
    proj_name.alignment = WD_ALIGN_PARAGRAPH.CENTER

    rationale_head = document.add_paragraph('\n')
    rationale_head.add_run(u'หลักการและเหตุผล', style='header')

    rationale = document.add_paragraph('\t')
    rationale.add_run(rational + '\n', style='content')
    rationale.alignment = WD_ALIGN_PARAGRAPH.THAI_JUSTIFY

    purpose_head = document.add_paragraph()
    purpose_head.add_run(u'วัตถุประสงค์', style='header').alignment = WD_ALIGN_PARAGRAPH.LEFT

    purpose = document.add_paragraph()
    x = 1
    for i in purpose_list:
        purpose.add_run('\t' + str(x) + '. ' + i + '\n', style='content') if len(i) != 0 else purpose.add_run()
        x += 1
    x = 0

    profit_head = document.add_paragraph()
    profit_head.add_run(u'ประโยชน์ที่คาดว่าจะได้รับ', style='header').alignment = WD_ALIGN_PARAGRAPH.LEFT

    profit_content = document.add_paragraph()
    x = 1
    for i in profit:
        profit_content.add_run('\t' + str(x) + '. ' + i + '\n', style='content') if len(
            i) != 0 else profit_content.add_run()
        x += 1
    x = 0

    owner_head = document.add_paragraph()
    owner_head.add_run(u'ผู้รับผิดชอบโครงการ', style='header').alignment = WD_ALIGN_PARAGRAPH.LEFT

    owner = document.add_paragraph()
    if len(owner_list) != 2:
        x = 1
        for i in owner_list:
            owner.add_run('\t' + str(x) + '. ' + i + '\n', style="content") if len(i) != 0 else owner.add_run()
            x += 1
        x = 0
    else:
        owner.add_run('\t' + owner_list[0] + '\n', style="content") if len(owner_list[0]) != 0 else owner.add_run()

    advisor_head = document.add_paragraph()
    advisor_head.add_run(u'อาจารย์ที่ปรึกษาโครงการ', style='header').alignment = WD_ALIGN_PARAGRAPH.LEFT

    advisor = document.add_paragraph()
    # if len(advisor_list) != 1 :
    #     x = 1
    #     for i in advisor_list:
    #         advisor.add_run('\t' + str(x) + '. ' + i + '\n', style="content")if len(i)!= 0 else advisor.add_run()
    #         x += 1
    #     x = 0
    # else:
    advisor.add_run('\t' + advisor_list + '\n', style="content") if len(advisor_list[0]) != 0 else advisor.add_run()

    member_head = document.add_paragraph()
    member_head.add_run(u'ผู้เข้าร่วมโครงการ', style='header').alignment = WD_ALIGN_PARAGRAPH.LEFT

    member = document.add_paragraph()
    x = 1
    for i in member_list:
        member.add_run('\t' + str(x) + '. ' + i + '\n', style="content") if len(i) != 0 else  member.add_run()
        x += 1
    x = 0

    plan_head = document.add_paragraph()
    plan_head.add_run(u'แผนการดำเนินงาน', style='header')

    plan = document.add_paragraph()
    plan.add_run(style='content')

    '''

    "Table"

        Date(details)

    '''

    place_head = document.add_paragraph()
    place_head.add_run(u'สถานที่ดำเนินการ', style='header').alignment = WD_ALIGN_PARAGRAPH.LEFT

    place = document.add_paragraph()
    place.add_run('\t' + activity_place, style='content')
    place.alingment = WD_ALIGN_PARAGRAPH.THAI_JUSTIFY

    activity_type_head = document.add_paragraph()
    activity_type_head.add_run(u'ลักษณะกิจกรรม', style='header').alignment = WD_ALIGN_PARAGRAPH.LEFT

    activity_type = document.add_paragraph()
    activity_type.add_run('\t' + type_of_activity, style='content')

    '''

    "Table"

        Cost

    '''

    print cost_list

    success_pointer_head = document.add_paragraph()
    success_pointer_head.add_run(u'ตัวชี้วัดความสำเร็จของโครงการ', style='header')

    success_pointer = document.add_paragraph()
    if len(success_criteria) != 2:
        x = 1
        for i in success_criteria:
            success_pointer.add_run('\t' + str(x) + '. ' + i + '\n', style="content") if len(
                i) != 0 else success_pointer.add_run()
            x += 1
        x = 0
    else:
        success_pointer.add_run('\t' + success_criteria[0] + '\n', style="content") if len(
            success_criteria[0]) != 0 else success_pointer.add_run()
    # success_pointer.add_run('\t' + success_criteria, style='content')

    sign_area = document.add_paragraph()
    sign_area.add_run(u'ลงชื่อ' + '.......................................................\n', style='content')
    sign_area.add_run((advisor_list.split('\t\t'))[0] + '\n', style="content")
    sign_area.add_run(u'อาจารย์ที่ปรึกษาโครงการ', style="content")
    sign_area.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # document.add_page_break()
    document.save(doc_name)
    print '#########################__Done!__#########################'


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = engine_from_config(settings, prefix='sqlalchemy.')
    Base.metadata.create_all(engine)

    maker = sessionmaker()
    maker.configure(bind=engine)

    session = get_session(maker, transaction.manager)

    all_data = Get_data(session=session, project_id=2)

    cost_list_param = all_data.proposal[0].cost.split(unichr(171)) if all_data.proposal[0].cost is not None else []
    cost_list_parameter = [i.split(unichr(172)) for i in cost_list_param]

    Gen_Doc(doc_name='FRA241PROJECT/static/Gened_DOC/' + 'Competitive_' + str(all_data.id) + '.docx'
            , project_name_th=all_data.title
            , date_cap=u'17 มกราคม – 21 มีนาคม 2559'
            , where=all_data.proposal[0].activity_location
            , rational=all_data.proposal[0].Reason
            , purpose_list=all_data.proposal[0].objective.split(unichr(171))
            , profit=all_data.proposal[0].profit.split(unichr(171))
            , owner_list=all_data.proposal[0].owner_for_proposal.split(unichr(171))
            , advisor_list=all_data.proposal[0].advisor_for_proposal
            , member_list=all_data.proposal[0].member_for_proposal.split(unichr(171))
            , activity_place=all_data.proposal[0].activity_location
            , type_of_activity=all_data.proposal[0].type_of_activity
            , cost_list=cost_list_param
            , success_criteria=all_data.proposal[0].success_criteria.split(unichr(171))
            )
