#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import asyncio
import concurrent.futures
import itertools
import logging
import os
import yt_dlp

from yt_dlp.postprocessor.ffmpeg import FFmpegVideoConvertorPP
from urllib.parse import urlparse
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

class MyConvertorPP(FFmpegVideoConvertorPP):
    def get_param(self, name, default=None, *args, **kwargs):
        if "postprocessor_args" == name:
            return ["-crf", "26", "-c:v", "libx264"]
        return super().get_param(name, default, *args, **kwargs)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

ydl_opts = {
    "noprogress": True,
    "format": "bv*[filesize_approx<1800M]+ba/b[filesize<2000M]",
}

progress_list = [
    chr(0x1F311),
    chr(0x1F318),
    chr(0x1F317),
    chr(0x1F316),
    chr(0x1F315),
    chr(0x1F314),
    chr(0x1F313),
    chr(0x1F312),
    chr(0x1F311),
    chr(0x1F312),
    chr(0x1F313),
    chr(0x1F314),
    chr(0x1F315),
    chr(0x1F316),
    chr(0x1F317),
    chr(0x1F318),
]

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(rf"Hi {user.mention_html()}!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def progress_co(msg):
    try:
        for p in itertools.cycle(progress_list):
            msg = await msg.edit_text(f"Processing... {p}")
            await asyncio.sleep(1)
    finally:
        await msg.delete()


def download(url: str) -> str:
    loop = asyncio.get_running_loop()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.add_post_processor(MyConvertorPP(preferedformat="mp4"))
        return loop.run_in_executor(executor, ydl.extract_info, url, True)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    logger.warning(update.message.chat)
    parsed = urlparse(update.message.text)
    if parsed.scheme and parsed.netloc:
        loop = asyncio.get_running_loop()
        progress_msg = await update.message.reply_text("Processing...")
        progress_task = asyncio.create_task(progress_co(progress_msg))
        try:
            fileinfo = await download(update.message.text)
            try:
                await update.message.reply_video(fileinfo["requested_downloads"][0]["filepath"],
                    duration=fileinfo["duration"],
                    width=fileinfo["requested_downloads"][0]["width"],
                    height=fileinfo["requested_downloads"][0]["height"],
                    cover=fileinfo["thumbnail"],
                    caption=fileinfo["title"][:1024],
                    read_timeout=300, write_timeout=300)
                progress_task.cancel()
            finally:
                await loop.run_in_executor(executor, os.unlink, fileinfo["requested_downloads"][0]["filepath"])
        except Exception as e:
            logger.warning("Unable to finalize the request", e)
            progress_task.cancel()
            await update.message.reply_text("Unable to finalize the request")
    else:
        await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = (Application.builder()
                              .base_url("http://tgbotapi:8081/bot")
                              .token(os.getenv("TOKEN"))
                              .concurrent_updates(True)
                              .build())

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

