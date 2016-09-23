import codecs
import csv
import datetime

from . import models as blog_engine_models
from django.contrib.auth.models import User

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def migrate_from_ghost_dump(posts_dump_file_path, tags_dump_file_path, posts_tags_filepath):
    """
from apps.blog_engine import utils
a = utils.migrate_from_ghost_dump('posts.csv', 'tags.csv', 'posts_tags.csv')

    """
    posts_sql = codecs.open(posts_dump_file_path, 'rb', encoding="utf-8")
    tags_sql = codecs.open(tags_dump_file_path, 'rb', encoding="utf-8")
    posts_tags_sql = codecs.open(posts_tags_filepath, 'rb', encoding="utf-8")

    tags_reader = unicode_csv_reader(tags_sql)
    tags = []
    for r in tags_reader:
        tag = blog_engine_models.Tag(
            name=r[1],
            slug=r[2]
        )
        tag.save()
        tag._id_ghost = int(r[0])
        tags.append(tag)

    posts_tags_reader = unicode_csv_reader(posts_tags_sql)
    posts_tags = []
    for r in posts_tags_reader:
        posts_tags.append(
            {
                'post': int(r[1]),
                'tag': int(r[2])
            }
        )

    posts_reader = unicode_csv_reader(posts_sql)
    posts = []
    for r in posts_reader:
        post = blog_engine_models.Post(
            title=r[1],
            slug=r[2],
            body_markdown=r[3],
            body=r[4],
            author=User.objects.get(pk=1)
        )
        post.created = datetime.datetime.fromtimestamp(int(r[6])/1000)
        post.save()
        post._id_ghost = int(r[0])
        posts.append(post)

    for post in posts:
        for posts_tag in posts_tags:
            for tag in tags:
                if post._id_ghost == posts_tag['post'] and tag._id_ghost == posts_tag['tag']:
                    post.tags.add(tag)
                    post.save()

    return posts




