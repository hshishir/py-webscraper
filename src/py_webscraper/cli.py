from seleniumwire import webdriver
from seleniumwire.utils import decode as decodesw
from urllib.parse import urlparse
import click
import json
import re
import requests


@click.group()
def runcli():
    """Simple command line tool"""


@runcli.command("parseurl")
@click.option("--filename", "-fname", type=str, default="url-links.txt")
def run_parseurl(filename: str) -> None:
    keywords = ["/api/"]
    tags = []
    url_tags = {}
    domain_tags = {}
    target_urls = get_urls_list(filename)

    for target_url in target_urls:
        tags.clear()
        driver = webdriver.Firefox(seleniumwire_options={"disable_encoding": True})
        print(f"====Parsing url: {target_url}")

        urls = get_request_urls(driver, target_url)
        responses = get_response_jsonable(driver, target_url)

        for url in urls:
            for kw in keywords:
                if kw in url["url"]:
                    print(f"[keyword {kw}], url {url}")
                    tags.append("#api")

        domain_name = get_domain_name(target_url)
        json_filename = f"{domain_name}.json"
        with open(json_filename, "w") as f:
            json.dump(responses, f)

        u_tags = set(tags)
        url_tags[target_url] = "".join(u_tags)
        domain_tags[domain_name] = "".join(u_tags)
        print(f"Url: {target_url}, Tags: {u_tags}")

        driver.close()
    with open("domain-tags.txt", "w") as file:
        for key, value in domain_tags.items():
            file.write(f"{key} = {value} \n")
    print(url_tags)


def get_domain_name(url: str) -> str:
    pattern = r"(?P<domain>[\w\-]+\.+[\w\-]+)"
    match = re.search(pattern, url)
    domain = match.group("domain")
    return domain


def get_urls_list(filename: str) -> list:
    urls = []
    with open(filename, "r") as file:
        line = file.readline()
        while line:
            urls.append(line)
            line = file.readline()
    return urls


def search_keywords_response(target_url: str) -> None:
    response = requests.get(target_url)


def get_request_urls(driver: webdriver, target_url: str) -> list:
    driver.get(target_url)
    urls = []
    urls.append({"url": target_url})
    for request in driver.requests:
        urls.append({"url": request.url})
    return urls


def get_response_jsonable(driver: webdriver, target_url: str):
    driver.get(target_url)
    responses = []

    for request in driver.requests:
        try:
            data = decodesw(
                request.response.body,
                request.response.headers.get("Content-Encoding", "identity"),
            )
            response = json.loads(data.decode("utf-8"))
            responses.append(response)
        except:
            pass
    return responses


if __name__ == "__main__":
    runcli()
