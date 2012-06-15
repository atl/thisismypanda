import calendar 
from collections import Counter
from math import log
import shelve
from contextlib import closing
import json
from operator import itemgetter

from marmalade import TIMJUser

DATA_FILE = '../shelf2'
JSON_FILE = '../view/%s.json'

def received_likes_weekday_jams(user):
    my_jams = user.get_jams()
    likes_by_day = Counter()
    jams_by_day = Counter()
    for j in my_jams:
        day = calendar.weekday(*j.get_creation_date().timetuple()[:3])
        jams_by_day.update([day])
        likes_by_day.update({day: j.get_num_likes()})
    out = Counter()
    for k in likes_by_day:
        out[k] = float(likes_by_day[k]) / jams_by_day[k]
    return out


#
def received_plays_weekday_jams(user):
    my_jams = user.get_jams()
    plays_by_day = Counter()
    jams_by_day = Counter()
    for j in my_jams:
        day = calendar.weekday(*j.get_creation_date().timetuple()[:3])
        jams_by_day.update([day])
        plays_by_day.update({day: j.get_num_plays()})
    out = Counter()
    for k in plays_by_day:
        out[k] = float(plays_by_day[k]) / jams_by_day[k]
    return out

#
def friend_stats(user):
    my_friends = user.get_followers(sort='affinity')[:100]
    likes_by_artist = Counter()
    scaled_likes_by_artist = Counter()
    likes_by_weekday = Counter()
    likes_by_hour = Counter()
    jams_by_artist = Counter()
    scaled_jams_by_artist = Counter()
    for friend in my_friends:
        likes_by_day = Counter()
        fr_likes_by_artist = Counter()
        fr_jams_by_artist = Counter()
        fr_likes_by_hour = Counter()
        try:
            friend_likes = friend.get_liked_jams()
        except:
            friend_likes = []
        for like in friend_likes:
            fr_likes_by_artist.update([like.get_artist()])
            day = calendar.weekday(*like.get_creation_date().timetuple()[:3])
            likes_by_day.update([day])
            fr_likes_by_hour.update([like.get_creation_date().hour])
        for x in likes_by_day:
            likes_by_day[x] /= float(len(friend_likes))
        likes_by_weekday.update(likes_by_day)
        for x in fr_likes_by_hour:
            fr_likes_by_hour[x] /= float(len(friend_likes))
        likes_by_hour.update(fr_likes_by_hour)
        likes_by_artist.update(fr_likes_by_artist)
        for x in fr_likes_by_artist:
            fr_likes_by_artist[x] = log(fr_likes_by_artist[x]+1.7)
        scaled_likes_by_artist.update(fr_likes_by_artist)
        for jam in friend.get_jams():
            fr_jams_by_artist.update([jam.get_artist()])
        jams_by_artist.update(fr_jams_by_artist)
        for x in fr_jams_by_artist:
            fr_jams_by_artist[x] = log(fr_jams_by_artist[x]+1.7)
        scaled_jams_by_artist.update(fr_jams_by_artist)
    return {'artist_likes':likes_by_artist,
            'scaled_artist_likes':scaled_likes_by_artist,
            'days_likes': likes_by_weekday,
            'artist_jams':jams_by_artist,
            'scaled_artist_jams':scaled_jams_by_artist,
            'hours_likes': likes_by_hour}

def analyze(username, cached=True):
    user = TIMJUser(username)
    with closing(shelve.open(DATA_FILE)) as DATA:
        if username in DATA and cached:
            stats = DATA[username]
        else:
            stats = friend_stats(user)
            if cached:
                DATA[username] = stats
    shaped = []
    artists = set(dict(stats['artist_likes'].most_common(25))).union(
        set(dict(stats['artist_jams'].most_common(25))),
        set(dict(stats['scaled_artist_likes'].most_common(25))),
        set(dict(stats['scaled_artist_jams'].most_common(25))))
    for art in artists:
        art_dict = {}
        art_dict['Artist'] = art
        # "Liked Artists", "Liked Artists Scaled", "Jammed Artists", "Jammed Artists Scaled"
        art_dict['Liked Artists'] = dict(stats['artist_likes']).get(art,0)
        art_dict['Liked Artists Scaled'] = dict(stats['scaled_artist_likes']).get(art,0)
        art_dict['Jammed Artists'] = dict(stats['artist_jams']).get(art,0)
        art_dict['Jammed Artists Scaled'] = dict(stats['scaled_artist_jams']).get(art,0)
        shaped.append(art_dict)
    output = {'artists': shaped}
    output['name'] = user.get_full_name()
    output['url'] = 'http://www.thisismyjam.com/%s' % username
    output['username'] = username
    output['avatar'] = user.get_avatar(size='small')
    output['clock'] = map(itemgetter(1),stats['hours_likes'].items())
    output['calendar'] = map(itemgetter(1),stats['days_likes'].items())
    return output
        
def save(username):
    with open(JSON_FILE % username, 'w') as f:
        json.dump(analyze(username), f)
