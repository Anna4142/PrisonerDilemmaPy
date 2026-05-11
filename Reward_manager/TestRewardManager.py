from Reward_manager.RewardManager import RewardManager
import datetime

# reward system configuration"
recipients = [{'Coo': 1,
               'Cen': 2,
               'Def': 3},
              {'Coo': 4,
               'Cen': 5,
               'Def': 6}]

rewards = [{'CC': 120,
            'CD': 0,
            'DC': 160,
            'DD': 30,
            'CN': 20},
           {'CC': 100,
            'CD': 10,
            'DC': 120,
            'DD': 40,
            'CN': 0}]

opcode = -1
comport = input("Comport: ")
reward_manager = RewardManager(comport, recipients, rewards)
rewards = []

while opcode != 0:
    opcodestr = input("opcode [0- exit, 1- set reward, 2- deliver]: ")
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

    else:
        print ("illegal opcode")