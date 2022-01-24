from typing import List
from app.schemas import PostOut


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    expected_posts = [PostOut(Post=post, votes=0) for post in test_posts]
    # post_list_from_response = [PostOut(**res_post) for res_post in res.json()]
    assert res.status_code == 200
    assert len(res.json()) == len(expected_posts)
