"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import redis 
from buzzfire.comment_app.models import Comment
from buzzfire.comment_app.dao import CommentDao

class SimpleTest(TestCase):
    def test_comment_dao(self):
        conn = redis.Redis("localhost")
        comment = Comment("1", "1", "hello")
        commentDao = CommentDao(conn)
        commentDao.save(comment)
        commentDao.get_comment("1")


