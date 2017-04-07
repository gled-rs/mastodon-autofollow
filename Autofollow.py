from mastodon import Mastodon
import json
import os

FIRST_RUN=False
DEBUG=False
INSTANCE='https://mastodon.host'

# Register app - only once!
if FIRST_RUN or not os.path.exists('.pytooter_clientcred.txt'):
	Mastodon.create_app(
	     'autofollower',
	      to_file = '.pytooter_clientcred.txt',
	      api_base_url=INSTANCE
	)
	username=raw_input('What is the username ?')
	password=raw_input('What is the password ?')

	mastodon = Mastodon(client_id = '.pytooter_clientcred.txt',api_base_url=INSTANCE)
	mastodon.log_in(
	    username,
	    password,
	    to_file = '.pytooter_usercred.txt'
	)

## Create actual instance
mastodon = Mastodon(
    client_id = '.pytooter_clientcred.txt',
    access_token = '.pytooter_usercred.txt',
    api_base_url=INSTANCE
)


if os.path.exists('.Autofollow.state.json'):
	with open('.Autofollow.state.json','r') as file:
		runparams=json.load(file)
else:
	runparams={'since_id':0}

my_id = mastodon.account_search('@followbot')[0]['id']

if DEBUG:
    print('Found my id %i' % my_id)

my_followed = mastodon.account_following(my_id)
my_followed_list=[my_id]
total_followed=0
for user in my_followed:
    my_followed_list.append(user['id'])
    total_followed+=1

if DEBUG:
    print('I am currently already following %i persons' % total_followed)

toots = mastodon.timeline_public(since_id=runparams['since_id'])
new_followed=0
for toot in toots:
    user_id = toot['account']['id']
    if DEBUG:
        print('[%i] new Toot from %i' % (toot['id'],user_id))
    runparams['since_id'] = toot['id']
    if user_id not in my_followed_list:
        if DEBUG:
            print('Trying to follow %i' % user_id)
        new_followed+=1
        mastodon.account_follow(user_id)
        my_followed_list.append(user_id)


with open('.Autofollow.state.json','w') as file:
        json.dump(runparams,file)

if new_followed > 0:
    mastodon.toot('I am now following %i new users, for a total of %i.' % (new_followed,total_followed+new_followed))
