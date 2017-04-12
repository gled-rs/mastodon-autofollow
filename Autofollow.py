from mastodon import Mastodon
import json
import os

FIRST_RUN=False
DEBUG=False
INSTANCE='https://mastodon.host'

BLACKLIST = {
        'users':['b@icosahedron.website','katiekats@community.highlandarrow.com','Elizafox@mst3k.interlinked.me','hatf@mastodon.cloud','hatf@cybre.space','xial@ninetailed.uk','lopatto@mastodon.xyz'],
        'instances':['icosahedron.website','slime.global','toot.cat','postgrestodon.magicannon.com','toot.cafe','cmpwn.com']
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
    INSTANCE=raw_input('What is your instance ?')
    botname=raw_input('What is your botname ?')

    mastodon = Mastodon(client_id = '.pytooter_clientcred.txt',api_base_url=INSTANCE)
    mastodon.log_in(
        username,
        password,
        to_file = '.pytooter_usercred.txt'
    )

if os.path.exists('.Autofollow.state.json'):
    with open('.Autofollow.state.json','r') as file:
        runparams=json.load(file)
else:
    runparams={'since_id':0,'botname':botname}

if 'instance' in runparams:
    INSTANCE=runparams['instance']
else:
    runparams['instance'] = INSTANCE

## Create actual instance
mastodon = Mastodon(
    client_id = '.pytooter_clientcred.txt',
    access_token = '.pytooter_usercred.txt',
    api_base_url=INSTANCE
)

if 'runcount' not in runparams:
    runparams['runcount'] = 1
else:
    runparams['runcount']+=1

if 'my_id' not in runparams:
    my_id = mastodon.account_search(runparams['botname'])[0]['id']
    runparams['my_id'] = my_id
else:
    my_id = runparams['my_id']

if DEBUG:
    print('Found my id %i' % my_id)

my_followed = mastodon.account_following(my_id)
my_followed_list=[my_id]
total_followed=0
for user in my_followed:
    if 'id' in user:
        my_followed_list.append(user['id'])
        total_followed+=1

if 'list_seen' not in runparams:
    runparams['list_seen'] = my_followed_list

if DEBUG:
    print('I am currently already following %i persons' % total_followed)

toots = mastodon.timeline_public(since_id=runparams['since_id'],limit=40)
if DEBUG:
    print('Found %i toots using since_id %i' % (len(toots),runparams['since_id']))
new_followed=0
new_user_list=[]
with open('.toots_followed.log','a') as f:
    for toot in toots:
        if DEBUG:
            print('Toot: %s' % toot)
        if toot != 'error':
            #try:
            if 'account' in toot:
                if '@' in toot['account']['acct']:
                    instance_domain = toot['account']['acct'].split('@')[1]
                else:
                    instance_domain=INSTANCE
                if toot['account']['acct'] not in BLACKLIST['users'] \
                        and instance_domain not in BLACKLIST['instances'] \
                        and ('#followme' in toot['account']['note'] or '#<span>followme</span>' in toot['account']['note']):
                    new_user_list.append(toot['account']['id'])
                    f.write("Toot:%s\n" % json.dumps(toot))
                if len(toot['mentions']) > 0:
                    for mention in toot['mentions']:
                        if '@' in mention['acct']:
                            mention_domain=mention['acct'].split('@')[1]
                        else:
                            mention_domain=INSTANCE
                        if mention['acct'] not in BLACKLIST['users'] \
                                and mention_domain not in BLACKLIST['instances'] \
                                and ('#followme' in toot['account']['note'] or '#<span>followme</span>' in toot['account']['note']):
                            new_user_list.append(mention['id'])
                            f.write("Mention:%s\n" % json.dumps(mention))
            #except:
            #    print('Error while trying to do something with %s' % (toot))
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
    mastodon.status_post('I am now following %i users out of the %i I have seen, boost some toots from others so I can see them :)' % (total_followed+new_followed,len(runparams['list_seen'])),visibility='unlisted')
    runparams['runcount'] = 1

with open('.Autofollow.state.json','w') as file:
        json.dump(runparams,file)
