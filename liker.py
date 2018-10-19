import time
from random import randint
import json
import requests
try:
    from instagram_private_api import (
        Client, ClientError, __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, __version__ as client_version)


def likeFollowersPhoto(user_id, follower):
    try:
        photo_id = selectPhotoToLike(user_id, follower)
        if not photo_id:
            continue
        api.post_like(photo_id)
        print(
            "Photo liked! Waiting {}secs to like again.."
                .format(sleep_time)
        )
        time.sleep(sleep_time)
        return True
    except ClientError:
        print('API Error')
    except KeyboardInterrupt:
        print('Liked:' + str(like_count))
        raise
    except:
        print('Liked:' + str(like_count))
        raise


def selectPhotoToLike(user_id, follower):
    print(
        "[From: {}][User: {}] Getting User Feed..."
            .format(str(user_id), str(follower))
    )
    users_media = api.user_feed(follower, extract=True)
    items_len = len(users_media.get('items', []))
    if not items_len:
        return
    rand_photo = randint(0, 3)
    rand_photo = min(items_len - 1, rand_photo)
    photo_id = users_media.get('items')[rand_photo].get('id')
    print('Selected photo to like...')
    return photo_id


def loadConfig():
    with open('liker.json') as f:
        return json.load(f)
    return {}



config = loadConfig()
username = config['username']
password = config['password']
sleep_time = config['sleep_time']
users = config['account_ids']

print('Logging into Instagram')
api = Client(username, password)

like_count = 0

for user_id in users:
    followers = []
    results = api.user_followers(user_id)
    followers.extend(results.get('users', []))

    next_max_id = results.get('next_max_id')
    while next_max_id:
        results = api.user_followers(user_id, max_id=next_max_id)
        followers.extend(results.get('users', []))
        next_max_id = results.get('next_max_id')

        followers = [u['pk'] for u in followers]
        for follower in followers:
            photo_liked = likeFollowersPhoto(user_id, follower)
            if photo_liked:
                like_count += 1

print('Liked:' + str(like_count))
