
from datetime import datetime

from flask import Blueprint, flash, g, render_template, request, url_for
from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Answer, Question
from pybo.views.auth_views import login, login_required
from werkzeug.utils import redirect

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form=AnswerForm()
    question=Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        
        content = request.form['content']
        answer = Answer(question=question, content=content, create_date=datetime.now(),user=g.user)
        db.session.add(answer)
        db.session.commit()
        # '{} = url 과 id가 들어가야함
        # '{}#answer_{}'.format(   ,answer.id) 
        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id),answer.id) )
    return render_template('question/question_detail.html',question=question,form=form)
@bp.route('/modify/<int:answer_id>',methods=('GET','POST'))
@login_required
def modify(answer_id):
    answer=Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail',question_id=answer.question.id))
    if request.method=='POST':
        form=AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date=datetime.now()
            db.session.commit()
                    # '{} = url 과 id가 들어가야함
        # '{}#answer_{}'.format(   ,answer.id) 
            return redirect('{}#answer_{}'.format(
                url_for('question.detail',question_id=answer.question.id),answer.id) )
    else:
        form=AnswerForm(obj=answer)
    return render_template('answer/answer_form.html',form=form)
            
@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer=Answer.query.get_or_404(answer_id)
    question_id=answer.question.id
    if g.user !=answer.user:
        flash('수정권한x')
    else:
        db.session.delete(answer)
        db.session.commit()
        
    return redirect(url_for('question.detail',question_id=question_id))
@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    _answer=Answer.query.get_or_404(answer_id)
    if g.user==_answer.user:
        flash('본인이 작성한글은 x')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
              # '{} = url 과 id가 들어가야함
        # '{}#answer_{}'.format(   ,answer.id) 
    return redirect('{}#answer_{}'.format(
        url_for('question.detail',question_id=_answer.question.id),_answer.id))
