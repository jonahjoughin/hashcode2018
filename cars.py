from collections import namedtuple

Point = namedtuple("Point", "x y")
Ride = namedtuple("Ride", "start latest end begin finish")

def distance(p1, p2):
  return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def ride(line):
  data = [int(x) for x in line.split(" ")]
  start = Point(data[0], data[1])
  end = Point(data[2], data[3])
  begin = data[4]
  finish = data[5]
  latest = finish - distance(start, end)
  return Ride(start, latest, end, begin, finish)

def closeEnough(car, ride, current, thresh):

  pickup_distance = distance(car, ride.start)
  trip_distance = distance(ride.start, ride.end)
  if (ride.latest < current + pickup_distance):
    return False
  if (trip_distance < pickup_distance * thresh):
    return False
  if (pickup_distance * thresh < (ride.begin - current)):
    return False
  return True

def candidateRides(car, rides, current, thresh):
  return [ride for ride in rides if closeEnough(car, ride, current, thresh)]

def base_cost(car, ride, current):
  if (ride.begin < current):
    return None
  trip_distance = abs(ride.end.x - ride.start.x) + abs(ride.end.y - ride.start.y)
  pickup_distance = abs(car.x - ride.start.x) + abs(car.y - ride.start.y)
  pickup_time = ride.begin - current
  elapsed = max(pickup_distance, pickup_time) + trip_distance
  pickup_points = B if pickup_distance <= pickup_time else 0
  on_time_points = elapsed if (current + elapsed) < ride.finish else 0
  return (pickup_points + on_time_points) / elapsed

lines = [line.rstrip("\n") for line in open("a_example.in")]
R, C, F, N, B, T = [int(x) for x in lines[0].split(" ")]
rides = [ride(line) for line in lines[1:]]

cars = [Point(0,0) for x in range(F)]
cr = candidateRides(cars[0], rides, 0, 1)
print(cr)
#print(rides)
