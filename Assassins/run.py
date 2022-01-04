#! /usr/bin/python3

from random import shuffle
import pickle
import datetime

# UTILS #

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

# END UTILS

#will create dict --> name: [kill-count, alive?, target, gender]
#such that target is another person
def start_new_game():
    print('Create a file with everyone\'s names on separate lines and enter it here (in quotes)')
##    try:
    filename = str(input())
    d = {}
    with open(filename, 'r') as f:
        name_list = f.read().split('\n')[:-1]
        name_list = [i.split(',') for i in name_list]
        shuffle(name_list)
        for i in range(len(name_list)):
            d[name_list[i][0].lower()] = [0, True, name_list[(i + 1) % len(name_list)][0].lower(), name_list[i][1]]
        save_obj(d, 'names')
        print('\nSuccess!\n')
##    except:
##        print('\nInvalid input!\n')

def update_kills():
    print('Who killed their target? (enter in quotes)')
    try:
        name = str(input()).lower()
        d = load_obj('names')

        killer = d[name]
        killed = d[d[name][2]]

        killer[0] += 1 # killer gets a kill
        killer[2] = killed[2] # killer takes new target
        killed[1] = False # killed is no longer alive
        killed[2] = 'None' # killed no longer has a target
        save_obj(d, 'names')
        print('\nSuccess!\n')
    except:
        print('\nInvalid input!\n')

def show_status():
    print('Enter \'<name>\' to show a specific person, or \'everyone\' to show everyone\'s status')
    try:
        name = str(input())
        d = load_obj('names')
        if name == 'everyone':
            for name in d:
                vals = d[name]
                print('{} ({}):\n\tKills: {}\n\tAlive?: {}\n\tTarget: {}\n'.format(name, vals[3], vals[0], vals[1], vals[2]))
        else:
            vals = d[name]
            print('{} ({}):\n\tKills: {}\n\tAlive?: {}\n\tTarget: {}\n'.format(name, vals[3], vals[0], vals[1], vals[2]))
    except:
        print('\nInvalid input!\n')

def export_names_targets(is_alpha):
    d = load_obj('names')
    out = []
    for name in d:
        for_out = get_output_line(name, d[name][3], d[name][2], d[d[name][2]][3])
        out.append(for_out)
    if is_alpha:
        out = sorted(out)
        f = open('nameTargetALPHA.txt', 'w+')
    else:
        f = open('nameTarget.txt', 'w+')
    for i in out:
        print(i)
    out = '\n'.join(out)
    f.write(out)
    f.close()
    print('Done!')

def get_output_line(name1, gen1, name2, gen2):
    end = ''
    if gen1 == gen2 and gen1 == 'Female':
        end = '\t!!!!!!!!!'
    name1 = name1 + (' ' * (20 - len(name1)))
    name2 = name2 + (' ' * (20 - len(name2)))
    gen1 = '(' + gen1 + ')'
    gen1 = gen1 + (' ' * (20 - len(gen1)))
    gen2 = '(' + gen2 + ')'
    gen2 = gen2 + (' ' * (20 - len(gen2)))
    return '{} {} -->\t{} {}{}'.format(name1, gen1, name2, gen2, end)

def export_living_status():
    today = datetime.datetime.today().strftime('%m-%d-%y')
    d = load_obj('names')
    alive = []
    dead = []
    for i in d:
        p = d[i]
        if p[1]:
            alive.append([i + ((20 - len(i)) * ' '), p[3], str(p[0])])
        else:
            dead.append([i + ((20 - len(i)) * ' '), p[3], str(p[0])])
    alive = sorted(alive, key=lambda x: x[0])
    dead = sorted(dead, key=lambda x: x[0])
    alive = ['\t'.join(i) for i in alive]
    dead = ['\t'.join(i) for i in dead]
    f = open('PlayersDeadAlive_{}.txt'.format(today), 'w+')
    f.write('ALIVE\n')
    f.write('\n'.join(alive))
    f.write('\n' + '-' * 30 + '\n\n')
    f.write('DEAD\n')
    f.write('\n'.join(dead))
    f.close()

def get_js_dict():
    d = load_obj('names')
    players = []
    for i in d:
        players.append([i.title(), d[i][0]])
    players = sorted(players)
    players = sorted(players, key=lambda x: x[1], reverse=True)
    for p in players:
        print('\t["{}", {}],'.format(*p))

def go():
    v = ''
    while (True):
        print('What would you like to do?')
        print('0. Start new game')
        print('1. Update kills')
        print('2. Show status')
        print('3. Export name,target to "nameTarget.txt"')
        print('4. Export name,target to "nameTargetALPHA.txt", in alphabetical order')
        print('5. Export living and dead people')
        print('6. Print JS Dict')
        print('7. Exit')
        v = str(input())
        if (v == '0'):
            start_new_game()
        elif (v == '1'):
            update_kills()
        elif (v == '2'):
            show_status()
        elif (v == '3'):
            export_names_targets(False)
        elif (v == '4'):
            export_names_targets(True)
        elif (v == '5'):
            export_living_status()
            print('\nwrote {}\n'.format('PlayersDeadAlive_{}.txt'.format(datetime.datetime.today().strftime('%m-%d-%y'))))
        elif (v == '6'):
            get_js_dict()
        elif (v == '7'):
            break

print('run go()')
