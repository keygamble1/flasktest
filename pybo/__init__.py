

import config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db=SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

migrate=Migrate()
# db랑 migrate 해주기 migrate=임시 db=원본
# db,migrate 초기화 후 migrate에 담을 app도 선언 migarte안에 app이랑 db담아야함
def create_app():
    app=Flask(__name__)
    app.config.from_object(config)
    # flask app이랑 config 설정 초기화
    
    #orm
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app,db,render_as_batch=True)
        # migrate형식
    else:
        migrate.init_app(app,db)
    
    #블루푸린트
    #
    from .views import answer_views, auth_views, main_views, question_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(auth_views.bp)
    # app에 차곡차곡넣어야함
    
    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime']=format_datetime
    return app
    
    