from Reward_manager.RewardManager import RewardManager
import datetime

# reward system configuration"
valves = {'M1 Coo': {'Channel': '1',
                     'flow unit': '1'},
          'M1 Cen': {'Channel': '2',
                     'flow unit': '3'},
          'M1 Def': {'Channel': '3',
                     'flow unit': '5'},
          'M2 Coo': {'Channel': '4',
                     'flow unit': '2'},
          'M2 Cen': {'Channel': '6',
                     'flow unit': '4'},
          'M2 Def': {'Channel': '5',
                     'flow unit': '6'}}

m1_rewards = {'CC': '12',
              'CD': '0',
              'DC': '16',
              'DD': '3',
              'CN': '2'}

m2_rewards = {'CC': '10',
              'CD': '1',
              'DC': '12',
              'DD': '4',
              'CN': '0'}

opcode = -1
comport = input("Comport: ")
reward_manager = RewardManager(comport, valves, m1_rewards, m2_rewards)
rewards = []

while opcode != 0:
    opcodestr = input("opcode [0- exit, 1- set reward, 2- deliver, 3- get reward]: ")
    opcode = int(opcodestr)

    if opcode == 0:
        print("Program terminated")

    elif opcode == 1:
        mouse = int(input("Mouse ID (1 or 2): "))
        scenario = input('Valid scenarios: CC, CD, DC, DD, CN: ')
        rewards.append([mouse, scenario])

    elif opcode == 2:
        for i in range(len(rewards)):
            reward_manager.deliver_reward(rewards[i][0], rewards[i][1])
        while not reward_manager.is_reward_delivered():
            pass
        ct = datetime.datetime.now().strftime("%M:%S.%f")
        print (f'Rewards delivered. Time Stamp= {ct}')
        rewards = []

    elif opcode == 3:
        if not rewards:
            print ("set a reward before getting is value")
        else:
            print(f' Reward u/L = {reward_manager.get_reward(rewards[0][0], rewards[0][1])}')


    else:
        print ("illegal opcode")