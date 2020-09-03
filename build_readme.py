import feedparser
import json
import pathlib
import re
import os
import time

root = pathlib.Path(__file__).parent.resolve()

def fetch_blog_entries():
    entries = feedparser.parse("https://markushatvan.com/rss.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published":  time.strftime('%Y-%m-%d', entry["published_parsed"]),
        }
        for entry in entries
    ]

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()

    entries = fetch_blog_entries()[:5]
    print(entries)

    entries_md = "\n".join(
        ["- [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )

    rewritten = replace_chunk(readme_contents, "blog", entries_md)
    readme.open("w").write(rewritten)
