# -*- coding:utf-8 -*-
"""
Author:duan
Date:2019/4/17 22:09
"""
from flask import render_template, flash, request, current_app, Blueprint, jsonify
from blog.extensions import db
from blog.models import Post, Category, Link, Aboutme

home_bp = Blueprint('home', __name__)


# 首页,显示最新的8篇博文
@home_bp.route('/')
def index():
    post_list = Post.query.order_by(
        Post.timestamp.desc()
    ).limit(8)
    return render_template('home/index.html', post_list=post_list)


# 搜索
@home_bp.route('/search/', methods=['GET'])
def search():
    keyword = request.args.get('keyboard', '')
    # print(keyword)
    if keyword == '':
        flash('Enter keyword about post.', 'err')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['HOME_POST_PER_PAGE']
    page_data = Post.query.filter(
        Post.title.ilike('%' + keyword + '%')
    ).paginate(page, per_page)
    return render_template('home/search.html', keyword=keyword, page_data=page_data)


# 测试侧边栏
@home_bp.route('/test/', methods=['GET'])
def test():
    return render_template('home/test.html')


# 展示博文
@home_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id=None):
    post = Post.query.get_or_404(int(post_id))
    next_post = Post.query.filter(Post.id > int(post_id)).first()
    prev_post = Post.query.filter(
        Post.id < int(post_id)
    ).order_by(
        Post.id.desc()
    ).first()
    return render_template('home/show_post.html', post=post, next_post=next_post, prev_post=prev_post)


# 查询某一级目录下的所有二级目录的所有博客
@home_bp.route('/posts/first_cate/<string:keyword>/<int:page>', methods=['GET', 'POST'])
def show_first_cate(keyword=None, page=None):
    global page_data
    if page is None:
        page = 1
    first_cates = Category.query.filter_by(type=keyword)
    first_cate_list = []
    for first_cate in first_cates:
        first_cate_list.append(first_cate.id)
    page_data = Post.query.filter(
        Post.category_id.in_(first_cate_list)
    ).paginate(page=page, per_page=current_app.config['HOME_POST_PER_PAGE'])
    return render_template('home/first_cate_posts.html', page_data=page_data, page=page, type=keyword)


# 查询某二级目录下的所有博客并展示
@home_bp.route('/posts/cate/<int:keyword>/<int:page>', methods=['GET', 'POST'])
def show_cate(keyword=None, page=None):
    global page_data
    if page is None:
        page = 1
    page_data = Post.query.filter_by(
        category_id=keyword
    ).paginate(page=page, per_page=current_app.config['HOME_POST_PER_PAGE'])
    second_category = Category.query.filter_by(id=keyword).first().name
    return render_template('home/cate_posts.html', page_data=page_data, page=page, cate_id=keyword,
                           second_category=second_category)


# 留言
@home_bp.route('/message/new/', methods=['GET', 'POST'])
def message():
    aboutme = Aboutme.query.first()
    return render_template('home/message.html', aboutme=aboutme)


# 关于我
@home_bp.route('/aboutme/', methods=['GET', 'POST'])
def about_me():
    aboutme = Aboutme.query.first()
    return render_template('home/aboutme.html', aboutme=aboutme)


@home_bp.route('/sidebar1/')
def sidebar_1():
    tuijian = Post.query.order_by(
        Post.comment_num.desc()
    ).limit(1)
    result = []
    for tui in tuijian:
        result.append(tui.to_json())
    return jsonify(result)


# 侧边栏/点击排行
@home_bp.route('/sidebar4/')
def sidebar_4():
    tuijian = Post.query.order_by(
        Post.comment_num.desc()
    ).limit(5)
    result = []
    for tui in tuijian:
        result.append(tui.to_json())
    return jsonify(result[1:])


# 侧边栏/右上
@home_bp.route('/right_top/')
def right_top():
    right2 = Post.query.order_by(
        Post.like_num.desc()
    ).limit(2)
    result = []
    for right in right2:
        result.append(right.to_json())
    return jsonify(result)


# 学无止境
@home_bp.route('/category1/')
def work_category():
    category = Category.query.filter_by(type='work')
    result = []
    for cate in category:
        result.append(cate.to_json())
    return jsonify(result)


# 慢生活
@home_bp.route('/category2/')
def life_category():
    category = Category.query.filter_by(type='life')
    result = []
    for cate in category:
        result.append(cate.to_json())
    return jsonify(result)


# 友情链接
@home_bp.route('/links/')
def friendly_link():
    # i1 = request.args.get('i1')
    # i2 = request.args.get('i2')
    # print(i1, i2)
    links = Link.query.all()
    result = []
    for link in links:
        result.append(link.to_json())
    return jsonify(result)


# 點讚
@home_bp.route('/addlike/', methods=['GET', 'POST'])
def addlike():
    result = {}
    post_id = request.args.get('post_id')
    post_obj = Post.query.filter_by(id=post_id).first()
    # print(type(post_obj))
    like_count = post_obj.like_num
    like_count = like_count + 1
    post_obj.like_num = like_count
    db.session.commit()
    result['state'] = True
    return jsonify(result)
