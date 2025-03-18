import random
import math
import pprint
import csv
from random import randrange
import matplotlib.pyplot as plt
import solution_checker
import time

start_time = time.time()
random.seed(40)
pro = 8

def solution_to_csv(filename, profit, truck_list):
    solution_file = open(filename, 'w+')
    writer = csv.writer(solution_file)
    writer.writerow(["Total Profit"])
    writer.writerow([str(profit)])

    i = 0

    writer = csv.writer(solution_file, delimiter=" ")

    for truck in truck_list:
        row1 = "Route", i + 1
        writer.writerow(row1)
        writer.writerow(truck.customer_list)
        i += 1

    solution_file.close()


def distance_calc(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist


def relocate(ifirst, isecond, jfirst, jsecond, trucklist):
    possibleChange = trucklist[ifirst].customer_list[jfirst]
    del trucklist[ifirst].customer_list[jfirst]
    if ifirst == isecond:
        if jfirst < jsecond:
            trucklist[isecond].customer_list.insert(jsecond, possibleChange)
        else:
            trucklist[isecond].customer_list.insert(jsecond + 1, possibleChange)
    else:
        trucklist[isecond].customer_list.insert(jsecond + 1, possibleChange)


def findBestRelocationMove(truck_list, all_distances_calc, customer_list_id):

    maxGainCost = 0
    gainlist = []
    flag = False

    for ifirst in range(6):
        for isecond in range(6):
            for jfirst in range(1, len(truck_list[ifirst].customer_list) - 1):
                for jsecond in range(0, len(truck_list[isecond].customer_list) - 1):

                    if ifirst == isecond and (jfirst == jsecond or jsecond == jfirst - 1):
                        continue

                    possibleChange = truck_list[ifirst].customer_list[jfirst]
                    possibleChangeBefore = truck_list[ifirst].customer_list[jfirst - 1]
                    possibleChangeAfter = truck_list[ifirst].customer_list[jfirst + 1]

                    possiblePlaceBefore = truck_list[isecond].customer_list[jsecond]
                    possiblePlaceAfter = truck_list[isecond].customer_list[jsecond + 1]

                    if ifirst != isecond:
                        if truck_list[isecond].q + customer_list_id[possibleChange][2] > 150:
                            continue

                    changeTimeSecond = all_distances_calc[possiblePlaceBefore][possibleChange] \
                                       + all_distances_calc[possibleChange][possiblePlaceAfter] \
                                       - all_distances_calc[possiblePlaceBefore][possiblePlaceAfter]

                    changeTimeFirst = all_distances_calc[possibleChangeBefore][possibleChangeAfter] \
                                      - all_distances_calc[possibleChangeBefore][possibleChange] \
                                      - all_distances_calc[possibleChange][possibleChangeAfter]

                    if ifirst != isecond:
                        if truck_list[isecond].t + customer_list_id[possibleChange][3] + changeTimeSecond > 200:
                            continue
                    else:
                        if truck_list[ifirst].t + changeTimeSecond + changeTimeFirst > 200:
                            continue

                    costAdd = all_distances_calc[possibleChangeBefore][possibleChangeAfter] \
                              + all_distances_calc[possiblePlaceBefore][possibleChange] \
                              + all_distances_calc[possibleChange][possiblePlaceAfter]

                    costRemoved = all_distances_calc[possibleChange][possibleChangeBefore] \
                                  + all_distances_calc[possibleChange][possibleChangeAfter] \
                                  + all_distances_calc[possiblePlaceBefore][possiblePlaceAfter]

                    moveCost = costAdd - costRemoved

                    if moveCost < maxGainCost - 0.0001:
                        flag = True
                        maxGainCost = moveCost
                        gainlist = [ifirst, isecond, jfirst, jsecond, changeTimeSecond, changeTimeFirst, possibleChange]


    if flag:
        relocate(gainlist[0], gainlist[1], gainlist[2], gainlist[3], truck_list)
        truck_list[gainlist[0]].t = truck_list[gainlist[0]].t + gainlist[5] - customer_list_id[gainlist[6]][3]
        truck_list[gainlist[1]].t = truck_list[gainlist[1]].t + gainlist[4] + customer_list_id[gainlist[6]][3]
        truck_list[gainlist[0]].q = truck_list[gainlist[0]].q - customer_list_id[gainlist[6]][2]
        truck_list[gainlist[1]].q = truck_list[gainlist[1]].q + customer_list_id[gainlist[6]][2]
        # print("relocate", gainlist[6], gainlist[5], gainlist[4])

    return flag


def swap(ifirst, isecond, jfirst, jsecond, trucklist):
    b1 = trucklist[ifirst].customer_list[jfirst]
    b2 = trucklist[isecond].customer_list[jsecond]
    trucklist[ifirst].customer_list[jfirst] = b2
    trucklist[isecond].customer_list[jsecond] = b1

def findBestSwapMove(truck_list, all_distances_calc, customer_list_id):
    flag = False

    maxgain = 0
    gainlist = []

    for ifirst in range(6):
        for isecond in range(ifirst, 6):
            for jfirst in range(1, len(truck_list[ifirst].customer_list) - 1):
                second = 1
                if ifirst == isecond:
                    second = jfirst + 1
                for jsecond in range(second, len(truck_list[isecond].customer_list) - 1):

                    a1 = truck_list[ifirst].customer_list[jfirst - 1]
                    b1 = truck_list[ifirst].customer_list[jfirst]
                    c1 = truck_list[ifirst].customer_list[jfirst + 1]

                    a2 = truck_list[isecond].customer_list[jsecond - 1]
                    b2 = truck_list[isecond].customer_list[jsecond]
                    c2 = truck_list[isecond].customer_list[jsecond + 1]

                    moveCost = None
                    costChangeFirstRoute = None
                    costChangeSecondRoute = None

                    if ifirst == isecond:
                        if jfirst == jsecond - 1:
                            costRemoved = all_distances_calc[a1][b1] + all_distances_calc[b1][b2] + \
                                          all_distances_calc[b2][c2]
                            costAdded = all_distances_calc[a1][b2] + all_distances_calc[b2][b1] + \
                                        all_distances_calc[b1][c2]
                            moveCost = costAdded - costRemoved

                        else:

                            costRemoved1 = all_distances_calc[a1][b1] + all_distances_calc[b1][c1]
                            costAdded1 = all_distances_calc[a1][b2] + all_distances_calc[b2][c1]
                            costRemoved2 = all_distances_calc[a2][b2] + all_distances_calc[b2][c2]
                            costAdded2 = all_distances_calc[a2][b1] + all_distances_calc[b1][c2]
                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                    else:
                        if truck_list[ifirst].q - customer_list_id[b1][2] + customer_list_id[b2][2] > 150:
                            continue
                        if truck_list[isecond].q - customer_list_id[b2][2] + customer_list_id[b1][2] > 150:
                            continue

                        costRemoved1 = all_distances_calc[a1][b1] + all_distances_calc[b1][c1]
                        costAdded1 = all_distances_calc[a1][b2] + all_distances_calc[b2][c1]
                        costRemoved2 = all_distances_calc[a2][b2] + all_distances_calc[b2][c2]
                        costAdded2 = all_distances_calc[a2][b1] + all_distances_calc[b1][c2]

                        costChangeFirstRoute = costAdded1 - costRemoved1
                        costChangeSecondRoute = costAdded2 - costRemoved2

                        if truck_list[ifirst].t + costChangeFirstRoute - customer_list_id[b1][3] + customer_list_id[b2][3] > 200 - 0.0001:
                            continue
                        if truck_list[isecond].t + costChangeSecondRoute - customer_list_id[b2][3] + customer_list_id[b1][3]> 200 - 0.0001:
                            continue

                        moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                    if moveCost < maxgain - 0.0001:
                        maxgain = moveCost
                        gainlist = [ifirst, isecond, jfirst, jsecond, moveCost, costChangeFirstRoute, costChangeSecondRoute]
                        flag = True

    if flag:
        # print("swapped")
        id1 = truck_list[gainlist[0]].customer_list[gainlist[2]]
        id2 = truck_list[gainlist[1]].customer_list[gainlist[3]]
        # print(id1, id2)
        swap(gainlist[0], gainlist[1], gainlist[2], gainlist[3], truck_list)
        if gainlist[0] == gainlist[1]:
            truck_list[gainlist[0]].t += maxgain
        else:
            truck_list[gainlist[0]].q = truck_list[gainlist[0]].q - customer_list_id[id1][2] + customer_list_id[id2][
                2]
            truck_list[gainlist[1]].q = truck_list[gainlist[1]].q - customer_list_id[id2][2] + customer_list_id[id1][
                2]
            truck_list[gainlist[0]].t = truck_list[gainlist[0]].t + gainlist[5] \
                                        - customer_list_id[id1][3] + customer_list_id[id2][3]
            truck_list[gainlist[1]].t = truck_list[gainlist[1]].t + gainlist[6] \
                                        - customer_list_id[id2][3] + customer_list_id[id1][3]

    return flag


def twoOptMove(ifirst, isecond, jfirst, jsecond, k, trucklist):
    if k == 1:
        # print("____")
        reversedSegment = reversed(trucklist[ifirst].customer_list[jfirst + 1: jsecond + 1])
        trucklist[ifirst].customer_list[jfirst + 1: jsecond + 1] = reversedSegment

    elif k == 2:
        # print("x")
        relocateSegmentTruck1 = trucklist[ifirst].customer_list[jfirst + 1:]
        relocateSegmentTruck2 = trucklist[isecond].customer_list[jsecond + 1:]

        del trucklist[ifirst].customer_list[jfirst + 1:]
        del trucklist[isecond].customer_list[jsecond + 1:]

        trucklist[ifirst].customer_list.extend(relocateSegmentTruck2)
        trucklist[isecond].customer_list.extend(relocateSegmentTruck1)

    else:

        # print("c")
        relocateFirstSegmentTruck2 = trucklist[isecond].customer_list[: jsecond + 1]
        relocateSecondSegmentTruck2 = trucklist[isecond].customer_list[jsecond + 1:]

        relocateFirstSegmentTruck1 = trucklist[ifirst].customer_list[: jfirst + 1]
        relocateSecondSegmentTruck1 = trucklist[ifirst].customer_list[jfirst + 1:]


        relocateFirstSegmentTruck2.reverse()
        relocateSecondSegmentTruck1.reverse()

        relocateFirstSegmentTruck1.extend(relocateFirstSegmentTruck2)
        relocateSecondSegmentTruck1.extend(relocateSecondSegmentTruck2)

        del trucklist[ifirst].customer_list[:]
        del trucklist[isecond].customer_list[:]

        trucklist[ifirst].customer_list.extend(relocateFirstSegmentTruck1)
        trucklist[isecond].customer_list.extend(relocateSecondSegmentTruck1)


def CapacityAndDurationIsViolated(param, jfirst, param1, jsecond):
    A = param.customer_list[jfirst]
    B = param.customer_list[jfirst + 1]
    K = param1.customer_list[jsecond]
    L = param1.customer_list[jsecond + 1]

    truck1FirstHalf = 0
    for i in range(0, jfirst + 1):
        id = param.customer_list[i]
        next_id = param.customer_list[i + 1]
        truck1FirstHalf += customer_list_id[id][3]
        truck1FirstHalf += all_distances_calc[id][next_id]
    AB = all_distances_calc[A][B]
    AL = all_distances_calc[A][L]
    truck1SecondHalf = param.t - truck1FirstHalf
    truck1FirstHalf -= AB

    demand_truck1FirstHalf = 0
    for i in range(0, jfirst + 1):
        id = param.customer_list[i]
        demand_truck1FirstHalf += customer_list_id[id][2]
    demand_truck1SecondHalf = param.q - demand_truck1FirstHalf

    truck2FirstHalf = 0
    for i in range(0, jsecond + 1):
        id = param1.customer_list[i]
        next_id = param1.customer_list[i + 1]
        truck2FirstHalf += customer_list_id[id][3]
        truck2FirstHalf += all_distances_calc[id][next_id]
    KL = all_distances_calc[K][L]
    KB = all_distances_calc[K][B]
    truck2SecondHalf = param1.t - truck2FirstHalf
    truck2FirstHalf -= KL

    demand_truck2FirstHalf = 0
    for i in range(0, jsecond + 1):
        id = param1.customer_list[i]
        demand_truck2FirstHalf += customer_list_id[id][2]
    demand_truck2SecondHalf = param1.q - demand_truck2FirstHalf

    return [truck1FirstHalf, truck1SecondHalf, truck2FirstHalf, truck2SecondHalf, demand_truck1FirstHalf,
            demand_truck1SecondHalf, demand_truck2FirstHalf, demand_truck2SecondHalf]


def findBesttwoOptMove(truck_list, all_distances_calc, customer_list_id):
    maxgain = 0
    gainlist = []
    flag = False
    for ifirst in range(6):
        for isecond in range(ifirst, 6):
            for jfirst in range(0, len(truck_list[ifirst].customer_list) - 1):
                start2 = 0
                if ifirst == isecond:
                    start2 = jfirst + 2

                for jsecond in range(start2, len(truck_list[isecond].customer_list) - 1):
                    moveCost = 10 ** 9

                    A = truck_list[ifirst].customer_list[jfirst]
                    B = truck_list[ifirst].customer_list[jfirst + 1]
                    K = truck_list[isecond].customer_list[jsecond]
                    L = truck_list[isecond].customer_list[jsecond + 1]

                    if ifirst == isecond:
                        if jfirst == 0 and jsecond == len(truck_list[ifirst].customer_list) - 2:
                            continue
                        costAdded = all_distances_calc[A][K] + all_distances_calc[B][L]
                        costRemoved = all_distances_calc[A][B] + all_distances_calc[K][L]
                        moveCost = costAdded - costRemoved

                        k = 1
                    else:
                        if jfirst == 0 and jsecond == 0:
                            continue
                        if jfirst == len(truck_list[ifirst].customer_list) - 2 and jsecond == len(truck_list[isecond].customer_list) - 2:
                            continue

                        cd = CapacityAndDurationIsViolated(truck_list[ifirst], jfirst, truck_list[isecond], jsecond)

                        Xstop = False
                        XtruckTime1 = cd[0] + cd[3] + all_distances_calc[A][L]
                        XtruckTime2 = cd[1] + cd[2] + all_distances_calc[B][K]
                        XtruckDemand1 = cd[4] + cd[7]
                        XtruckDemand2 = cd[5] + cd[6]

                        if XtruckTime1 > 200:
                            Xstop = True
                        if XtruckTime2 > 200:
                            Xstop = True
                        if XtruckDemand1 > 150:
                            Xstop = True
                        if XtruckDemand2 > 150:
                            Xstop = True

                        XcostAdded = all_distances_calc[A][L] + all_distances_calc[B][K]
                        XcostRemoved = all_distances_calc[A][B] + all_distances_calc[K][L]
                        XmoveCost = XcostAdded - XcostRemoved

                        Cstop = False
                        CtruckTime1 = cd[0] + cd[2] + all_distances_calc[A][K]
                        CtruckTime2 = cd[1] + cd[3] + all_distances_calc[B][L]
                        CtruckDemand1 = cd[4] + cd[6]
                        CtruckDemand2 = cd[5] + cd[7]

                        if CtruckTime1 > 200:
                            Cstop = True
                        if CtruckTime2 > 200:
                            Cstop = True
                        if CtruckDemand1 > 150:
                            Cstop = True
                        if CtruckDemand2 > 150:
                            Cstop = True

                        CcostAdded = all_distances_calc[A][K] + all_distances_calc[B][L]
                        CcostRemoved = all_distances_calc[A][B] + all_distances_calc[K][L]
                        CmoveCost = CcostAdded - CcostRemoved

                        if Xstop == True and Cstop == True:
                            continue
                        elif Xstop == True and Cstop == False:
                            truckTime1 = CtruckTime1
                            truckTime2 = CtruckTime2
                            truckDemand1 = CtruckDemand1
                            truckDemand2 = CtruckDemand2
                            moveCost = CmoveCost
                            k = 3
                        elif Xstop == False and Cstop == True:
                            truckTime1 = XtruckTime1
                            truckTime2 = XtruckTime2
                            truckDemand1 = XtruckDemand1
                            truckDemand2 = XtruckDemand2
                            moveCost = XmoveCost
                            k = 2
                        else:
                            if XmoveCost > CmoveCost:
                                truckTime1 = CtruckTime1
                                truckTime2 = CtruckTime2
                                truckDemand1 = CtruckDemand1
                                truckDemand2 = CtruckDemand2
                                moveCost = CmoveCost
                                k = 3
                            else:
                                truckTime1 = XtruckTime1
                                truckTime2 = XtruckTime2
                                truckDemand1 = XtruckDemand1
                                truckDemand2 = XtruckDemand2
                                moveCost = XmoveCost
                                k = 2

                    if moveCost < maxgain - 0.0001:
                        maxgain = moveCost
                        if k == 1:
                            gainlist = [ifirst, isecond, jfirst, jsecond, moveCost, None, None, None, k]
                        else:
                            gainlist = [ifirst, isecond, jfirst, jsecond, truckTime1,
                                        truckTime2, truckDemand1, truckDemand2, k]
                        flag = True

    if flag:

        twoOptMove(gainlist[0], gainlist[1], gainlist[2], gainlist[3], gainlist[8], truck_list)

        if gainlist[8] == 1:
            truck_list[gainlist[0]].t += gainlist[4]
        else:
            truck_list[gainlist[0]].t = gainlist[4]
            truck_list[gainlist[1]].t = gainlist[5]
            truck_list[gainlist[0]].q = gainlist[6]
            truck_list[gainlist[1]].q = gainlist[7]

    return flag


class Truck:
    def __init__(self, number, q, t, customer_list, profit):
        self.number = number
        self.q = q
        self.t = t
        self.customer_list = customer_list
        self.profit = profit

    def __len__(self):
        return len(self.customer_list)


class Customer:
    def __init__(self, id, x, y, demand, service_time, profit):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.service_time = service_time
        self.profit = profit


customer_list = []
customer_list_id = [[23.142, 11.736, 0, 0, 0]]

with open('Instance.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            k = int(row[1])
        elif line_count == 1:
            q = int(row[1])
        elif line_count == 2:
            t = int(row[1])
        elif line_count == 5:
            depot = [float(row[1]), float(row[2])]
        elif line_count == 7:
            customers = row[1]
        elif line_count >= 11:
            customer_list.append([int(row[0]), float(row[1]), float(row[2]), int(row[3]), int(row[4]), int(row[5])])
            customer_list_id.append([float(row[1]), float(row[2]), int(row[3]), int(row[4]), int(row[5])])
        line_count += 1

all_distances = [[0, 23.142, 11.736]]
for i in range(len(customer_list)):
    all_distances.append([customer_list[i][0], customer_list[i][1], customer_list[i][2]])

all_distances_calc = []
all_nearest_neighbors = []
for i in range(len(all_distances)):
    ilist = []
    nearest_neighbors = []
    max = 0
    max_id = 0
    for j in range(len(all_distances)):
        d = distance_calc(all_distances[i][1], all_distances[i][2], all_distances[j][1], all_distances[j][2])
        ilist.append(d)
        if d < 10 and i < j and i != 0 and j != 0:
            new_profit = customer_list_id[i][4] + customer_list_id[j][4]
            if new_profit >= 10:
                new_id = i * 1000 + j
                new_service_time = d + customer_list_id[i][3] + customer_list_id[j][3]
                new_demand = customer_list_id[i][2] + customer_list_id[j][2]
        if len(nearest_neighbors) < 337 and d != 0 and i != j:
            max_id = j
            max = d
            nearest_neighbors.append([max_id, max])
            nearest_neighbors.sort(key=lambda x: (x[1]), reverse=False)
        else:
            if max > d and d != 0 and i != j:
                max_id = j
                max = d
                nearest_neighbors.pop()
                nearest_neighbors.append([max_id, max])
                nearest_neighbors.sort(key=lambda x: (x[1]), reverse=False)
    all_nearest_neighbors.append(nearest_neighbors)
    all_distances_calc.append(ilist)


truck_list = []

zeroneighbours = []
for i in range(len(all_nearest_neighbors[0])):
    zeroneighbours.append(all_nearest_neighbors[0][i])
    zeroneighbours[i].append((i + 1) * 1)

customers_sorted_by_profit = customer_list.copy()
customers_sorted_by_profit.sort(key=lambda x: ((x[5] * x[5]) / (x[3] * x[4])), reverse=True)
customer_profit_secondChance = customers_sorted_by_profit.copy()

for i in range(len(customers_sorted_by_profit)):
    customers_sorted_by_profit[i].append((i + 1) * 1)

zeroneighbours.sort(key=lambda x: (x[0]), reverse=False)
customers_sorted_by_profit.sort(key=lambda x: (x[0]), reverse=False)

for i in range(len(zeroneighbours)):
    zeroneighbours[i][2] += customers_sorted_by_profit[i][6]

zeroneighbours.sort(key=lambda x: (x[2]), reverse=False)

for i in range(6):
    truck_list.append(Truck(i + 1, 0, 0, [0], 0))



best_truck_list = []
best_profit = 0
best_i = -1

for i in range(2500):
    f = False
    customersintrucks = []

    for truck in range(6):
        f = False
        id = zeroneighbours[random.randint(0, 54)][0]
        if customer_list_id[id][4] < pro:
            f = True
        while id in customersintrucks or f:
            id = zeroneighbours[random.randint(0, 54)][0]
            if customer_list_id[id][4] < pro:
                f = True
            else:
                f = False

        demand = customer_list_id[id][2]
        service_time = customer_list_id[id][3]
        profit = customer_list_id[id][4]

        if len(truck_list[truck].customer_list) == 1:

            go_and_service_time = all_distances_calc[0][id] + service_time
            quantity = truck_list[truck].q
            available_time = truck_list[truck].t

            if (go_and_service_time + all_distances_calc[0][
                id] + available_time) <= 200 and demand + quantity <= 150:
                truck_list[truck].customer_list.append(id)
                customersintrucks.append(id)
                truck_list[truck].t = truck_list[truck].t + go_and_service_time
                truck_list[truck].q = truck_list[truck].q + demand
                truck_list[truck].profit = profit

            for j in range(len(all_nearest_neighbors[id])):


                next_id = all_nearest_neighbors[id][j][0]
                if customer_list_id[next_id][4] < pro:
                    continue

                demand = customer_list_id[next_id][2]
                service_time = customer_list_id[next_id][3]
                profit = customer_list_id[next_id][4]

                if next_id not in customersintrucks and next_id != 0:

                    trucklistlength = len(truck_list[truck].customer_list)
                    location = truck_list[truck].customer_list[trucklistlength - 1]
                    quantity = truck_list[truck].q
                    available_time = truck_list[truck].t
                    go_and_service_time = all_distances_calc[location][next_id] + service_time

                    if (go_and_service_time + all_distances_calc[0][
                        next_id] + available_time) <= 200 and demand + quantity <= 150:
                        truck_list[truck].q = truck_list[truck].q + demand
                        truck_list[truck].t = truck_list[truck].t + go_and_service_time
                        truck_list[truck].customer_list.append(next_id)
                        customersintrucks.append(next_id)
                        truck_list[truck].profit = truck_list[truck].profit + profit
                        id = next_id

    all_profit = 0


    for l in range(6):
        trucklistlength = len(truck_list[l].customer_list)
        location = truck_list[l].customer_list[trucklistlength - 1]
        truck_list[l].t = truck_list[l].t + all_distances_calc[location][0]
        all_profit = all_profit + truck_list[l].profit
        truck_list[l].customer_list.append(0)


    flag2 = findBestRelocationMove(truck_list,all_distances_calc,customer_list_id)
    while flag2:
        flag2 = findBestRelocationMove(truck_list, all_distances_calc, customer_list_id)

    flag = findBestSwapMove(truck_list, all_distances_calc, customer_list_id)
    while flag:
        flag = findBestSwapMove(truck_list, all_distances_calc, customer_list_id)

    flag3 = findBesttwoOptMove(truck_list, all_distances_calc, customer_list_id)
    while flag3:
        flag3 = findBesttwoOptMove(truck_list, all_distances_calc, customer_list_id)



    stop = False

    while not stop:

        for truck in truck_list:
            trucklistlength = len(truck.customer_list)

            for customer in range(len(customer_profit_secondChance)):

                id_secondChance = customer_profit_secondChance[customer][0]
                demand = customer_list_id[id_secondChance][2]
                service_time = customer_list_id[id_secondChance][3]
                profit = customer_list_id[id_secondChance][4]
                if id_secondChance not in customersintrucks and demand + truck.q <= 150 and profit >= pro - 5:

                    for j in range(0, trucklistlength - 1):
                        id_pre = truck.customer_list[j]
                        id_after = truck.customer_list[j + 1]
                        new_time = truck.t + all_distances_calc[id_pre][id_secondChance] + service_time \
                                   + all_distances_calc[id_after][id_secondChance] - all_distances_calc[id_pre][id_after]
                        if new_time <= 200 and new_time - truck.t < 50:

                            truck.q = truck.q + demand
                            truck.t = new_time
                            truck.customer_list.insert(j + 1, id_secondChance)
                            customersintrucks.append(id_secondChance)
                            truck.profit = truck.profit + profit

                            break

        profit = 0
        for truck in truck_list:
            profit += truck.profit

        if profit <= 750:
            break

        counter = 0

        flag2 = findBestRelocationMove(truck_list, all_distances_calc, customer_list_id)
        while flag2:
            flag2 = findBestRelocationMove(truck_list, all_distances_calc, customer_list_id)
            if flag2:
                counter += 1

        flag = findBestSwapMove(truck_list, all_distances_calc, customer_list_id)
        while flag:
            flag = findBestSwapMove(truck_list, all_distances_calc, customer_list_id)
            if flag:
                counter += 1

        flag3 = findBesttwoOptMove(truck_list, all_distances_calc, customer_list_id)
        while flag3:
            flag3 = findBesttwoOptMove(truck_list, all_distances_calc, customer_list_id)
            if flag3:
                counter += 1


        if counter == 0:

            stop = True
            for truck in truck_list:
                trucklistlength = len(truck.customer_list)

                for customer in range(len(customer_profit_secondChance)):

                    id_secondChance = customer_profit_secondChance[customer][0]
                    demand = customer_list_id[id_secondChance][2]
                    service_time = customer_list_id[id_secondChance][3]
                    profit = customer_list_id[id_secondChance][4]
                    if id_secondChance not in customersintrucks and demand + truck.q <= 150 and profit >= pro - 5:

                        for j in range(0, trucklistlength - 1):
                            id_pre = truck.customer_list[j]
                            id_after = truck.customer_list[j + 1]
                            new_time = truck.t + all_distances_calc[id_pre][id_secondChance] + service_time \
                                       + all_distances_calc[id_after][id_secondChance] - all_distances_calc[id_pre][
                                           id_after]
                            if new_time <= 200 and new_time - truck.t < 50:
                                truck.q = truck.q + demand
                                truck.t = new_time
                                truck.customer_list.insert(j + 1, id_secondChance)
                                customersintrucks.append(id_secondChance)
                                truck.profit = truck.profit + profit

                                break

    all_profit = 0
    for truck in truck_list:
        all_profit += truck.profit
    # print(i, all_profit)

    if i % 100 == 0:
        print(i)

    if best_profit < all_profit:
        best_i = i
        best_profit = all_profit
        best_truck_list = truck_list.copy()
        bestcustomersintrucks = customersintrucks.copy()

    truck_list.clear()
    customersintrucks.clear()

    for k in range(6):
        truck_list.append(Truck(k + 1, 0, 0, [0], 0))



print(best_i, best_profit)
for i in range(6):
    routTime = 0
    routDemand = 0
    for j in range(1, len(best_truck_list[i].customer_list)):
        id_pre = best_truck_list[i].customer_list[j - 1]
        id = best_truck_list[i].customer_list[j]
        routTime += all_distances_calc[id_pre][id]
        routTime += customer_list_id[id][3]
        routDemand += customer_list_id[id][2]
    print(routTime, "--", routDemand)


print("--- %s seconds ---" % (time.time() - start_time))


#
# plt.axis([-100, 100, -100, 100])
# plot_colors = ['r', 'b', 'g', 'm', 'darkorange', 'y']
#
# for i in range(len(customer_list_id)):
#     plt.plot(customer_list_id[i][0], customer_list_id[i][1], 'co')
#
# for i in range(6):
#     plot_x = []
#     plot_y = []
#     for j in range(len(best_truck_list[i].customer_list)):
#         plot_x.append(customer_list_id[best_truck_list[i].customer_list[j]][0])
#         plot_y.append(customer_list_id[best_truck_list[i].customer_list[j]][1])
#     plt.plot(plot_x, plot_y, plot_colors[i])
#     plt.plot(plot_x, plot_y, 'ko')
#
# plt.show()

solution_to_csv("sol_example.txt", best_profit, best_truck_list)

all_nodes_c, vehicles_c, capacity_c, time_limit_c = solution_checker.load_model('Instance.txt')
solution_checker.test_solution('sol_example.txt', all_nodes_c, vehicles_c, capacity_c, time_limit_c)
print()
