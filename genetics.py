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


def find_mates(gene, parents, mates):
    # this will be run with a one dimensional array & never null time
    #  remember, you're looping through half the population (105)
    possible_mates = []

    #  automatically we know all null times are possible mates
    for g in range(len(parents)):
        if not parents[g][1]:
            possible_mates.append(parents[g])

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

    for g in range(len(parents)):
        if parents[g][1]:  # if time is not null
            next_start_time = datetime(year=1, month=1, day=1, hour=(int(parents[g][1].split(":")[0])),
                                       minute=(int(parents[g][1].split(":")[1])))
            if mates:
                print("possible mate 2:", parents[g])
                print("start_time", next_start_time.strftime("%H:%M:%S"))

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

    return possible_mates


def crossover(parents, cross, remove_genes):
    offspring = [[[]]]

    for g in range(len(parents)):
        try:
            gene1 = random.choice(get_updated_parents(remove_genes, parents))
        except IndexError:
            break

        if cross:
            print("parent population:", len(get_updated_parents(remove_genes, parents)))
            print("gene1:", gene1)

        remove_genes.append(gene1)

        if gene1[1]:  # if gene1 has specific pickup time
            if cross:
                print("possible mates: ",
                      len(find_mates(gene1, get_updated_parents(remove_genes, parents), mates=False)))
            try:
                gene2 = random.choice(find_mates(gene1, get_updated_parents(remove_genes, parents), mates=False))

            except IndexError:
                gene2 = random.choice(get_updated_parents(remove_genes, parents))

        else:  # if gene has no pickup time
            gene2 = random.choice(get_updated_parents(remove_genes, parents))
        if cross:
            print("gene2:", gene2)
        remove_genes.append(gene2)

        if gene2[1]:
            if cross:
                print("possible mates: ",
                      len(find_mates(gene2, get_updated_parents(remove_genes, parents), mates=False)))
            try:
                gene3 = random.choice(find_mates(gene2, get_updated_parents(remove_genes, parents), mates=False))
            except IndexError:

                gene3 = random.choice(get_updated_parents(remove_genes, parents))
        else:

            gene3 = random.choice(get_updated_parents(remove_genes, parents))

        if cross:
            print("gene3:", gene3)
            print()
        remove_genes.append(gene3)

        chromosome = [gene1, gene2, gene3]
        offspring.append(chromosome)
    return offspring


def get_updated_parents(remove_genes, parents):
    temp_parents = []
    for c in range(1, len(parents)):
        for g in range(3):
            temp_parents.append(parents[c][g])
    updated = [elem for elem in temp_parents if elem not in remove_genes]
    return updated

# def mutation(offspring):
#    for i in range(len(offspring)):
