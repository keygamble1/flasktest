from datetime import datetime

from flask import request
from pybo.models import Answer, Question, User

q=Question(subject='플라스크모델질문',content='id자동생성?',create_date=datetime.now())

from pybo import db

db.session.add(q)
db.session.commit()
Question.query.all()
Question.query.filter(Question.id==1).all()
Question.query.get(1)
Question.query.filter(Question.subject.like('%플라스크%')).all()
q=Question.query.get(2)
q
q.subject='Flask Model Question'
db.session.commit()
q=Question.query.get(1)
db.session.delete(q)
db.session.commit()
a=Answer(question=q,content='네 자동생성됨',create_date=datetime.now())
db.session.add(a)
db.session.commit()
a=Answer.query.get(1)

from datetime import datetime

from pybo import db
from pybo.models import Question

for i in range(300):
    q=Question(subject='테스트데이터[%03d]' % i, content='내용무',create_date=datetime.now())
    db.session.add(q)

db.session.commit()
page=request.args.get('page',type=int,default=1)
# url 쿼리 파라미터에서 가져올거 url통해서 가져오는거기때문에 views저의해주어햐마
# default=1이기때문에 자동으로 ?page=1이되어서 받아온느거 없으면 안됨 ?page= 이래버림


question_list = Question.query.order_by(Question.create_date.desc())
question_list=question_list.paginate(page=page,per_page=10)
question_list.has_prev
question_list.prev_num
question_list.has_next
question_list.next_num
question_list.iter_pages()
question_list.total
question_list.page-1
question_list.per_page
question = Question.query.get_or_404(1)
question.answer_set
# iter)pages=그냥 알맞게 페이지를 앞 끝 적절하게 분배해줌
# ?page=임 앞에 ? 뒤에 = 기호가 앞뒤로있어야함 = {{}} 이렇게외우자 = 변수니까
from pybo.models import Answer, Question

Question.query.count()
Answer.query.count()
Question.query.join(Answer).count()
# 삭제해도 Answer이 데이터가 남아서 더나옴
# join안에 모데들어가면 ㅏㅈ동 .query한다고보자
Question.query.outerjoin(Answer).count()
# 질문한개에 여러개 답변이기때문에 더늘음
Question.query.outerjoin(Answer).distinct().count()
# 중복제거 질문중복제거
# 질문1:답변1 질문1:답변2 보기안좋음
Question.query.outerjoin(Answer).filter(
    Question.content.ilike('%파이썬%')|
    Answer.content.ilike('%파이썬%')
).distinct().count()
# Answer->user를 쿼리
# user에서 answer을 쿼리한거 관계형 쿼리를 만듬
# 정보를 가져오려면 join을해야함 
# 필드를 추가하려면 join을 해줘야함
sub_query=db.session.query(Answer.quesiton_id,Answer.content,User.username) \
        .join(User,Answer.user_id==User.id).subquery()
        
question_list.next_num
        # 여기서 User는 조건부에불과 답변작성자도 있어야하기때문에
# Question에서 조회하기위한 중간쿼리
# 각질문에대해 조회할때는 1:1이라서 outer안해도되지만
# 각질문에 여러개의 answe가있을경우에는 다대1관게가 성립해 outerjoin을한다
# 동시에 post는 잘안되지만(서버가 부하됨 만료된페이지 계속 post로 쓰기때문)
# 동시에 get은 가능