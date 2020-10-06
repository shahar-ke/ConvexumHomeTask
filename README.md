# ConvexumHomeTask

## usage
start server
```console
$ PYTHONPATH=[path/to/repo] python server_lib/drones_sensors_app.py
```
start sensor
```console
$ PYTHONPATH=[path/to/repo] python sensor_lib/sensor.py [path/to/repo]/task_def/drones.txt
```
sensor process will print each drone it senses

when sensor process is done, on server process drones history is printed

## requirements
```console
$ pip install -r requirements.txt
```
## solution overview

server was implemented with flask and python 3.8
sensor was implemented in python + thread for the async tracking of new drones

### sensor side
a sensor uses a driver which does the sense action async

sensor registers itself with server

sensor syncs with the driver queue to fetch next sensed drone

sensor reports to server new drone sensed, gets instruction, handles it, and reports final state to server

when sensor driver is done, sensor report to server it has shut down

### server side
sensor end point - registers a new sensor

found end point - receives a new drone, saves it to db and returns it's id

final end point - receives final drone state, saves to db

done - sensor reports it is done, prints and returns its history

server and underlying db schema was implemented to support multiple sensors


## project structure
- drone_data_lib - generic enums and DS to represents drone data and states, shared between server and sensor
- sensor_lib.com_utils - the server client, base class inherited by http and moc (for test) are implemented
- sensor_lib.drivers - contains sense drivers, base class inherited by file simulation are implemented
- sensor_lib.sensor.py - the sensor, initialized with com_util, and sensor_driver
- server_lib.db_layer - contains db config, models and client
- server_lib.end_points - the end points with receives requests from sensors, handles them, and responds
- server_lib.drones_manager.py - makes decisions what to do with reported drones
- server_lib.drones_sensor_app.py - server entry point
- task_def - drones.txt and task definition
- tests.sensor_tests - sensor test, uses moc com util to simulate server
- tests.server_tests - server test, intended to run when server is already online,
initialises file based sensor simulation, checks server response is as expected from drones.txt


## main things to improve
- dockerise solution for ease of deployment
- error handling on client side, asserts should be transformed to meaningful exceptions
- error handling on server side, asserts should be transformed to meaningful exceptions and return explicit 5xx/4xx 
status codes for server/client errors

fun stuff :)