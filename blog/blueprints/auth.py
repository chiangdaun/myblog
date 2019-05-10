# -*- coding:utf-8 -*-
"""
Author:duan
Date:2019/4/17 22:09
"""
from io import BytesIO

from flask import render_template, flash, redirect, url_for, Blueprint, session, request, make_response
from flask_login import logout_user, login_required, current_user
from blog.blueprints.code import get_verify_code
from blog.forms import LoginForm
from blog.models import Admin

auth_bp = Blueprint('auth', __name__)


# 验证码
@auth_bp.route('/code')
def get_code():
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = code
    return response


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.account.data
        password = form.pwd.data
        admin = Admin.query.filter_by(username=username).first()
        if admin:
            if not admin.validate_password(password):
                flash("密码错误！", "err")
                return redirect(url_for("auth.login"))
            session['admin'] = form.account.data
        else:
            flash('账号不存在.', 'err')
            return redirect('login')
        return redirect(url_for("admin.index"))
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    session.pop("admin")
    logout_user()
    return redirect(url_for('home.index'))
