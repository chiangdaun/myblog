# -*- coding:utf-8 -*-
"""
Author:duan
Date:2019/4/17 22:09
"""
import datetime
import os
import time
from functools import wraps

import psutil as psutil
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory, \
    session, jsonify
from flask_ckeditor import upload_success, upload_fail

from blog.extensions import db
from blog.forms import PostForm, CategoryForm, LinkForm, AboutmeForm
from blog.models import Post, Category, Comment, Link, Aboutme, Oplog
from blog.utils import allowed_file

admin_bp = Blueprint('admin', __name__)
page_data = None


# 登录装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 上下文应用处理器
@admin_bp.context_processor
def tpl_extra():
    data = dict(
        online_time=time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
        len=current_app.config['POST_PER_PAGE'],
        admin=session["admin"]
    )
    return data


# 计算内存使用率
@admin_bp.route('/memory_state')
def memory_state():
    phymem = psutil.virtual_memory()
    total_mem = int(phymem.total / 1024 / 1024)
    used_mem = int(phymem.used / 1024 / 1024)
    available_mem = int(phymem.available / 1024 / 1024)
    line = [{"used_mem": used_mem, "total_mem": total_mem, "available_mem": available_mem}]
    return jsonify(line)


# 后台首页
@admin_bp.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')


# 博客列表
@admin_bp.route('/posts/list/<int:page>', methods=['GET', 'POST'])
@admin_login_req
def post_list(page=None):
    global page_data
    if page is None:
        page = 1
    page_data = Post.query.order_by(
        Post.timestamp.desc()
    ).paginate(page=page, per_page=current_app.config['POST_PER_PAGE'])
    return render_template('admin/post_list.html', page_data=page_data, page=page)


# 获取图片
@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


# 上传图片
@admin_bp.route('/upload', methods=['POST', 'GET'])
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only!')
    f.save(os.path.join(current_app.config['UPLOAD_PATH'], f.filename))
    url = url_for('.get_image', filename=f.filename)
    return upload_success(url, f.filename)


# 新增博客
@admin_bp.route('/post/new', methods=['GET', 'POST'])
@admin_login_req
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(
            title=title,
            body=body,
            category=category,
            read_num=form.read_num.data,
            comment_num=form.comment_num.data,
            like_num=form.like_num.data
        )
        db.session.add(post)
        db.session.commit()
        flash('添加博客成功!', 'ok')
        oplog = Oplog(
            user='dsq',
            ip=request.remote_addr,
            reason="新增博客-%s" % form.title.data,
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.new_post'))
    return render_template('admin/new_post.html', form=form)


# 编辑博客
@admin_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@admin_login_req
def edit_post(post_id=None):
    if page_data is None or page_data.pages == 1:
        page = 1
    else:
        page = page_data.page if page_data.page < page_data.pages or page_data.total % page_data.per_page != 1 else page_data.pages - 1
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        post.read_num = form.read_num.data
        post.comment_num = form.comment_num.data
        post.like_num = form.like_num.data
        db.session.commit()
        flash('重新编辑成功!', 'ok')
        oplog = Oplog(
            user='dsq',
            ip=request.remote_addr,
            reason="编辑博客-%s" % form.title.data,
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.post_list', page=page))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    form.comment_num.data = post.comment_num
    form.read_num.data = post.read_num
    form.like_num.data = post.like_num
    return render_template('admin/edit_post.html', form=form)


# 删除博客
@admin_bp.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@admin_login_req
def delete_post(post_id=None):
    if page_data is None or page_data.pages == 1:
        page = 1
    else:
        page = page_data.page if page_data.page < page_data.pages or page_data.total % page_data.per_page != 1 else page_data.pages - 1
    post = Post.query.get_or_404(int(post_id))
    db.session.delete(post)
    db.session.commit()
    flash('删除博文成功!', 'ok')
    oplog = Oplog(
        user='dsq',
        ip=request.remote_addr,
        reason="删除博客-%s" % post.title,
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.post_list', page=page))


# 分类列表
@admin_bp.route('/category/list/<int:page>', methods=['GET', 'POST'])
@admin_login_req
def category_list(page=None):
    global page_data
    if page is None:
        page = 1
    page_data = Category.query.order_by(
        Category.id.desc()
    ).paginate(page=page, per_page=current_app.config['POST_PER_PAGE'])
    return render_template('admin/category_list.html', page_data=page_data, page=page)


# 新增分类(自定义表单验证器不起作用)
@admin_bp.route('/category/new', methods=['GET', 'POST'])
@admin_login_req
def new_category():
    form = CategoryForm()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        name = form.name.data
        if Category.query.filter_by(name=form.name.data).count() == 1:
            flash('分类已存在!', 'err')
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('添加分类成功!', 'ok')
        oplog = Oplog(
            user='dsq',
            ip=request.remote_addr,
            reason="新增分类-%s" % form.name.data,
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.new_category'))
    return render_template('admin/new_category.html', form=form)


# 编辑分类
@admin_bp.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
@admin_login_req
def edit_category(category_id=None):
    if page_data is None or page_data.pages == 1:
        page = 1
    else:
        page = page_data.page if page_data.page < page_data.pages or page_data.total % page_data.per_page != 1 else page_data.pages - 1
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('默认分类不可更改', 'err')
        return redirect(url_for('admin.category_list', page=page))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('编辑分类成功!', 'ok')
        oplog = Oplog(
            user='dsq',
            ip=request.remote_addr,
            reason="修改分类:'%s'为'%s'" % (category.name, form.name.data),
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.category_list', page=page))
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


# 删除分类
@admin_bp.route('/category/delete/<int:category_id>', methods=['GET', 'POST'])
def delete_category(category_id=None):
    if page_data.pages == 1 or page_data is None:
        page = 1
    else:
        page = page_data.page if page_data.page < page_data.pages or page_data.total % page_data.per_page != 1 else page_data.pages - 1
    category = Category.query.get_or_404(int(category_id))
    # 此处的delete()是在Category类中实现的，实现了删除某一分类时,将该类下的所有文章移到默认分类
    category.delete()
    flash('删除分类成功!', 'ok')
    oplog = Oplog(
        user='dsq',
        ip=request.remote_addr,
        reason="删除分类-%s" % category.name,
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.category_list', page=page))


# 评论列表
@admin_bp.route('/comment/list/<int:page>', methods=['GET', 'POST'])
@admin_login_req
def comment_list(page=None):
    global page_data
    if page is None:
        page = 1
    page_data = Comment.query.order_by(
        Comment.id.desc()
    ).paginate(page=page, per_page=current_app.config['POST_PER_PAGE'])
    return render_template('admin/comment_list.html', page_data=page_data, page=page)


# 链接列表
@admin_bp.route('/links/list/<int:page>', methods=['GET', 'POST'])
@admin_login_req
def link_list(page=None):
    global page_data
    if page is None:
        page = 1
    page_data = Link.query.order_by(
        Link.id.desc()
    ).paginate(page=page, per_page=current_app.config['POST_PER_PAGE'])
    return render_template('admin/link_list.html', page_data=page_data, page=page)


# 新增链接
@admin_bp.route('/link/new', methods=['GET', 'POST'])
@admin_login_req
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        if Link.query.filter_by(name=name).count() == 1:
            flash("链接已存在!", "err")
        link = Link(name=name, url=url)
        db.session.add(link)
        db.session.commit()
        flash('添加链接成功!', 'ok')
        oplog = Oplog(
            user='dsq',
            ip=request.remote_addr,
            reason="新增链接-%s" % form.name.data,
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for("admin.new_link"))
    return render_template('admin/new_link.html', form=form)


# 编辑链接
@admin_bp.route('/link/edit/<int:link_id>', methods=['GET', 'POST'])
@admin_login_req
def edit_link(link_id=None):
    if page_data is None or page_data.pages == 1:
        page = 1
    else:
        page = page_data.page if page_data.page < page_data.pages or page_data.total % page_data.per_page != 1 else page_data.pages - 1
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash("编辑链接成功", "ok")
        oplog = Oplog(
            user='dsq',
            ip=request.remote_addr,
            reason="修改链接:'%s'为'%s'" % (link.name, form.name.data),
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.link_list', page=page))
    form.name.data = link.name
    form.url.data = link.url
    return render_template('admin/edit_link.html', form=form)


# 删除链接
@admin_bp.route('/link/delete/<int:link_id>', methods=['GET', 'POST'])
@admin_login_req
def delete_link(link_id=None):
    if page_data is None or page_data.pages == 1:
        page = 1
    else:
        page = page_data.page if page_data.page < page_data.pages or page_data.total % page_data.per_page != 1 else page_data.pages - 1
    link = Link.query.get_or_404(int(link_id))
    db.session.delete(link)
    db.session.commit()
    flash("删除链接成功!", "ok")
    oplog = Oplog(
        user="dsq",
        ip=request.remote_addr,
        reason="删除链接-%s" % link.name,
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.link_list', page=page))


# 关于我
@admin_bp.route('/aboutme/', methods=['GET', 'POST'])
@admin_login_req
def edit_aboutme():
    form = AboutmeForm()
    aboutme = Aboutme.query.first()
    if form.validate_on_submit():
        aboutme.intro = form.intro.data
        aboutme.body = form.body.data
        db.session.commit()
        flash('编辑完成!', 'ok')
        oplog = Oplog(
            user='dsq',
            ip=request.remote_addr,
            reason="编辑关于我",
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.edit_aboutme'))
    form.intro.data = aboutme.intro
    form.body.data = aboutme.body
    return render_template('admin/edit_aboutme.html', form=form)


# 操作日志
@admin_bp.route('/oplog/list/<int:page>', methods=['GET'])
@admin_login_req
def oplog_list(page=None):
    global page_data
    if page is None:
        page = 1
    page_data = Oplog.query.order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=current_app.config['POST_PER_PAGE'])
    return render_template("admin/oplog_list.html", page_data=page_data, page=page)
