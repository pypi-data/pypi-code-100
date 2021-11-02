from typing import List
from tuat_feed.post import Post
import requests


def fetch(
    category: str = "all", url: str = "https://api.ihavenojob.work/tuat/"
) -> List[Post]:
    """投稿の取得

    Parameters
    ----------
    category : str, optional
        取得する投稿の種類。"all","campus","academic"。デフォルトでは"all"。
    url : str, optional
        データを取得するAPIのURL、デフォルトでは"https://api.ihavenojob.work/tuat/"

    Returns
    -------
    List[Post]
        投稿の一覧

    Raises
    ------
    ValueError
        categoryに規定外の入力があった場合
    """

    if category == "all":
        response = requests.get(url)
    elif category == "academic":
        response = requests.get(url + "academic")
    elif category == "campus":
        response = requests.get(url + "campus")
    else:
        raise ValueError(
            f'category must be one of "all", "academic" or "campus". {category} was supplied.'
        )

    feed = response.json()
    posts = []
    for p in feed:
        posts.append(Post.parse_post(p))
    return posts
