# -*- coding:utf-8 -*-
"""
Author:duan
Date:2019/4/17 22:16
"""
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from blog import db
from blog.models import Admin, Category, Post, Comment, Link, Tag, Aboutme, Message

fake = Faker(locale='zh_CN')


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='Bluelog',
        blog_sub_title="No, I'm the real thing.",
        name='Ted Duan',
        about='Um, l, Ted Duan, had a fun time as a member of CHAM...'
    )
    admin.set_password('helloblog')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default', type='work')
    db.session.add(category)

    for i in range(count):
        type = 'work'
        if i % 3 == 0:
            type = 'life'
        category = Category(
            name=fake.word(),
            type=type
        )
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year(),
            comment_num=random.randint(10, 100),
            read_num=random.randint(100, 200),
            like_num=random.randint(50, 100)
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # unreviewed comments
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # from admin
        comment = Comment(
            author='Mima Kirigoe',
            email='mima@example.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # replies
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()


def fake_tags(count=20):
    for i in range(count):
        tag = Tag(
            name=fake.word(),
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(tag)
    db.session.commit()


def fake_message(count=50):
    for i in range(count):
        message = Message(
            name=fake.name(),
            email=fake.email(),
            site=fake.url(),
            message=fake.sentence(),
            ip=fake.ipv4(network=False),
            reviewed=True,
            addtime=fake.date_time_this_year(),
        )
        db.session.add(message)
    db.session.commit()


def fake_aboutme():
    aboutme = Aboutme(
        intro='一个走丢的孩子',
        body=fake.text(888)
    )
    db.session.add(aboutme)
    db.session.commit()
