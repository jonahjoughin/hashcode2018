from collections import namedtuple
import argparse

args = {}


parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i",help="Input file to read", required="true")
parser.add_argument("--output", "-o",help="Output file to write to", required="true")
args = parser.parse_args()
inputFile = args.input
outputFile = args.output


Point = namedtuple("Point", "x y")
Car = namedtuple("Car", "x y free id")
Ride = namedtuple("Ride", "start latest end begin finish id")

def distance(p1, p2):
  return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def ride(line, i):
  data = [int(x) for x in line.split(" ")]
  start = Point(data[0], data[1])
  end = Point(data[2], data[3])
  begin = data[4]
  finish = data[5]
  latest = finish - distance(start, end)
  return Ride(start, latest, end, begin, finish, i)

# M Threshold and A Threshold control sensitivity of closeEnough
# Increasing them will result in more rides being considered "close enough"
def closeEnough(car, ride, current, m_thresh, a_thresh):

  pickup_distance = distance(car, ride.start)
  trip_distance = distance(ride.start, ride.end)
  if (ride.latest < current + pickup_distance):
    return False
  if (trip_distance * m_thresh < pickup_distance):
    return False
  if (pickup_distance * m_thresh + a_thresh < (ride.begin - current)):
    return False
  return True

def candidateRides(car, rides, current, m_thresh, a_thresh):
  crs = [ride for ride in rides if closeEnough(car, ride, current, m_thresh, a_thresh)]
  # Increase thresholds if not enough values found
  if len(crs) < 1 and m_thresh < 1<<32 and a_thresh < 1<<32:
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

lines = [line.rstrip("\n") for line in open(inputFile)]
R, C, F, N, B, T = [int(x) for x in lines[0].split(" ")]
rides = [ride(line,i) for (i,line) in enumerate(lines[1:])]
cars = [Car(0, 0, 0, x) for x in range(F)]
time = 0

out = {car.id: [] for car in cars}

while time < T:
  if (len(cars) == 0):
    break
  for car in cars:
    cr = candidateRides(car, rides, 0, 1, 2)
    if (cr != []):
      bestRide = max(cr, key=lambda x: base_value(car, x, car.free))
      bestVal = base_value(car, bestRide, car.free)

      ######## Add in check here for whether this is a better car for this ride

      trip_distance = distance(bestRide.start, bestRide.end)
      pickup_distance = distance(bestRide.start, car)
      pickup_time = bestRide.begin - car.free

      ####### Add in check here to make sure we dont run out of time
      if (car.free + trip_distance + max(pickup_distance, pickup_time) < T):
        rides.remove(bestRide)
        car = Car(car.x, car.y, car.free + trip_distance + max(pickup_distance, pickup_time), car.id)
        if out[car.id] == None:
          out[car.id] == [bestRide.id]
        else:
          out[car.id].append(bestRide.id)
        print(bestVal)
      else:
        cars.remove(car)
      time = min(time, car.free)
    else:
      cars.remove(car)

f = open(outputFile, "w")
for key in out.keys():
  els = [str(key)]
  for val in out[key]:
    els.append(str(val))
  line = " ".join(els)+"\n"
  f.write(line)
