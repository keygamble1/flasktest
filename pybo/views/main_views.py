from flask import Blueprint, redirect, render_template, url_for
from pybo.models import Question

# myproejct까지 들어가면 못찾음 
bp=Blueprint('main',__name__,url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('question._list'))
# views에서 redirect 찾는거





