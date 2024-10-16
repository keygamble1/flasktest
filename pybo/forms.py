from ast import Eq, Pass

from flask_wtf import *
from wtforms import *
from wtforms.validators import *


class QuestionForm(FlaskForm):
    # validetors는 수정가능하기떄문에 datarequired를 리스트형태로받음
    subject=StringField('제목',validators=[DataRequired('제목은 필수입력')])
    content=TextAreaField('내용',validators=[DataRequired('내용은 필수입력')])

class AnswerForm(FlaskForm):
    content=TextAreaField('내용',validators=[DataRequired('내용은 필수 입력')])

class UserCreateForm(FlaskForm):
    # 클래스변수로 정의를 해버리면 부모클래스에서는 인자를 받지않고도 폼을 사용가능함
    # DAtarequired 빈칸을 안채울시 오류가 발생한다느 ㄴ뜻임 폼제출할때
    # 튜플은 새로 생성해야함  migrate upgrade시 +    vaildators로
    # list는 가변적이라 원소의 개수를 넣다뺏다해도 새로생성안하고 그대로 유지함
    # 튜플은 수정추가삭제를하려면 빈 튜플을 만들고 거기다가 새로 고쳐넣어야함
    # list는 가변이라 그 list변수에서 계속 삭제 수정다가능
    username=StringField('사용자이름',validators=[DataRequired(),Length(min=3,max=25)])
    # input type="text"
    password1=PasswordField('비밀번호',validators=[DataRequired(),EqualTo('password2','비밀번호일치x')])
    # input type="password "자동변환
    password2=PasswordField('비밀번호확인',validators=[DataRequired()])
    email=EmailField('이메일',validators=[DataRequired(),Email()])
    # input type="email"로 자동변환 이제 html이랑 형식 다 맞춰야함

class UserLoginForm(FlaskForm):
    username=StringField('사용자이름',validators=[DataRequired(),Length(min=3,max=25)])
    password=PasswordField('비밀번호',validators=[DataRequired()])    