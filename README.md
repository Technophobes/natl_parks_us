# natl_parks_visits
USA National Parks by Location and Visitation Numbers

Install: `pip3 install rq redis`

To start Redis install docker desktop and run `docker run -p6379:6379 redis`.


To start the worker: `rq worker parks`

The worker runs the function `park_queue.add_park_from_queue` on every item that gets put in the queue.

The api "park" POST endpoint puts the request data on the queue.

Source: https://data.world/inform8n/us-national-parks-visitation-1904-2016-with-boundaries