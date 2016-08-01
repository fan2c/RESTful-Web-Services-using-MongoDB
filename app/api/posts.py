from . import api
from .. import mongo
from datetime import datetime
from bson import json_util
from bson.objectid import ObjectId
from flask import jsonify, request, abort
import json

@api.route('/articles', methods=['GET'])
def getAriticles():
    cur = mongo.db.posts.find().sort('date')
    if not cur:
        abort(400)
    articles = [article for article in cur]
    return jsonify({'articles': json.dumps(articles, default=json_util.default)})

@api.route('/articles/<string:article_id>', methods=['GET'])
def getAriticle(article_id):
    articles = mongo.db.posts.find_one(
        {'_id': ObjectId(article_id)}
    )
    if not articles:
        abort(400)
    return jsonify({'articles': json.dumps(articles, default=json_util.default)})

@api.route('/articlesbyTag/<string:tag>', methods=['GET'])
def getArticlesbyTag(tag):
    if tag is None:
        abort(400)
    cur = mongo.db.posts.find(
        {'tags': tag})
    if not cur:
        abort(400)
    articles = [article for article in cur]
    return jsonify({'articles': json.dumps(articles, default=json_util.default)})


@api.route('/article', methods=['POST'])
def createArticle():
    data = request.get_json()
    if not data:
        return jsonify({'message':'No data!'})
    article = {
        'title': data['title'],
        'context': data['context'],
        'date': datetime.utcnow(),
        'author': data['author'],
        'tags': data['tags'],
    }
    mongo.db.posts.insert(article)
    return jsonify({'articles': json.dumps(article, default=json_util.default)}), 201

@api.route('/articles/<string:article_id>/comments', methods=['GET'])
def getComment(article_id):
    page = request.args.get('page')
    print(page)
    qry = {'article_id': ObjectId(article_id)}
    if page is not None:
        qry['page'] = int(page)
    cur = mongo.db.comments.find(qry)
    if not cur:
        abort(400)
    comments = [comment for comment in cur]
    return jsonify({'comments' : json.dumps(comments, default=json_util.default)})

@api.route('/articles/<string:article_id>/comments', methods=['POST'])
def addComment(article_id):
    comment = request.get_json()
    if not comment:
        return jsonify({'message':'No data!'})
    comments_pages = 1
    article = mongo.db.posts.find_and_modify(
        {'_id': ObjectId(article_id)},
        {'$inc': {'last_comment_id': 1}},
        new=True,
        fileds={'last_comment_id':1})
    if article is None:
        abort(400)
    page_id = article['last_comment_id'] // 100
    comment['date'] = datetime.utcnow()
    page = mongo.db.comments.find_and_modify(
        {'article_id': ObjectId(article_id),
         'page': page_id},
        {'$inc': {'count': 1},
         '$push': {
            'comments': comment}},
        fields={'count': 1},
        upsert=True,
        new=True)
    if page['count']> 100:
        mongo.db.posts.update(
            {'_id': article_id,
             'comments_pages': article['comments_pages']},
            {'$inc': {'comments_pages': 1}}
        )
    res = mongo.db.posts.update(
        {'_id': ObjectId(article_id)},
            {'$push': {'comments': {'$each': [comment],
                    '$sort': {'date': 1},
                    '$slice': -10}},
             '$inc': {'comment_count': 1}})
    addInteraction(article_id, type)
    if res is None:
        abort(400)
    return jsonify({'comment': json.dumps(comment, default=json_util.default)}), 201

def addInteraction(article_id, type):
  ts = datetime.utcnow()
  mongo.db.interactions.update(
    { 'article_id' : ObjectId(article_id),
      'date' : datetime(ts.year, ts.month, ts.day)},
    { '$inc' : {
        'daily.{}'.format(type) : 1,
        'hourly.{}.{}'.format(ts.hour,type) : 1
    }},
    upsert=True,
    w=0)
