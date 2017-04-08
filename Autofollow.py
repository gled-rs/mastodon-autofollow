from mastodon import Mastodon
import json
import os

FIRST_RUN=False
DEBUG=False
INSTANCE='https://mastodon.host'

BLACKLIST = {
        'users':['b@icosahedron.website'],
        'instances':['icosahedron.website','slime.global']
        }

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

if 'runcount' not in runparams:
    runparams['runcount'] = 1
else:
    runparams['runcount']+=1

my_id = mastodon.account_search('@followbot')[0]['id']

if DEBUG:
    print('Found my id %i' % my_id)

my_followed = mastodon.account_following(my_id)
my_followed_list=[my_id]
total_followed=0
for user in my_followed:
    my_followed_list.append(user['id'])
    total_followed+=1

if 'list_seen' not in runparams:
    runparams['list_seen'] = my_followed_list

if DEBUG:
    print('I am currently already following %i persons' % total_followed)

toots = mastodon.timeline_public(since_id=runparams['since_id'],limit=40)
new_followed=0
new_user_list=[]
for toot in toots:
    if toot['account']['acct'] not in BLACKLIST['users'] and toot['account']['acct'].split('@')[1] not in BLACKLIST['instances']:
        new_user_list.append(toot['account']['id'])
    if len(toot['mentions']) > 0:
        for mention in toot['mentions']:
            if mention['acct'] not in BLACKLIST['users'] and mention['acct'].split('@')[1] not in BLACKLIST['instances']:
                new_user_list.append(mention['id'])
    runparams['since_id'] = toot['id']

for user_id in new_user_list:
    if user_id not in my_followed_list or user_id not in runparams['list_seen']:
        if DEBUG:
            print('Trying to follow %i' % user_id)
        new_followed+=1
        mastodon.account_follow(user_id)
        my_followed_list.append(user_id)
        runparams['list_seen'].append(user_id)

if new_followed > 0 and runparams['runcount'] > 10:
    mastodon.toot('I am now following %i users out of the %i I have seen, boost some toots from others so I add them :)' % (total_followed+new_followed,len(runparams['list_seen'])))
    runparams['runcount'] = 1

with open('.Autofollow.state.json','w') as file:
        json.dump(runparams,file)
