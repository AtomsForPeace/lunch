#!/usr/bin/python
# -*- coding: utf-8 -*-
# File name: app.py

import json
from operator import itemgetter
from sanic import Sanic
from sanic import response
from websockets import ConnectionClosed


app = Sanic(__name__)
app.static('/static', './static')


restaurant_dict = {
    'Bares': 0,
    'Lassi': 0,
    'Inder': 0,
    'Haltestelle': 0,
    'Tuerker': 0,
    'Bild': 0,
    'Schroedi': 0,
    'Burger': 0,
    'Gruen/Grau': 0,
    'Audi': 0,
    'Pinse': 0,
}
clients = {}
voters = {r: set() for r in restaurant_dict}


@app.route('/')
@app.route('/index')
async def index(request):
    return await response.file('index.html')


@app.route('/restaurants')
async def restaurants(request):
    return response.text(json.dumps({
        'message': sorted(
            restaurant_dict.items(),
            key=itemgetter(1),
            reverse=True),
        'status': 200
        }
    ))


@app.websocket('/update/')
async def update(request, ws):
    while True:
        data = json.loads(await ws.recv())
        restaurant = None
        client_id = request.ip
        if data['message'] == 'online':
            clients[client_id] = ws
        else:
            restaurant = data['message']
            await handle_vote(ws, restaurant, client_id)


async def handle_vote(ws, restaurant, hostname):
    this_vote = voters.get(restaurant)
    if hostname not in this_vote:
        voters[restaurant].add(hostname)
        restaurant_dict[restaurant] += 1
        for client in clients.values():
            try:
                await client.send(restaurant)
            except ConnectionClosed:
                del clients[client]
    else:
        await ws.send('406')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
