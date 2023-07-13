# file = 'data.txt'
# alti = 20
def readWaypoints(filename, alti=20):
    with open(filename) as f:
        wps = f.readlines()
        wps = [x.replace("\n", "") for x  in wps]

        wps = [x.split(" ") for x in wps]
        wps = [[float(y) for y in x] for x in wps]
        for i,wp in enumerate(wps):
            wp.append(alti)
            wp.append(i)
        wps = [tuple(x) for x in wps]

        print(wps)
        # return wps

readWaypoints('waypointlist.txt')