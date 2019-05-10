# -*- coding:utf-8 -*-
"""
Author:duan
Date:2019/4/17 22:10
"""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from blog.models import Category, Admin


# 管理员登录表单
class LoginForm(FlaskForm):
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号!",
            "required": "required",
            # "autocomplete": "off"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码!",
            "required": "required"
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField(
        label='博客标题',
        validators=[
            DataRequired(),
            Length(1, 128)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "博客标题...",
            "required": "required",
        }
    )
    category = SelectField(
        label='Category',
        coerce=int,
        default=1,
        render_kw={
            "class": "form-control",
            "placeholder": "选择类别",
            "required": "required"
        }
    )
    body = CKEditorField(
        label='博客正文',
        validators=[
            DataRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "输入博客正文...",
            "required": "required"
        }
    )
    read_num = IntegerField(
        label='阅读数',
        validators=[
            DataRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "输入阅读数...",
            "required": "required"
        }
    )
    comment_num = IntegerField(
        label='评论数',
        validators=[
            DataRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "输入评论数...",
            "required": "required"
        }
    )
    like_num = IntegerField(
        label='点赞数',
        validators=[
            DataRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "输入点赞...",
            "required": "required"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField(
        label='Name',
        validators=[
            DataRequired(),
            Length(1, 30)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "输入分类名称...",
            "required": "required"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).count() == 1:
            raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField(
        label='链接名称',
        validators=[
            DataRequired(),
            Length(1, 30)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "输入链接名称...",
            "required": "required"
        }
    )
    url = StringField(
        label='链接URL',
        validators=[
            DataRequired(),
            URL(),
            Length(1, 255)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "输入链接URL...",
            "required": "required"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )


class MessageForm(FlaskForm):
    name = StringField(
        label='你的名字',
        validators=[
            DataRequired(),
            Length(1, 10)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "姓名或者昵称",
            "required": "required"
        }
    )
    email = StringField(
        label='你的邮箱',
        validators=[
            DataRequired(),
            Email(),
            Length(1, 254)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "邮箱",
            "required": "required"
        }
    )
    site = StringField(
        'Site',
        validators=[
            Optional(),
            URL(),
            Length(0, 255)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "网址",
        }
    )
    body = TextAreaField(
        label='留言',
        validators=[
            DataRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "写下你要说的吧...",
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )


class AboutmeForm(FlaskForm):
    intro = StringField(
        label='关于我简介',
        validators=[
            DataRequired(),
            Length(1, 128)
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "博客标题...",
            "required": "required",
        }
    )
    body = CKEditorField(
        label='关于我正文',
        validators=[
            DataRequired()
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "输入正文...",
            "required": "required"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )


class SearchForm(FlaskForm):
    search_key = StringField(
        label='关键字',
        description='关键字',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入关键字...",
            "size": "12"
        }
    )
    submit = SubmitField(
        label='搜索',
        render_kw={
            "class": "btn btn-primary"
        }
    )
