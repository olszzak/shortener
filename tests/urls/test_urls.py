def test_post_url(db_session, url_app):
    response = url_app.post("/urls", json={"url": "https://x.com/"})
    assert response.status_code == 201

def test_post_url_2(db_session, url_app):
    response1 = url_app.post("/urls", json={"url": "https://x.com/"})
    assert response1.status_code == 201

    response2 = url_app.post("/urls", json={"url": "https://x.com/"})
    assert response2.status_code == 201

    assert response1.json()["id"] == response2.json()["id"]

def test_get_url(db_session, url_app):
    response1 = url_app.post("/urls", json={"url": "https://x.com/"})
    assert response1.status_code == 201

    response2 = url_app.get(f"/stats/{response1.json()['id']}")
    assert response2.json()["count"] == 0

    url_app.get(f"/urls/{response1.json()['id']}")

    response4 = url_app.get(f"/stats/{response1.json()['id']}")
    assert response4.json()["count"] == 1
