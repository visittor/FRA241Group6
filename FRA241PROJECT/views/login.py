from pyramid.httpexceptions import HTTPFound
from sqlalchemy.orm.exc import NoResultFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import User


@view_config(route_name='login', renderer='../templates/login.pt')
def login(request):
    # next_url = request.params.get('next', request.referrer)
    next_url = request.route_url('home')
    # if not next_url:
    #     next_url = request.route_url('home')
    print '\n\n\n\n\n####################################################\n\n\n\n\n\n'
    message = 'what'
    message2 = ''
    login = 'Username...'
    form_user_name = 'User name...'
    form_student_id = 'Student id...'
    form_pass_word = 'password...'
    form_first_name = 'First name...'
    form_last_name = 'Last name...'
    form_email = 'Email...'

    if 'form.submitted' in request.params:
        login = request.params['form-username']
        password = request.params['form-password']
        try:
            user = request.db_session.query(User).filter_by(user_id=login).first()
            if user is not None and user.check_password(password):
                headers = remember(request, user.id)
                message = 'grat'
                print "\n\n\n\n\n grat \n\n\n\n\n\n",next_url,'\n\n\n\n\n\n'
                return HTTPFound(location=next_url, headers=headers)
            message = 'Failed login'
        except NoResultFound:
            message = 'Failed login'

    elif 'form.signup' in request.params:
        form_user_name = request.params.get("form-user-name")
        form_student_id = request.params.get("form-student-id")
        form_pass_word = request.params.get("form-pass-word")
        form_first_name = request.params.get("form-first-name")
        form_last_name = request.params.get("form-last-name")
        form_email = request.params.get("form-email")
        if form_user_name is None or form_user_name == '':
            message2 = 'User name Invalid'
        elif form_student_id is None or form_student_id == '':
            message2 = 'Student ID Invalid'
        elif form_pass_word is None or form_pass_word == '' :
            message2 = 'password Invalid'
        elif form_first_name is None or form_first_name == '' :
            message2 = 'First name Invalid'
        elif form_last_name is None or form_last_name == '':
            message2 = 'Last name Invalid'
        elif form_email is None or form_email == '' :
            message2 = 'email Invalid'
        else:

            user = User(First_name = form_first_name, Last_name= form_last_name,role='student',student_id=int(form_student_id),Email=form_email,user_id=form_user_name,year=0)
            user.hash_password(form_pass_word)
            request.db_session.add(user)
    print '\n\n\n\n\n####################################################\n\n\n\n\n\n'

    return dict(
        message=message,
        message2 = message2,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
        form_user_name=form_user_name,
        form_student_id = form_student_id,
        form_pass_word = form_pass_word,
        form_first_name = form_first_name,
        form_last_name = form_last_name,
        form_email = form_email,
        )