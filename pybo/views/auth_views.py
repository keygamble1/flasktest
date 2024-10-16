import functools
from textwrap import wrap

from flask import (Blueprint, flash, g, render_template, request, session,
                   url_for)
from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

bp=Blueprint('auth',__name__,url_prefix='/auth')
# '라벨','이경로의 이름','url_preflex


    
    
@bp.route('/signup/',methods=('GET','POST'))
def signup():
    form=UserCreateForm()
    if request.method =='POST' and form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        
        if not user:
            # 모델=form형식으로 유효성검사해야함
            user=User(username=form.username.data,
                    password=generate_password_hash(form.password1.data),
                    email=form.email.data
                    )
            db.session.add(user)
            # 변경점 저장=add migrate 같음
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재함')
    return render_template('auth/signup.html',form=form)
            
@bp.route('/login/',methods=('GET','POST'))
def login():
    form=UserLoginForm()
    if request.method=='POST' and form.validate_on_submit():
        error=None
        user=User.query.filter_by(username=form.username.data).first()
        if not user:
            error='존재안하는 사용자'
        elif not check_password_hash(user.password,form.password.data):
            error='비밀번호x'
        if error is None:
            session.clear()
            # 계속 실패하고나서 login될경우 대비
            # user라는 레코드에서 id를 뽑아 session에 넣음
            session['user_id']=user.id
            _next=request.args.get('next','')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html',form=form)
            # list user_id가 또있어도 어차피 인덱스있어서 괜ㄴ찮음
            # user_id라는 키가있느게아님 딕셔너리방식과 유사한것
            
            # 세션저장
# @bp.before_app_request는 라우팅함수보다 먼저실행
@bp.before_app_request
def load_logged_in_user():
    user_id=session.get('user_id')
    # 저장된 세션을 불러온다
    if user_id is None:
        g.user=None
    else:
        g.user=User.query.get(user_id)
        # 전역변수 할당
        
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
def login_required(view):
    @functools.wraps(view)
    # 원래는 데코레이터쓸경우 view함수가 view 메탙데이터를 변경하지만 
    # wraps하면 변경되지않음
    # 사용하지않을경우 view.__nae__=원래 view.ㅔㅛ vkdlfdl wrapper로 변경됨
    # 메타데이터=함수자체의 동작과는 관련없지만 그함수에대한 부가적인 정보제공하는속성
    # 데이터의 데이터,__name__은 함수이름 내가 py파일을 만들었을때 그 py함수의 정보들을 출력한다는것이다
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next=request.url if request.method=='GET' else ''
            # 삼항연산자 request.method==get일때 _next=request.url 아니면 ''
            return redirect(url_for('auth.login',next=_next))
        return view(*args, **kwargs)
    return wrapped_view