

# import sqlalchemy as db

from pybo import db

# 유저한명이 질문여러개 올리면 질문이 다가되고
# 질문한개에 답변이 여러개달리면 답변이 여러개됨
# n:n관계를 하려고하면 가능하긴하나 두개다 pk관계가 성리됨

question_voter=db.Table(
    # queestion->voter라는뜻
    'question_voter',
    # 속성이름='user_id'표기
    db.Column('user_id',db.Integer(),db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True),
    db.Column('question_id',db.Integer(),db.ForeignKey('question.id',ondelete='CASCADE'),primary_key=True)
)
answer_voter=db.Table(
    'answer_voter',
    # 속성이름='user_id'표기
    db.Column('user_id',db.Integer(),db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True),
    db.Column('answer_id',db.Integer(),db.ForeignKey('answer.id',ondelete='CASCADE'),primary_key=True)
)
class Question(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    subject=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    modify_date=db.Column(db.DateTime(),nullable=True)
    # server_default=없던속성을 만들어야하는상황에서씀
    # flask db upgrade에도 속성갖고있지않던 기존데이터에도 저장되지만
    #  그냥 default는 새로생성되는것만됨 기존거하려면 server_default해줘야함
    # 최종리비젼= heads 현재리비젼=current 현재->최종하려면 current하고 ,flask db stamp heads로 해야함
    user=db.relationship('User',backref=db.backref('question_set'))
    voter=db.relationship('User',secondary='question_voter',backref=db.backref('question_voter_set'))
    # backref는 voter->question_voter_set으로 가능
    # question_voter에 실제데이터가 저장되고, Question모델의 voter속성을 통해 참조가능 question->voter로 가능
class Answer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    quesiton_id=db.Column(db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'))
    question=db.relationship('Question',backref=db.backref('answer_set'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    user=db.relationship('User',backref=db.backref('answer_set'))
    # reationship을 안할경우 answer.question_id 를 Question.query.get(answer.question) 해야함 코드길어지고 싫음 
    # 외래부모키 id 후 부모키로 바로 들어갈수있는걸 reation쉽하면 편하게 .하나찍고 할수있음 굳이 id안알아도됨
    modify_date=db.Column(db.DateTime(),nullable=True)
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    voter=db.relationship('User',secondary='answer_voter',backref=db.backref('answer_voter_set'))
    
class User(db.Model):
    # 굳이 Integer ()안해도 자동으로 스태틱 기본값초기화있어서 상관없을듯?
    # String은그래도 글자제한들어가야하니 하는게나음?
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(),unique=True,nullable=False) 
    #   migrate해서 리비젼파일생성 리비젼파일=변경점을 기록하는것
    #  이 변경점을 적용하고싶으면 upgrade를 하는거
    #  여태까지한 변경점을 저장 실시간으로 저장이안되기때문에 그냥 임시로 저장하는것
    # 만약 migrate하고 upgrade안한후 여러작업후 upgrade하면 migrate한지점까지만한다는뜻
    