from fastapi.testclient import TestClient


def ticket_payload(title: str = "API indisponible") -> dict[str, str]:
    return {
        "title": title,
        "description": f"Description de {title}",
    }


def test_create_ticket(client: TestClient):
    response = client.post("/v1/tickets/", json=ticket_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "API indisponible"
    assert body["description"] == "Description de API indisponible"
    assert body["status"] == "open"
    assert body["created_at"]


def test_create_ticket_rejects_invalid_payload(client: TestClient):
    response = client.post(
        "/v1/tickets/",
        json={"title": "", "description": "Description"},
    )

    assert response.status_code == 422


def test_list_tickets_with_pagination(client: TestClient):
    for index in range(3):
        client.post("/v1/tickets/", json=ticket_payload(f"Ticket {index}"))

    response = client.get("/v1/tickets/", params={"limit": 1, "offset": 1})

    assert response.status_code == 200
    assert response.headers["X-Total-Count"] == "3"
    assert [ticket["title"] for ticket in response.json()] == ["Ticket 1"]


def test_list_tickets_rejects_invalid_pagination(client: TestClient):
    response = client.get("/v1/tickets/", params={"limit": 0, "offset": -1})

    assert response.status_code == 422


def test_get_ticket(client: TestClient):
    created = client.post("/v1/tickets/", json=ticket_payload()).json()

    response = client.get(f"/v1/tickets/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_unknown_ticket_returns_404(client: TestClient):
    response = client.get("/v1/tickets/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_update_ticket(client: TestClient):
    created = client.post("/v1/tickets/", json=ticket_payload()).json()
    payload = ticket_payload("Titre modifié")

    response = client.put(f"/v1/tickets/{created['id']}", json=payload)

    assert response.status_code == 200
    assert response.json()["title"] == "Titre modifié"
    assert response.json()["description"] == "Description de Titre modifié"


def test_update_unknown_ticket_returns_404(client: TestClient):
    response = client.put("/v1/tickets/999", json=ticket_payload())

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_close_ticket(client: TestClient):
    created = client.post("/v1/tickets/", json=ticket_payload()).json()

    response = client.patch(f"/v1/tickets/{created['id']}/close")

    assert response.status_code == 200
    assert response.json()["status"] == "closed"


def test_close_already_closed_ticket_returns_400(client: TestClient):
    created = client.post("/v1/tickets/", json=ticket_payload()).json()
    client.patch(f"/v1/tickets/{created['id']}/close")

    response = client.patch(f"/v1/tickets/{created['id']}/close")

    assert response.status_code == 400
    assert response.json() == {"detail": "Ticket is already closed"}


def test_close_unknown_ticket_returns_404(client: TestClient):
    response = client.patch("/v1/tickets/999/close")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}
