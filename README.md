yt-dlp telegram bot
===

This is a telegram bot that downloads the requested media from
YouTube, TikTok, Instagram, etc.

The installation includes a [telegram bot api server](https://github.com/tdlib/telegram-bot-api), [yt-dlp](https://github.com/yt-dlp/yt-dlp) and some additional tools
for the latter ([deno](https://github.com/denoland/deno),
[curl-impersonate](https://github.com/lexiforest/curl-impersonate)).

Everything is packed into the docker compose.


Prerequisites
===

Obtain api key from Telegram
---

Telegram bot api is a piece of software that acts as a proxy (kinda) server between the bot and Telegram servers.
This allows to send bigger files (up to 2Gb) from a bot.

For telegram it is a client application that requires registering.
To do so please follow https://core.telegram.org/api/obtaining_api_id.

As the result you should get back `API_ID` and `API_HASH` which you fill into the `.env` (`TGBOTAPISRV_API_ID` and `TGBOTAPISRV_API_HASH` variables accordingly).


Create a new Telegram bot
---

The bot itself also requires registering.
It can be done in the Telegram messenger with the help of [@BotFather](https://t.me/BotFather).

More on that can be found [here](https://core.telegram.org/bots/features#botfather).

The result of registering a bot should be a token like `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`.
Please add it to the `.env` in the variable called `TGBOT_TOKEN`.


Build and run
===

The package uses the docker compose which should be installed.

When run first the docker images are going to be build which can take some time (5-10 minutes).

The command to run the app is:

```bash
$ docker-compose up -d
```


Usage
===

At the moment the bot requires sending an URL with the video.
This video will be downloaded and sent back to the user.

In case a text message is not recognized as an URL it will reply with the original text.
