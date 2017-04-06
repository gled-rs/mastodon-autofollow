from mastodon import Mastodon
import json
import os

FIRST_RUN=False
INSTANCE='https://mastodon.pericles.world'

# Register app - only once!
if FIRST_RUN or not os.path.exists('.pytooter_clientcred.txt'):
	Mastodon.create_app(
	     'autofollower',
	      to_file = '.pytooter_clientcred.txt',
	      api_base_url=INSTANCE
	)
	username=input('What is the username ?')
	password=input('What is the password ?')

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

#mastodon.toot('Fetching new users to follow on the timeline...')

if os.path.exists('.Autofollow.state.json'):
	with open('.Autofollow.state.json','r') as file:
		runparams=json.load(file)
else:
	runparams={'since_id':0}

my_id = mastodon.account_search('@followbot')[0]['id']
my_followed = mastodon.account_following(my_id)

print(json.dumps(my_followed))

toots = mastodon.timeline_public(since_id=runparams['since_id'])
for toot in toots:
	#print(json.dumps(toot))
	user_id = toot['account']['id']
	runparams['since_id'] = toot['id']
	mastodon.account_follow(user_id)


#with open('.Autofollow.state.json','w') as file:
#	json.dump(runparams,file)
