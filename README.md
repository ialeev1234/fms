In this docker-compose (use `docker-compose up` for running) placed 3 services.

- API (provides api for access to CRUD for cars and to driver's penalties, storing in the MongoDB collections)
- Dumper (dumps to drivers collection incoming tracking messages from RabbitMQ)
- Simulator (generates tracking messages for existing cars in the RabbitMQ)



API (available on IP 0.0.0.0)

We have resource /cars with GET/POST/PATCH/DELETE methods.
For creating car with car_id=1 we need to send POST with car_id=1.
We can update this car with driver_id via PATCH method.
List of all cars available on GET /cars.

Also, we have /assign endpoint for setting driver_id to car.

You can get penalties for all drivers via GET /drivers, 
or you can filter driver using GET parameter driver_id.

 
 
Simulator

Every 10 seconds takes all cars and generate random speed for each.



Dumper

Check speed and calculate penalty depending on value.


