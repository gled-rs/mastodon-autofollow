# mastodon-autofollow
**Disclaimer**: follow bots put an undue burden of spam and traffic on the
network. It's better to let your instance grow organically. If you want follow
bots to follow you, put #followme in your profile.

Autofollow bot for mastodon, the first of its kind.

Simple bot that follows every new user it finds on the public timeline of an instance( except the blacklisted ones, or if the user has #nobot in his bio ).

The goal of such a bot is to help populating the federated timeline on the instance I am running with a more broad view of the fediverse.
This helps also small instances federating and gathering toots on the federated timeline, ensuring that your instance is not creating a validation loop or a echo chamber.

Do not mix this kind of bot for Mastodon with bots on twitter. Follow bots on Mastodon are a way to get instances populated with users from other instances, nothing else.

It's a proof of concept, but a working one.

please keep a link to the code here or your fork, in case a user wants to be added to the blacklist.

# dependancies:
- Mastodon.py ( with the pull request 24 if you want your count of followees to be accurate)

# launch.sh
Simple script that takes care of installing dependancie in virtualenv and launching the script.

use it in cron at your own pace after the first launch ( you need to launch manually ./launch.sh first before using cron )

Example:
*/2	*	*	*	* cd /home/mastodon/mastodon-autofollow; ./launch.sh >> /home/mastodon/autofollow.log


# blacklist:

To users: if in your bio you have the keyword #nobot, this bot won't try to follow you !

If you use this code, please respect the wishes of the person this bot will follow. Some don't want to be bothered, some instances don't want
a followbot to bother them, respect them and either contact me ( @gled@mastodon.host ) or do a Pull Request to add your blacklist to the list.
The blacklist is in Autofollow.py, variable BLACKLIST
