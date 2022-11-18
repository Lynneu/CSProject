import itertools
import DataInit

def held_karp(dists):
  n = len(dists)
  C = {}
  for k in range(1, n):
    C[(1 << k, k)] = (dists[0][k], 0)

  for subset_size in range(2, n):
    for subset in itertools.combinations(range(1, n), subset_size):
      # Set bits for all nodes in this subset
      bits = 0
      for bit in subset:
        bits |= 1 << bit

      # Find the lowest cost to get to this subset
      for k in subset:
        prev = bits & ~(1 << k)

        res = []
        for m in subset:
          if m == 0 or m == k:
            continue
          res.append((C[(prev, m)][0] + dists[m][k], m))
        C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
  bits = (2 ** n - 1) - 1

  # Calculate optimal cost
  res = []
  for k in range(1, n):
    res.append((C[(bits, k)][0] + dists[k][0], k))
  opt, parent = min(res)

  # Backtrack to find full path
  path = []
  for i in range(n - 1):
    path.append(parent)
    new_bits = bits & ~(1 << parent)
    _, parent = C[(bits, parent)]
    bits = new_bits

  # Add implicit start state
  path.append(0)
  route = list(reversed(path))
  route.append(0)

  return opt, route


def finalRoute(arr,dists):
  distance, route = held_karp(dists)
  routeLocation = DataInit.read_csv_lng_lat(arr,route)

  return distance, routeLocation

# if __name__ == '__main__':
#   arr = [1,16,5,15,6,0]
#   dists = DataInit.read_csv_distance(arr)
#   for row in dists:
#     print(''.join([str(n).rjust(4, ' ') for n in row]))
#   distance, route = held_karp(dists)
#   print(distance)
#   print(route)
