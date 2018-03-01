from collections import namedtuple

Point = namedtuple("Point", "x y")
Car = namedtuple("Car", "x y free")
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

# M Threshold and A Threshold control sensitivity of closeEnough
# Increasing them will result in more rides being considered "close enough"
def closeEnough(car, ride, current, m_thresh, a_thresh):

  pickup_distance = distance(car, ride.start)
  trip_distance = distance(ride.start, ride.end)
  if (ride.latest < current + pickup_distance):
    return False
  if (trip_distance < pickup_distance * m_thresh):
    return False
  if (pickup_distance * m_thresh + a_thresh < (ride.begin - current)):
    return False
  return True

def candidateRides(car, rides, current, m_thresh, a_thresh):
  crs = [ride for ride in rides if closeEnough(car, ride, current, m_thresh, a_thresh)]
  # Increase thresholds if not enough values found
  if len(crs) < 2:
     return candidateRides(car, rides, current, m_thresh*2, a_thresh*2)
  else:
    return crs

# Simple value for a given ride, car, and on_time_points
# Higher is better

def base_value(car, ride, current):
  if (ride.begin < current):
    return 0
  trip_distance = distance(ride.start, ride.end)
  pickup_distance = distance(ride.start, car)
  pickup_time = ride.begin - current
  elapsed = max(pickup_distance, pickup_time) + trip_distance
  pickup_points = B if pickup_distance <= pickup_time else 0
  on_time_points = trip_distance if (current + elapsed) < ride.finish else 0
  return (pickup_points + on_time_points) / elapsed

# Parse input

lines = [line.rstrip("\n") for line in open("b_should_be_easy.in")]
R, C, F, N, B, T = [int(x) for x in lines[0].split(" ")]
rides = [ride(line) for line in lines[1:]]
cars = [Car(0, 0, 0) for x in range(F)]
time = 0

cr = candidateRides(cars[0], rides, 0, 1, 2)
bestRide = max(cr, key=lambda x: base_value(cars[0], x, time))

print([base_value(cars[0], ride, time) for ride in rides])
print([base_value(cars[0], ride, time) for ride in cr])
print(base_value(cars[0], bestRide, time))
