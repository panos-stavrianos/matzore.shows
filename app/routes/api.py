# -*- coding: utf-8 -*-
from datetime import datetime

from flask import jsonify

from app import app
from app.models import PlayingNow, Show, Member, Article, Event, Tag, Category, Schedule, days


@app.route('/api/get_show_playing', methods=['GET'])
def api_get_show_playing():
    try:
        playing_now = PlayingNow.query.order_by(PlayingNow.id.desc()).first()
        if playing_now.until_time > datetime.now():
            playing_now_json = {'name': playing_now.show.name, 'cover': playing_now.show.logo,
                                'show_id': playing_now.show.id,
                                'message': playing_now.message, 'now': datetime.now()}
            return playing_now_json
    except:
        return {}
    return {}


@app.route('/api/get_shows', methods=['GET'])
def api_get_shows():
    try:
        shows = list(map(lambda show: show.to_dict(), Show.query.all()))
        return jsonify(shows)
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_show/<show_id>', methods=['GET'])
def api_get_show(show_id):
    try:
        show = Show.query.get(show_id).to_dict_full()
        return jsonify(show)
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_members', methods=['GET'])
def api_get_members():
    try:
        members = list(map(lambda member: member.to_dict(), Member.query.all()))
        return jsonify(members)
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_member/<member_id>', methods=['GET'])
def api_get_member(member_id):
    try:
        member = Member.query.get(member_id).to_dict_full()
        return jsonify(member)
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_articles', methods=['GET'])
def api_get_articles():
    try:
        articles = list(map(lambda article: article.to_dict(), Article.query.filter(Article.published == True).all()))
        return jsonify(articles)
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_article/<article_id>', methods=['GET'])
def api_get_article(article_id):
    try:
        article = Article.query.filter(Article.published == True, Article.id == article_id).first().to_dict_full()
        return jsonify(article)
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_events', methods=['GET'])
def api_get_events():
    try:
        events = list(map(lambda event: event.to_dict(), Event.query.filter(Event.published == True).all()))
        return jsonify(events)
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_event/<event_id>', methods=['GET'])
def api_get_event(event_id):
    try:
        event = Event.query.filter(Event.published == True, Event.id == event_id).first().to_dict_full()
        return jsonify(event)
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_tags', methods=['GET'])
def api_get_tags():
    try:
        tags = list(map(lambda tag: tag.to_dict(), Tag.query.all()))
        return jsonify({'tags': tags})
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_tag/<tag_id>', methods=['GET'])
def api_get_tag(tag_id):
    try:
        tag = Tag.query.get(tag_id).to_dict_full()
        events = list(filter(lambda event: event['published'], tag['events']))
        articles = list(filter(lambda article: article['published'], tag['articles']))
        return jsonify({'articles': articles, 'events': events})
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_categories', methods=['GET'])
def api_get_categories():
    try:
        categories = list(map(lambda category: category.to_dict(), Category.query.all()))
        return jsonify({'categories': categories})
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_category/<category_id>', methods=['GET'])
def api_get_category(category_id):
    try:
        articles = list(map(lambda article: article.to_dict(),
                            Article.query.filter(Article.published == True, Article.category_id == category_id).all()))
        return jsonify({'articles': articles})
    except Exception as e:
        print(e)
        return {}


@app.route('/api/get_schedule', methods=['GET'])
def api_get_schedule():
    try:
        schedule = Schedule.query.all()
        data = {}
        for day in days:
            data[day] = []
        for record in schedule:
            data[record.day].append(record.to_dict_full())
        for day in data:
            data[day] = sorted(data[day], key=lambda record: record['from_time'])
        return jsonify({'schedule': data, 'days': days})
    except Exception as e:
        print(e)
        return {}
