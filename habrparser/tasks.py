import asyncio
import urllib.parse

import aiohttp
from bs4 import BeautifulSoup
from celery import shared_task

from habrparser.models import Article

BASE_URL = "https://habr.com"


async def send_response(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse(html: str):
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all(class_="tm-article-snippet")

    for article in articles:
        author_block = article.find("a", class_="tm-user-info__username")
        author_username = author_block.get_text()
        author_link = author_block["href"]

        time = article.find("time")["datetime"]

        title_block = article.find("a", class_="tm-title__link")
        link = title_block["href"]
        title = title_block.get_text()

        full_link = urllib.parse.urljoin(BASE_URL, link)
        soup = BeautifulSoup(await send_response(full_link), "html.parser")

        text = "".join(
            [str(i) for i in soup.find(id="post-content-body").children],
        )

        Article.objects.create(
            title=title,
            link=link,
            date=time,
            author=author_username,
            author_link=author_link,
            text=text,
        )


@shared_task
def parse_habr_task(hub_title: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(
        send_response(f"{BASE_URL}/ru/hubs/{hub_title}/articles/"),
    )
    response = loop.run_until_complete(task)
    loop.run_until_complete(parse(response))
    loop.close()
