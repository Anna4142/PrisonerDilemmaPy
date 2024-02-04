from Reward_manager.RewardManager import RewardManager
from Video_analyser_code.locations import Locations


opcode = -1
comport = input("Comport: ")
reward_manager = RewardManager(comport)
rewards = []

while opcode != 0:
    opcodestr = input("opcode [0- exit, 1- set reward, 2- deliver]: ")
    opcode = int(opcodestr)

    if opcode == 0:
        print("Program terminated")

    elif opcode == 1:
        mouse = int(input("Mouse ID: "))
        location = Locations(int(input("1- Cooperate, 2- Center, 3- Defect: ")))
        duration = float(input("Duration: "))
        rewards.append([mouse, location, duration])

    elif opcode == 2:
        for i in range(len(rewards)):
            reward_manager.deliver_reward(rewards[i][0], rewards[i][1], rewards[i][2])
        while not reward_manager.is_reward_delivered():
            pass
        rewards = []

    else:
        print ("illegal opcode")