from Reward_manager.RewardManager import RewardManager
import datetime

# reward system configuration"
recipients = [{'Coo': '1',
               'Cen': '2',
               'Def': '3'},
              {'Coo': '4',
               'Cen': '5',
               'Def': '6'}]

rewards = [{'CC': {'opening time': '120', 'water volume': '12'},
            'CD': {'opening time': '0', 'water volume': '0'},
            'DC': {'opening time': '160', 'water volume': '16'},
            'DD': {'opening time': '30', 'water volume': '12'},
            'CN': {'opening time': '20', 'water volume': '2'}},
           {'CC': {'opening time': '121', 'water volume': '13'},
            'CD': {'opening time': '160', 'water volume': '16'},
            'DC': {'opening time': '0', 'water volume': '0'},
            'DD': {'opening time': '31', 'water volume': '3'},
            'CN': {'opening time': '20', 'water volume': '3'}}]

opcode = -1
comport = input("Comport: ")
reward_manager = RewardManager(comport, recipients, rewards)
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
        mouse = int(input("Mouse ID (1 or 2): "))
        scenario = input('Valid scenarios: CC, CD, DC, DD, CN: ')
        print (f'Rewards volume = {reward_manager.get_reward(mouse, scenario)}')

    else:
        print ("illegal opcode")