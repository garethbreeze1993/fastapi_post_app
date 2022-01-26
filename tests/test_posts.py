import pytest
from typing import List
from app.schemas import PostOut, Post


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    expected_posts = [PostOut(Post=post, votes=0) for post in test_posts]
    # post_list_from_response = [PostOut(**res_post) for res_post in res.json()]
    assert res.status_code == 200
    assert len(res.json()) == len(expected_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_authorized_user_get_one_posts_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/999')
    assert res.status_code == 404


def test_authorized_user_get_one_posts_post_does_exist(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 200
    post = PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [('awesome new title', 'awesome_new_content', True),
                                                       ('fav pizza', 'peperoini', False),
                                                       ('fav singer', 'george michael', True)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post('/posts/', json={'title': title, 'content': content, 'published': published})
    assert res.status_code == 201
    created_post = Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user.get('id')


def test_create_post_default_published(authorized_client, test_user, test_posts):
    title = 'New title of this test'
    content = 'New content for tbis test'
    res = authorized_client.post('/posts/', json={'title': title, 'content': content})
    assert res.status_code == 201
    created_post = Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published is True
    assert created_post.owner_id == test_user.get('id')


def test_unauthorized_user_create_post(client, test_posts):
    title = 'New title of this test'
    content = 'New content for tbis test'
    res = client.post('/posts/', json={'title': title, 'content': content})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_authorized_user_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204


def test_authorized_user_delete_post_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/8888')
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert test_posts[3].owner_id != test_user['id']
    assert res.status_code == 403


def test_update_post_success(authorized_client, test_user, test_posts):
    title = 'New title of this test'
    content = 'New content for tbis test'
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json={'title': title, 'content': content})
    assert res.status_code == 200
    updated_post = Post(**res.json())
    assert updated_post.title == title
    assert updated_post.content == content
    assert updated_post.id == test_posts[0].id


def test_update_post_other_user_fail(authorized_client, test_user, test_posts):
    title = 'New title of this test'
    content = 'New content for tbis test'
    assert test_posts[3].owner_id != test_user['id']
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json={'title': title, 'content': content})
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    title = 'New title of this test'
    content = 'New content for tbis test'
    res = client.put(f'/posts/{test_posts[0].id}', json={'title': title, 'content': content})
    assert res.status_code == 401


def test_update_post_not_found(authorized_client, test_user, test_posts):
    title = 'New title of this test'
    content = 'New content for tbis test'
    res = authorized_client.put(f'/posts/9999', json={'title': title, 'content': content})
    assert res.status_code == 404
