import math
from datetime import datetime, timedelta
# pickup lat pickup long dropoff lat drop off long
import map

#TODO fix potential bug with this (run fitnesses of pop1 and pop13, 3,15)
def get_fitness(chromosome, fit):
    tot_distances = 0
    tot_time = 0
    for g in range(len(chromosome) - 1):
        loc1 = str(chromosome[g][4]) + "," + str(chromosome[g][5])
        loc2 = str(chromosome[g + 1][2]) + "," + str(chromosome[g + 1][3])

        driving_time = map.cached_timedistance(loc1, loc2)[0]
        distance_between = map.cached_timedistance(loc1, loc2)[1]
        trip1_start_time = datetime(year=1, month=1, day=1, hour=(int(chromosome[g][1].split(":")[0])),
                                    minute=(int(chromosome[g][1].split(":")[1])))
        trip2_start_time = datetime(year=1, month=1, day=1, hour=(int(chromosome[g + 1][1].split(":")[0])),
                                    minute=(int(chromosome[g + 1][1].split(":")[1])))
        time_between = trip2_start_time - trip1_start_time
        # what cross takes into account
        extra_time = time_between - timedelta(minutes=driving_time)
        if fit:
            print()
            print("gene 1:", chromosome[g])
            print("gene 2:", chromosome[g + 1])
            print("time between", time_between)
            print("km between", distance_between)
            print("driving mins", driving_time)
            print("extra time", extra_time)
            print()
        try:
            extra_time = int(str(extra_time).split(":")[0]) * 60 + int(str(extra_time).split(":")[1])
        except ValueError:
            print("SHOULDNT BE ABLE TO HAPPEN")
            print(trip1_start_time)
            print(trip2_start_time)
            print()

        tot_time += extra_time
        tot_distances += distance_between
    return [chromosome, tot_distances, tot_time]


def find_mates(gene, parents, mates):
    # this will be run with a one dimensional array & never null time
    # remember, you're looping through half the population (105)
    possible_mates = []
    previous_start_time = datetime(year=1, month=1, day=1, hour=(int(gene[1].split(":")[0])),
                                   minute=(int(gene[1].split(":")[1])))
    duration = int(gene[7])

    if mates:
        print("mate 1:", gene)
        print("mate 1 start time:", previous_start_time.strftime("%H:%M:%S"))
        print()

    for g in range(len(parents)):
        loc1 = str(gene[4]) + "," + str(gene[5])
        loc2 = str(parents[g][2]) + "," + str(parents[g][3])
        trip_time = int(gene[7]) / 60

        tot_time = trip_time
        time_distance = map.cached_timedistance(loc1, loc2)
        driving_time_between = time_distance[0]
        tot_time += driving_time_between
        window = tot_time
        tot_time = previous_start_time + timedelta(seconds=duration + tot_time*60)
        next_start_time = datetime(year=1, month=1, day=1, hour=(int(parents[g][1].split(":")[0])),
                                   minute=(int(parents[g][1].split(":")[1])))

        if mates:
            print("possible mate 2:", parents[g])
            print("start_time", next_start_time.strftime("%H:%M:%S"))
            print("driving time:", window, "minutes")

        if next_start_time >= tot_time:
            possible_mates.append(parents[g])

            if mates:
                print(next_start_time.strftime("%H:%M:%S"), ">", tot_time.strftime("%H:%M:%S"))
                print("can complete trip in time")
                print()
        else:
            if mates:
                print(next_start_time.strftime("%H:%M:%S"), "<", tot_time.strftime("%H:%M:%S"))
                print("cannot complete trip in time")
                print()

    for i in range(len(possible_mates)):
        for j in range(0, len(possible_mates) - i - 1):
            # Swap if current element is greater than next
            current_time = int(possible_mates[j][1].split(":")[0] + possible_mates[j][1].split(":")[1])
            next_time = int(possible_mates[j + 1][1].split(":")[0] + possible_mates[j + 1][1].split(":")[1])
            if current_time > next_time:
                possible_mates[j], possible_mates[j + 1] = possible_mates[j + 1], possible_mates[j]

    return possible_mates


def assign_trips(parents, assign):
    # offspring = ["ID", "RequestedPickUpTime","PickUpLat","PickUpLng","DropOffLat","DropOffLng",	"EstimatedDistance","EstimatedDuration (s)","SeatingNeedCode"]
    offspring = []
    remove_genes = []
    drivers = 25  # 25 = num of drivers

    for c in range(drivers):
        chromosome = []

        parents = get_updated_parents(remove_genes, parents)
        for i in range(len(parents)):
            for j in range(0, len(parents) - i - 1):
                # Swap if current element is greater than next
                current_time = int(parents[j][1].split(":")[0] + parents[j][1].split(":")[1])
                next_time = int(parents[j + 1][1].split(":")[0] + parents[j + 1][1].split(":")[1])
                if current_time > next_time:
                    parents[j], parents[j + 1] = parents[j + 1], parents[j]

        gene1 = parents[0]
        chromosome.append(gene1)
        remove_genes.append(gene1)
        offspring.append(chromosome)

    if assign:
        print("FIRST PASS")
        for i in range(len(offspring)):
            print(offspring[i])

    for c2 in range(drivers):
        # if cross:
        # print("possible mates: ", len(find_mates(offspring[c2][0], get_updated_parents(remove_genes, parents), mates=False)))
        if len(find_mates(offspring[c2][0], get_updated_parents(remove_genes, parents), mates=False)) > 0:
            gene2 = find_mates(offspring[c2][0], get_updated_parents(remove_genes, parents), mates=False)[0]
            remove_genes.append(gene2)
            offspring[c2].append(gene2)

    if assign:
        print()
        print("SECOND PASS")
        for j in range(len(offspring)):
            print(offspring[j])

    for c3 in range(drivers):
        # if cross:
        # print("possible mates: ", len(find_mates(offspring[c3][0], get_updated_parents(remove_genes, parents), mates=False)))
        if len(offspring[c3]) == 2:
            if len(find_mates(offspring[c3][1], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene3 = find_mates(offspring[c3][1], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene3)
                offspring[c3].append(gene3)
        else:
            if len(find_mates(offspring[c3][0], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene3 = find_mates(offspring[c3][0], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene3)
                offspring[c3].append(gene3)

    if assign:
        print()
        print("THIRD PASS")
        for j in range(len(offspring)):
            print(offspring[j])
        print("genes left:", len(get_updated_parents(remove_genes, parents)))

    for c4 in range(drivers):

        if len(offspring[c4]) == 3:
            if len(find_mates(offspring[c4][2], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene4 = find_mates(offspring[c4][2], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene4)
                offspring[c4].append(gene4)

        elif len(offspring[c4]) == 2:
            if len(find_mates(offspring[c4][1], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene4 = find_mates(offspring[c4][1], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene4)
                offspring[c4].append(gene4)

        else:
            if len(find_mates(offspring[c4][0], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene4 = find_mates(offspring[c4][0], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene4)
                offspring[c4].append(gene4)

    if assign:
        print()
        print("FOURTH PASS")
        for j in range(len(offspring)):
            print(offspring[j])

        print("genes left:", len(get_updated_parents(remove_genes, parents)))
    return offspring


# TODO delete get_updated_parents
def get_updated_parents(remove_genes, parents):
    temp_parents = []
    for c in range(len(parents)):
        temp_parents.append(parents[c])
    updated = [elem for elem in temp_parents if elem not in remove_genes]
    return updated


def get_fit_half(offspring):
    # arr returned from [[get_fit [trip1, trip2, trip3, trip4?, distance, time]]
    arr = []
    for i in range(len(offspring)):
        arr.append(get_fitness(offspring[i], fit=False))

    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            if (arr[j][1] + float(arr[j][2])) > (arr[j + 1][1] + float(arr[j + 1][2])):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    fit_half = []
    for i in range(round(len(arr) / 2)):
        fit_half.append(arr[i][0])
    return fit_half
    # returns  [[trip1, trip2, trip3, trip4?, distance, time]]


# [ [ [trip1][trip2][trip3][trip4?] ] ]
#TODO fix having only 24 drivers
def crossover(parents):
    population = []
    for i in range(len(parents)):
        new_run = []
        half = round(len(parents[i])/2)
        # run = chromosome
        for a in range(0, half):
            new_run.append(parents[i][a])
        population.append(new_run)

    gene_population = []
    for i in range(len(parents)):
        for g in range(len(parents[i])):
            gene_population.append(parents[i][g])

    for i in range(len(population)):
        if len(parents[i]) == 3:
            next_trip1 = find_mates(population[i][len(population[i])-1], gene_population, mates=False)[0]
            population[i].append(next_trip1)
            gene_population.remove(next_trip1)
        else:
            next_trip1 = find_mates(population[i][len(population[i]) - 1], gene_population, mates=False)[0]
            population[i].append(next_trip1)
            gene_population.remove(next_trip1)
            next_trip2 = find_mates(population[i][len(population[i]) - 1], gene_population, mates=False)[0]
            population[i].append(next_trip2)
            gene_population.remove(next_trip2)

    return population

def algo(parents, algo):
    mates = False
    assign = False
    fit = False
    population = assign_trips(parents, assign)

    parent_half = get_fit_half(population)
    if algo:
        print("PARENTS")
        print(parent_half)
        print()
    parent_fitness = []
    for i in range(len(parent_half)):
        fit_arr = get_fitness(parent_half[i], fit)
        chrom_fitness = fit_arr[1] + float(fit_arr[2])
        parent_fitness.append(chrom_fitness)
    parent_fitness.sort()
    if algo:
        print("PARENT FITNESS")
        print(parent_fitness)
        print()

    offspring_half = crossover(parent_half)
    if algo:
        print("OFFSPRING")
        print(offspring_half)
        print()
    child_fitness = []
    for i in range(len(offspring_half)):
        fit_arr = get_fitness(offspring_half[i], fit)
        chrom_fitness = fit_arr[1] + float(fit_arr[2])
        child_fitness.append(chrom_fitness)
    child_fitness.sort()
    if algo:
        print("OFFSPRING FITNESS")
        print(child_fitness)
        print()

    del population[:]
    for i in range(len(parent_half)):
        population.append(parent_half[i])
    for i in range(len(offspring_half)):
        population.append(offspring_half[i])
    if algo:
        print("NEW POPULATION")
        print(population)
    return population

