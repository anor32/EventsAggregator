import pytest


@pytest.mark.asyncio
async def test_01_health_check(client):
    response = await client.get(url='/api/health/')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_02_manual_sync(client):
    response = await client.post('/api/sync/trigger')
    assert response.json() == {"msg": "success added"}


@pytest.mark.asyncio
async def test_03_get_events(client, pages_body):
    response = await client.get('/api/events', params=pages_body.model_dump())
    assert response.status_code == 200
    assert len(response.json()['results']) == 20


@pytest.mark.asyncio
async def test_05_get_event(client, event_id):
    response = await client.get(f'/api/events/{event_id}')
    assert response.status_code == 200
    assert response.json().get('event_time')


@pytest.mark.asyncio
async def test_06_get_seats(client, event_id):
    response = await client.get(f'/api/events/{event_id}/seats')
    assert response.status_code == 200 or response.status_code == 503
    if response.status_code ==200:
        assert  response.json().get('event_time')


@pytest.mark.asyncio
async def test_07_register(client,register_user):
    response = await client.post(f'/api/tickets',json=register_user.model_dump(mode='json'))
    assert response.status_code == 201
    assert response.json().get('ticket_id')



@pytest.mark.asyncio
async def test_08_unregister(client,register_user,ticket_id):
    response = await client.post(f'/api/tickets/{ticket_id}',json=register_user.model_dump(mode='json'))
    assert response.status_code == 200
    assert response.json().get('ticket_id')
