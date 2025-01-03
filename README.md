# File Sharing Ultra Modified Version With Shortener By Hunters

![image](https://github.com/Sahil0976/Multi-ForceSub_3buttons/assets/97865856/f590a80a-f80c-40bb-b583-a6e114122f3d)

## A Telegram File sharing bot you can access files through specific links..

##

Made Under - [@Anime_X_Hunters](https://t.me/Anime_X_Hunters).



### Features
- Fully customisable.
- Two Force Sub Channels added By - [SAHIL](https://t.me/Okabe_xRintarou)
- Customisable welcome & Forcesub messages.
- Customisable Pics
- Shortener feature added
- More than one Posts in One Link.
- Can be deployed on heroku directly.
- Can be deployed on Koyeb Either

### Setup

- Add bot to Database Channel with all permission
- Add bot to ForceSub channel as Admin with Invite Users via Link Permission if you enabled ForceSub 

##
### Installation
#### Deploy on Heroku
**BEFORE YOU DEPLOY ON HEROKU, YOU SHOULD FORK THE REPO AND CHANGE ITS NAME TO ANYTHING ELSE**<br>
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)</br>

##
## Installation
#### Deploy on Render
<b>BEFORE DEPLOY ON RENDER, FORK REPO EDIT CONFIG, CREATE NEW WEB-SERVICE ADD VARIABLES AND ADD MONITOR THATS IT</b>

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

##
#### Deploy in your VPS
````bash
git clone https://github.com/<github-username>/<reponame>
cd <repo name>
# Make sure to remove "<>" symbols
pip3 install -r requirements.txt
# Add all values in config.py properly
python3 main.py
````
##
#### Deploy in your VPS if Repository was Private
````bash
git clone https://<your-github-private-token>:x-oauth-basic@github.com/<github-username>/<repo-name>
cd <repo name>
# Make sure to remove "<>" symbols
pip3 install -r requirements.txt
# Add all values in config.py properly
python3 main.py
````

### Admin Commands

```
start - start the bot or get posts
my_plan - To Check your plan
request - Premium users can request their Fav content
batch - create link for more than one posts
genlink - create link for one post
users - view bot statistics
broadcast - broadcast any messages to bot users
stats - checking your bot uptime
about - about bot
help - help regarding bot
add_premium - (Owner Only) To add Admins
remove_premium - (Owner Only) Delete Admins
list_premium - (Owner Only) Show Admin List
```

### Variables

* `API_HASH` Your API Hash from my.telegram.org
* `APP_ID` Your API ID from my.telegram.org
* `TG_BOT_TOKEN` Your bot token from @BotFather
* `OWNER_ID` Must enter Your Telegram Id
* `CHANNEL_ID` Your Channel ID eg:- -100xxxxxxxx
* `DB_URL` Your mongo db url
* `DB_NAME` Your mongo db session name
* `ADMINS` Optional: A space separated list of user_ids of Admins, they can only create links
* `START_MSG` Optional: start message of bot, use HTML and <a href='https://github.com/codexbotz/File-Sharing-Bot/blob/main/README.md#start_message'>fillings</a>
* `FORCE_SUB_MESSAGE`Optional:Force sub message of bot, use HTML and Fillings
* `FORCE_CHANNEL` Optional: ForceSub Channel ID, leave 0 if you want disable force sub
* `FORCE_CHANNEL2` Optional: ForceSub Channel ID, leave 0 if you want disable force sub
* `PROTECT_CONTENT` Optional: True if you need to prevent files from forwarding

### Extra Variables

* `CUSTOM_CAPTION` put your Custom caption text if you want Setup Custom Caption, you can use HTML and <a href='https://github.com/CodeXBotz/File-Sharing-Bot/blob/main/README.md#custom_caption'>fillings</a> for formatting (only for documents)
* `DISABLE_CHANNEL_BUTTON` Put True to Disable Channel Share Button, Default if False
* `BOT_STATS_TEXT` put your custom text for stats command, use HTML and <a href='https://github.com/codexbotz/File-Sharing-Bot/blob/main/README.md#custom_stats'>fillings</a>
* `USER_REPLY_TEXT` put your text to show when user sends any message, use HTML


### Fillings
#### START_MESSAGE | FORCE_SUB_MESSAGE

* `{first}` - User first name
* `{last}` - User last name
* `{id}` - User ID
* `{mention}` - Mention the user
* `{username}` - Username

#### CUSTOM_CAPTION

* `{filename}` - file name of the Document
* `{previouscaption}` - Original Caption

#### CUSTOM_STATS

* `{uptime}` - Bot Uptime


### Licence
[![GNU GPLv3 Image](https://www.gnu.org/graphics/gplv3-127x51.png)](http://www.gnu.org/licenses/gpl-3.0.en.html)
##

   **Star this Repo if you Liked it ⭐⭐⭐**

