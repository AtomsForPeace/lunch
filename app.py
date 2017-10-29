#!/usr/bin/python
# -*- coding: utf-8 -*-
# File name: app.py

import json
from socket import gethostname
from operator import itemgetter
from sanic import Sanic
from sanic import response


app = Sanic(__name__)


restaurant_dict = {
    'Bares': 0,
    'Lassi': 0,
    'Inder': 0,
    'Haltestelle': 0,
    'Tuerker': 0,
    'Bild': 0,
    'Schroedi': 0,
    'Burger': 0,
    'Gruene': 0,
    'Audi': 0,
}


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
        restaurant = await ws.recv()
        hostname = gethostname()
        this_vote = voters.get(restaurant)
        if not this_vote:
            if hostname not in this_vote:
                voters[restaurant].add(hostname)
                restaurant_dict[restaurant] += 1
                await ws.send(restaurant)
        else:
            await ws.send('406')


if __name__ == '__main__':
    app.run()
