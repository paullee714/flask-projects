from flask import Blueprint, request, jsonify, current_app
from my_util.my_logger import my_logger
from my_model import user_model
from my_model import tweet_model
from my_util.auth_util import token_required

import jwt
import datetime

tweet_route = Blueprint('tweet_route', __name__)


@tweet_route.route('/tweet', methods=["GET"])
@token_required
def tweet_list(current_user):
    my_logger.info("get Tweet List")
    tweet_list = tweet_model.Tweet.query.all()
    return jsonify([t.to_dict() for t in tweet_list])


@tweet_route.route('/tweet', methods=["POST"])
@token_required
def create_tweet(current_user):
    my_logger.info("Tweet Post!")
    try:
        data = request.get_json()
        title = data.get("title")
        words = data.get("words")
        created_at = datetime.datetime.utcnow()
        updated_at = datetime.datetime.utcnow()

        db = tweet_model.db
        tweet = tweet_model.Tweet(
            title=title,
            words=words,
            creator=current_user.username,
            created_at=created_at,
            updated_at=updated_at
        )
        db.session.add(tweet)
        db.session.commit()
        return jsonify(tweet.to_dict()), 200
    except Exception as e:
        my_logger.error(e)
        return jsonify({'message': 'fail to save tweet'}), 200
