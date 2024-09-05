# Courses Bot
![Screenshot_8](https://github.com/user-attachments/assets/4f28d016-5567-40f2-9330-30da51c60e68)

## About
When a student unregisters from a course, a vacant seat opens up, but the vacancy isn't instantly filled by students from the waitlist. Based on my experience, there's often a long grace period (sometimes lasting hours) before the vacancy is filled. During this time, anyone can register directly, bypassing the waitlist. After discovering paid services that exploit this loophole, I found it to be an interesting flaw in the system. This curiosity led me to create a Discord bot to explore the concept further.

## Technologies
* `discord.py` for bot development
* `BeautifulSoup4` for web scraping course seat status

## Commands and how to use them ##

* `*general <url>`  Pings once a general seat is available<br>
* `*any <url>`      Pings once a general or restricted seat is available<br>
* `*cancel`         Stops monitoring page<br>

Replace `<url>` with any valid UBC course URL.

## Limitations ##
The courses site allows crawlers, but I don't know how fast I'm allowed to poll without breaking the site's terms of use (I'm pretty much just guessing a polling rate). Other paid notifier services out there might be a few seconds faster, so if you have a good spot in the waitlist, be very careful.

Additionally, with the transition to Workday, the scraper will no longer work. I'm also not sure if the same flaw still exists.
