from datetime import datetime
from math import e
from re import sub

from flask import Blueprint, flash, g, render_template, request, url_for
from pybo import db
from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Answer, Question, User
from pybo.views.auth_views import login_required
from werkzeug.utils import redirect

bp = Blueprint('question', __name__, url_prefix='/question')
# url_preflix에 / 를안붙였으므로 /붙여야함 앞뒤로 /가 나와야 작동!!
# /question/면 detail 만함

@bp.route('/list/')
def _list():
    page=request.args.get('page',type=int,default=1)
    kw=request.args.get('kw',type=str,default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    # url 쿼리 파라미터에서 가져올거 url통해서 가져오는거기때문에 views저의해주어햐마
    # default=1이기때문에 자동으로 ?page=1이되어서 받아온느거 없으면 안됨 ?page= 이래버림
    if kw:
        search='%%{}%%'.format(kw)
        sub_query=db.session.query(Answer.quesiton_id,Answer.content,User.username) \
            .join(User,Answer.user_id==User.id).subquery()
        # 필드 명시선언하면 그필드만가져오고
        # 명시선언안할시 전체가져옴
        question_list=question_list \
            .join(User) \
            .outerjoin(sub_query,sub_query.c.quesiton_id==Question.id) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    ) \
            .distinct()
            # 같은거니까 Answer.content,Answer.Username,Answer.question_id가 오른쪽에 붙는다
    
    
    question_list=question_list.paginate(page=page,per_page=10)
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    # 처음부터들어갈경우
    form=AnswerForm()
    question = Question.query.get_or_404(question_id)
    # answer_view에서 form을 전달했는데 여기서 안하면 에러 null 이되버림 연동되는게아니라서
    # 다써줘야함
    return render_template('question/question_detail.html', question=question,form=form) 

# render post를하는 디폴드url을 가지고있는데 이 디폴트 url은 기본적으로
# post를 못받음 그러므로 써줘야함
# 하지만 지금 route에서 post를 받는다고 써있지않기때문에 오류

@bp.route('/create/',methods=('GET','POST'))
@login_required
def create():
    # 함수바로위에 해야함
    # 기본적으로 get이기때문에 if post를 써줭햐ㅏㅁ
    
    form=QuestionForm()
    if request.method == 'POST'  and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),user=g.user)
        # 전역변수 g에 저장된걸 가져온다
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html',form=form)


@bp.route('/modify/<int:question_id>',methods=('GET','POST'))
@login_required
# login_required는 view만담고 라우팅은 못잡어넣음
def modify(question_id):
    question=Question.query.get_or_404(question_id)
    
    if g.user !=question.user:
        flash('수정권한x')
        return redirect(url_for('question.detail',question_id=question_id))
    if request.method=='POST':
        form=QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date=datetime.now()
            db.session.commit()
            # 아직 add하는거아님
            return redirect(url_for('question.detail',question_id=question_id))
    else:
        form=QuestionForm(obj=question)
    return render_template('question/question_form.html',form=form)    

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question=Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한x')
        return redirect(url_for('question.detail',question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    # commit 변경점 적용
    return redirect(url_for('question._list'))


@bp.route('/voter/<int:question_id>')
@login_required
def vote(question_id):
# def view 매개함수에는 route로부터 받는거임
# route가 views가있으면 view 받느넉고
    _question=Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인추천x')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=question_id))