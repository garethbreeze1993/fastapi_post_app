import pytest

from app import models


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Votes(post_id=test_posts[3].id, user_id=test_user.id)
    session.add(new_vote)
    session.commit()


def test_vote_up_on_post(authorized_client, test_user, test_posts):
    res = authorized_client.post('/vote/', json={'post_id': test_posts[3].id, 'vote_dir': 1})
    assert res.status_code == 201


def vote_twice_on_post(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post('/vote/', json={'post_id': test_posts[3].id, 'vote_dir': 1})
    assert res.status_code == 409


def vote_down_on_post(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post('/vote/', json={'post_id': test_posts[3].id, 'vote_dir': 0})
    assert res.status_code == 201


def test_vote_down_on_post_not_voted_on_fail(authorized_client, test_user, test_posts):
    res = authorized_client.post('/vote/', json={'post_id': test_posts[3].id, 'vote_dir': 0})
    assert res.status_code == 400


def test_vote_on_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.post('/vote/', json={'post_id': 9999, 'vote_dir': 1})
    assert res.status_code == 404


def test_vote_up_on_post_unauthenticated(client, test_user, test_posts):
    res = client.post('/vote/', json={'post_id': test_posts[3].id, 'vote_dir': 1})
    assert res.status_code == 401
