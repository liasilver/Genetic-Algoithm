from datetime import datetime, timedelta
import haversine as hs
import random


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

#
# def crossover(parents, cross):
#     offspring = [[[]]]
#
#     for c in range(1, len(parents)):
#         # create chromosome with 1 gene from parent1 and 2 genes from parent2
#         offspring_chromosome = [[]]
#         for g in range(len(parents)):
#             if cross:
#                 print("mate 1:", parents[c][g])
#             if parents[c][g][1]:
#                 possible_mates = [[]]
#                 previous_start_time = datetime(year=1, month=1, day=1, hour=(int(parents[c][g][1].split(":")[0])),minute=(int(parents[c][g][1].split(":")[1])))
#                 if cross:
#                     print("mate 1 start time:", previous_start_time.strftime("%H:%M:%S"))
#                 duration = int(parents[c][g][7])
#                 if cross:
#                     print("duration:", duration)
#                 window = 1200 # 20 minutes in seconds
#
#                 total_time = previous_start_time + timedelta(seconds=duration + window)
#                 if cross:
#                     print("total time (duration + start):", total_time.strftime("%H:%M:%S"))
#                 print()
#                 for c2 in range(1, len(parents)):
#                     for g2 in range(3):
#                         if parents[c2][g2][1] and parents[c2][g2] != parents[c2][g]:
#                             if cross:
#                                 print("possible mate 2:", parents[c2][g2])
#
#                             next_start_time = datetime(year=1, month=1, day=1, hour=(int(parents[c2][g2][1].split(":")[0])), minute=(int(parents[c2][g2][1].split(":")[1])))
#                             if cross:
#                                 print("start_time", next_start_time.strftime("%H:%M:%S"))
#
#                             if next_start_time > total_time:
#                                 if cross:
#                                     print(next_start_time.strftime("%H:%M:%S"), ">", total_time.strftime("%H:%M:%S"))
#                                 possible_mates.append(parents[c2][g2])
#                                 if cross:
#                                     print("can complete trip in time")
#                                     print()
#                             else:
#                                 if cross:
#                                     print(next_start_time.strftime("%H:%M:%S"), "<", total_time.strftime("%H:%M:%S"))
#                                     print("cannot complete trip in time")
#                                 print()
#
#         offspring.append(offspring_chromosome)
#         if cross:
#             print("parents: ")
#             print(parents[c])
#             print(parents[c + 1])
#             print("child:")
#             print(offspring_chromosome)
#     return offspring

def find_mates(gene, parents, mates):
    #  remember, you're looping through half the population (35)
    possible_mates = []

    for c2 in range(1, len(parents)):
        for g2 in range(3):
            if not parents[c2][g2][1]:
                possible_mates.append(parents[c2][g2])

    if gene[1]:  # if pickup time is not null

        previous_start_time = datetime(year=1, month=1, day=1, hour=(int(gene[1].split(":")[0])),
                                       minute=(int(gene[1].split(":")[1])))
        duration = int(gene[7])
        window = 1200  # 20 minutes in seconds, will find exact estimates for driving window later
        tot_time = previous_start_time + timedelta(seconds=duration + window)

        if mates:
            print("mate 1:", gene)
            print("mate 1 start time:", previous_start_time.strftime("%H:%M:%S"))
            print("duration", duration)
            print("total time (duration + start):", tot_time.strftime("%H:%M:%S"))
            print()

        for c in range(1, len(parents)):
            for g in range(3):  # 3 genes per chromosome
                if parents[c][g][1]:
                    next_start_time = datetime(year=1, month=1, day=1, hour=(int(parents[c][g][1].split(":")[0])),
                                               minute=(int(parents[c][g][1].split(":")[1])))
                    if mates:
                        print("possible mate 2:", parents[c][g])
                        print("start_time", next_start_time.strftime("%H:%M:%S"))
                    if next_start_time >= tot_time:
                        possible_mates.append(parents[c][g])
                        if mates:
                            print(next_start_time.strftime("%H:%M:%S"), ">", tot_time.strftime("%H:%M:%S"))
                            print("can complete trip in time")
                            print()
                    else:
                        if mates:
                            print(next_start_time.strftime("%H:%M:%S"), "<", tot_time.strftime("%H:%M:%S"))
                            print("cannot complete trip in time")
                            print()

    return possible_mates


def crossover(parents, cross, remove_genes):
    offspring = [[[]]]

    for c in range(1, len(parents)):
        for g in range(3):
            if parents[c][g][1]:
                gene1 = parents[c][g]
                remove_genes.append(gene1)
                gene2 = random.choice(find_mates(gene1, get_updated_parents(remove_genes, parents), mates=False))
                remove_genes.append(gene2)
                gene3 = random.choice(find_mates(gene2, get_updated_parents(remove_genes, parents), mates=False))
                remove_genes.append(gene3)
                if cross:
                    print("gene1:", gene1)
                    print("gene2:", gene2)
                    print("gene3:", gene3)
                    print()


# def get_updated_parents(remove_genes, parents):
#     temp_parents = []
#     for c in range(1, len(parents)):
#         for g in range(3):
#             temp_parents.append(parents[c][g])
#
#     print("remove genes:", len(remove_genes))
#     updated = [elem for elem in temp_parents if elem not in remove_genes]
#     print("updated parents:", len(updated))
#     return updated

def get_updated_parents(remove_genes, parents):
    return [elem for elem in parents if elem not in remove_genes]


# def mutation(offspring):
#    for i in range(len(offspring)):
