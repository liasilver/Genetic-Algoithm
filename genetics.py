from datetime import datetime, timedelta
import haversine as hs

# def calc_fitness(pop):
#    for i in range(len(pop)):
#
#
# #return dictionary with chromosomes and fitnesses
#
#
# def select_mates(pop):
#     mates_dict ={}
#     mates = [[]]
#     for i in range(len(pop)):
#         mates_dict[pop[i]] = calc_fitness(pop[i])
#     mates_sorted = sorted(mates_dict.items(), key=lambda x: x[1], reverse=True)
#     for j in range(len(mates_sorted)/2): # sort out numbers for everything
#         mates.append()


def crossover(parents, cross):
    offspring = [[[]]]

    for c in range(1, len(parents)):
        # create chromosome with 1 gene from parent1 and 2 genes from parent2
        offspring_chromosome = [[]]
        for g in range(len(parents)):
            if cross:
                print("mate 1:", parents[c][g])
            if parents[c][g][1]:
                possible_mates = [[]]
                previous_start_time = datetime(year=1, month=1, day=1, hour=(int(parents[c][g][1].split(":")[0])),minute=(int(parents[c][g][1].split(":")[1])))
                if cross:
                    print("mate 1 start time:", previous_start_time.strftime("%H:%M:%S"))
                duration = int(parents[c][g][7])
                if cross:
                    print("duration:", duration)
                window = 1200 # 20 minutes in seconds

                total_time = previous_start_time + timedelta(seconds=duration + window)
                if cross:
                    print("total time (duration + start):", total_time.strftime("%H:%M:%S"))
                print()
                for c2 in range(1, len(parents)):
                    for g2 in range(3):
                        if parents[c2][g2][1] and parents[c2][g2] != parents[c2][g]:
                            if cross:
                                print("possible mate 2:", parents[c2][g2])

                            next_start_time = datetime(year=1, month=1, day=1, hour=(int(parents[c2][g2][1].split(":")[0])), minute=(int(parents[c2][g2][1].split(":")[1])))
                            if cross:
                                print("start_time", next_start_time.strftime("%H:%M:%S"))

                            if next_start_time > total_time:
                                if cross:
                                    print(next_start_time.strftime("%H:%M:%S"), ">", total_time.strftime("%H:%M:%S"))
                                possible_mates.append(parents[c2][g2])
                                if cross:
                                    print("can complete trip in time")
                                    print()
                            else:
                                if cross:
                                    print(next_start_time.strftime("%H:%M:%S"), "<", total_time.strftime("%H:%M:%S"))
                                    print("cannot complete trip in time")
                                print()

        offspring.append(offspring_chromosome)
        if cross:
            print("parents: ")
            print(parents[c])
            print(parents[c + 1])
            print("child:")
            print(offspring_chromosome)
    return offspring
    #35 offspring and 35 parents
    # excluding two times
    # randomize distance & time slightly
# json webpag with map api
# 4:00 am1

# def mutation(offspring):
#    for i in range(len(offspring)):
