import csv
import matplotlib.pyplot as plt
import numpy as np
import math

#pure-water-s2/1 ...,2,3,4
#pure-organic-s2/1 ...2,3,4
#25o-75w-s2/1 ...2,3,4
#25w-75o-s2/1
#50o-50w-prelim/1 ...2,3

xls = './25w-75o-s2/1'
results = xls + '/results.xls'
processed_results = xls + '/processed_result.csv'


lines = []

with open(results, 'r') as f:
    reader = csv.reader(f, delimiter='\t')

    for line in reader:
        lines.append(line)

for line in lines:
    if len(line) == 1:
        print line

particle_count = raw_input("Please interpret particle count!\nParticle count = ")
format_particle_offset = raw_input("Please interpret particles per set!\nNOTE: EXAMPLE ['Tracks 1 to 75'] per set 75 particles (count from 0)\nParticles per set = ")
print particle_count

frames = []
do = 0
done = 0

for line in lines:
    if len(line) == 1:
        if do == 0:
            do = 1
        elif do == 1:
            done = 1
            do = 0
    else:
        if do == 1 and done != 1:
            frames.append(line[0])

print str(len(frames)) + ' frames to process'
print particle_count + ' particles to process'

frame_particles_pos = [0]*int(particle_count)
particles_pos = [frame_particles_pos]*len(frames)

frame_count = 0
while frame_count < len(frames):
    frame_particles_pos = [0]*int(particle_count)
    add_particle_offset = -int(format_particle_offset)
    for line in lines:
        if len(line) == 1:
            add_particle_offset += int(format_particle_offset)
        if line[0] == str(frame_count):
            # print line
            cursor = 0
            for element in line:
                add_particle_count = 0
                while cursor < len(line):
                    if cursor == 0:
                        cursor += 1
                    if cursor != 0:
                        if len(line) > 1:
                            if line[cursor] != ' ' and line[cursor+1] != ' ':
                                # print 'x: ' + str(line[cursor]) + 'y: ' + str(line[cursor+1])
                                frame_particles_pos[add_particle_count+add_particle_offset] = (line[cursor], line[cursor+1])
                        add_particle_count += 1
                        cursor += 3
    particles_pos[frame_count] = frame_particles_pos
    frame_count += 1

# print particles_pos[87]
# print particles_pos[0]
#print particles_pos[1][1] # frame 1, particle number 2
#print particles_pos[87][150] #frame 87, particle number 151
# print len(particles_pos[87])

raw_input('particles upload complete. press enter to continue')
mode = raw_input('choose mode...\n1: linear fit\n2:normal dist\n?')
if int(mode) == 1:
    fps = float(raw_input('fps?\nfps='))
    time_interval = 1.0/float(fps)

    time = []
    time_count = 0.0
    for frame in frames:
        time.append(time_count * time_interval)
        time_count += 1.0

    particles_MSD = []
    index = 0
    while index < int(particle_count):
        particle_MSD = []
        ref_particle_pos = -1
        frame_count = 0
        for frame in frames:
            position_in_frame = particles_pos[frame_count][index]
            if type(position_in_frame) != type(1):
                if ref_particle_pos == -1:
                    ref_particle_pos = position_in_frame
                    particle_MSD.append(0)
                else:
                    particle_MSD.append((( ((float(position_in_frame[0]) - float(ref_particle_pos[0])) ** 2.0) + ((float(position_in_frame[1]) - float(ref_particle_pos[1])) ** 2.0) ) ** (0.5)) ** (2.0))
            else:
                particle_MSD.append(0)
            frame_count += 1
        particles_MSD.append(particle_MSD)
        print('particle ' + str(index) + ' analyzed')
        index += 1

    print particles_MSD[0][16]
    print particles_MSD[0][17]
    print particles_MSD[0][18]

    net_MSD = []

    frame_count = 0
    for frame in frames:
        total = 0.0
        count = 0.0
        for pMSD in particles_MSD:
            if pMSD[frame_count] != 0.0 and pMSD[frame_count] != 0:
                total += pMSD[frame_count]
                count += 1.0
        if count == 0 or count == 0.0:
            net_MSD.append(0)
        else:
            net_MSD.append(float(total)/float(count))
        frame_count += 1

    scaled_net_MSD = []
    #rescaling distances
    for MSD in net_MSD:
        scaled_net_MSD.append(MSD*(150.0/538.0))

    plt.plot(time, scaled_net_MSD)
    plt.show()


    csv.register_dialect(
        'EXCEL',
        delimiter = ',',
        quotechar = '"',
        doublequote = True,
        skipinitialspace = True,
        lineterminator = '\n',
        quoting = csv.QUOTE_MINIMAL)

    with open(processed_results, 'w') as file:
        writer = csv.writer(file, dialect='EXCEL')
        cursor = 0
        for t in time:
            writer.writerow([t, scaled_net_MSD[cursor]])
            cursor += 1

elif int(mode) == 2:
    min_length = int(raw_input('min frame length?'))
    raw_input('this might take a while. press enter to go.')

    # frame_1 = 1
    # frame_2 = 2
    # sframe_1 = -1
    # sframe_2 = -1
    # top_save = []
    # while frame_1 < len(frames):
    #     frame_2 = frame_1
    #     while frame_2 < len(frames):
    #         if frame_2 > frame_1:
    #             print 'checking between frames ' + str(frame_1) + ' and ' + str(frame_2)
    #             i = 0
    #             saves_1 = []
    #             for particle_position in particles_pos[frame_1]:
    #                 if type(particle_position) != type(1):
    #                     saves_1.append(i)
    #                 i += 1
    #             i = 0
    #             saves_2 = []
    #             for particle_position in particles_pos[frame_2]:
    #                 if type(particle_position) != type(1):
    #                     saves_2.append(i)
    #                 i += 1
    #             save = list(set(saves_1).intersection(saves_2))
    #             if len(save) > len(top_save) and (frame_2 - frame_1)>=min_length:
    #                 top_save = save
    #                 sframe_1 = frame_1
    #                 sframe_2 = frame_2
    #         frame_2 += 1
    #     frame_1 += 1
    #
    # print 'found best interval'
    # print top_save
    # print 'between frames ' + str(sframe_1) + ' and ' + str(sframe_2)
    #
    # displacements = []
    # for particle in top_save:
    #     d = (((float(particles_pos[sframe_2][particle][0])) - float(particles_pos[sframe_1][particle][0])) ** 2.0 + ((float(particles_pos[sframe_2][particle][1])) - float(particles_pos[sframe_1][particle][1])) ** 2.0) ** (0.5)
    #     #x2-x1 its a vector!
    #     #d2 = (( float((particles_pos[sframe_2][particle][0])) ** 2.0) + ( float(particles_pos[sframe_2][particle][1]) ** 2.0)) ** (0.5)
    #     #d1 = (( float((particles_pos[sframe_1][particle][0])) ** 2.0) + ( float(particles_pos[sframe_1][particle][1]) ** 2.0)) ** (0.5)
    #     #d = d2 - d1
    #     displacements.append(d)
    #
    # print displacements
    # bin_size = float(raw_input('whats the size of you bin yo'))
    # hist, bins = np.histogram(displacements, bins=bin_size)
    # width = 0.7 * (bins[1] - bins[0])
    # center = (bins[:-1] + bins[1:])/2
    #
    # plt.bar(center, hist, align='center', width=width)
    # plt.show()
    #
    # print 'old way of variance val:'
    # print np.var(displacements, ddof=1)

    sframe_1 = 2
    frame_gap = min_length
    variances = []
    all_displacements = []
    o_all_displacements = []
    check_displacements = []
    track_counting = [0] * len(particles_pos[1])
    factor = (150.0/538.0) * (10 ** (-6))

    while sframe_1 + frame_gap < len(frames):
        sframe_2 = sframe_1 + frame_gap
        print 'now analyzing frame ' + str(sframe_1) + ' to frame ' + str(sframe_2) + ' of ' + str(len(frames)) + ' total frames.'
        displacements = []
        o_displacements = []

        i = 0

        for particle_position in particles_pos[sframe_1]:
            do = True

            if type(particles_pos[sframe_2][i]) != type(1) and type(particles_pos[sframe_1][i] != type(1)):
                print 'we got one'
            else:
                do = False

            if do:
                if type(particles_pos[sframe_1][i]) != type(1):
                    if type(particles_pos[sframe_2][i]) != type(1):
                        d = (float(particles_pos[sframe_2][i][1]) * factor) - (float(particles_pos[sframe_1][i][1]) * factor)
                        #d = (((float(particles_pos[sframe_2][i][0]))* factor - float(particles_pos[sframe_1][i][0]) * factor) ** 2.0 + ((float(particles_pos[sframe_2][i][1])) * factor - float(particles_pos[sframe_1][i][1]) * factor) ** 2.0) ** (0.5)
                        track_counting[i] += 1
                        displacements.append(d)


            i += 1

        if not math.isnan(np.var(displacements, ddof=1)):
            variances.append(np.var(displacements, ddof=1))
        all_displacements.extend(displacements)
        check_displacements.extend(displacements)
        sframe_1 += frame_gap + 1

    print variances
    print str(sum(variances)/(len(variances)))
    print np.var(check_displacements, ddof = 1)

    csv.register_dialect(
    'EXCEL',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)

    with open(xls + '/TEST.csv', 'w') as file:
        writer = csv.writer(file, dialect='EXCEL')
        for variance in variances:
            writer.writerow([variance])

    bin_size = float(raw_input('whats the size of you bin yo'))
    hist, bins = np.histogram(all_displacements, bins=bin_size)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:])/2

    print hist
    print center
    print bins

    csv.register_dialect(
    'EXCEL',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)

    with open(xls + '/hist.csv', 'w') as file:
        writer = csv.writer(file, dialect='EXCEL')
        for histt in hist:
            writer.writerow([histt])
    with open(xls + '/center.csv', 'w') as file:
        writer = csv.writer(file, dialect='EXCEL')
        for i in center:
            writer.writerow([i])
    with open(xls + '/bins.csv', 'w') as file:
        writer = csv.writer(file, dialect='EXCEL')
        for bin in bins:
            writer.writerow([i])



    plt.bar(center, hist, align='center', width=width)
    plt.show()

