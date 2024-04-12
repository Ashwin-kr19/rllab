import numpy as np
import random

# random.choice([1,2,3,4,5,6])

"""# Monte Carlo"""

# let us consier a process with 0 as start state and 2 as end state:
# 0 <-> 1 -> 2(end state)
# we shall create episodes and update q values using on and off policies

episodes = [[[0, "R", 10, 1], [1, "L", 1, 0], [0, "R", 15, 1], [1, "R", 35, 2]], [[0, "R", 15, 1], [1, "R", 25, 2]]]

"""## On Policy"""

class monte_carlo_on:
    def __init__(self, n, gamma, eps, episodes):
        self.episodes = episodes
        self.n = n
        self.gamma = gamma
        self.eps = eps
        self.q = dict()
        self.policy = dict()
        # self.actions = actions


    def possible_state_action_pair(self):
        state_action_pair = list()

        for i in self.episodes:
            for ind, step in enumerate(i):
                if (step[0], step[1]) not in state_action_pair:
                    state_action_pair.append((step[0], step[1]))

        print(state_action_pair)

        return state_action_pair


    def update(self):
        state_action_pair = self.possible_state_action_pair()

        for k in state_action_pair:
            for i in self.episodes:
                returns = 0
                for ind, step in enumerate(i):
                    if step[0] == k[0] and step[1] == k[1]:

                        returns = returns + ((self.gamma ** ind) * step[2])
                        print(ind, returns)

                        if (step[0], step[1]) not in self.q:
                            self.q[(step[0], step[1])] = [returns, 1]

                        else:
                            self.q[(step[0], step[1])] = [self.q[(step[0], step[1])][0] + returns, self.q[(step[0], step[1])][1] + 1]

        print(self.q)

        for i in self.q:
            self.q[i] = self.q[i][0] / len(episodes)


        return self.q


    def generate_random_no(self):
        return np.random.uniform(0,1)


    def update_policy(self):
        for i in range(0, self.n-1, 1):
            actions = dict()

            for k in self.q:
                if i == k[0]:
                    if k[1] not in actions:
                        actions[k[1]] = self.q[k]


            greedy_action = None
            soft_action = None
            max_val = float('-inf')

            for act in actions:
                if actions[act] > max_val:
                    max_val = actions[act]
                    greedy_action = act

            rand_no = self.generate_random_no()

            print(rand_no)
            print(list(actions.keys()))


            if rand_no <= self.eps:
                soft_action = random.choice(list(actions.keys()))
            else:
                soft_action = greedy_action

            self.policy[i] = soft_action

        return self.policy

obj = monte_carlo_on(3, 0.1, 0.9, episodes)
obj.update()

obj.update_policy()

"""## Off Policy"""



class monte_carlo_off:
    def __init__(self, n, actions, gamma, eps, episodes):
        self.episodes = episodes
        self.n = n
        self.actions = ["L","R"]
        self.gamma = gamma
        self.eps = eps
        self.q = dict()
        self.policy = {0:'R', 1:'R'}

        self.c = dict()

        for i in range(0, self.n-1, 1):
            for j in self.actions:
                self.c[(i,j)] = 0

        print(self.c)
        # self.actions = actions


    def find_probability(self,state,action):
        total = 0
        count = 0

        for i in self.episodes:
            for ind,step in enumerate(i):
                if step[0] == state:
                    total += 1

                    if step[1] == action:
                        count += 1

        return count/total


    def update(self):
        # episodes = [[[0, "R", 10, 1], [1, "L", 1, 0], [0, "R", 15, 1], [1, "R", 35, 2]], [[0, "R", 15, 1], [1, "R", 25, 2]]]
        for i in self.episodes:
            returns = 0
            w = 1
            for ind, step in enumerate(i):
                returns = returns + ((self.gamma ** ind) * step[2])
                print(ind, returns)

                self.c[(step[0], step[1])] = self.c[(step[0], step[1])] + w

                if (step[0], step[1]) not in self.q:
                    self.q[(step[0], step[1])] = 0

                self.q[(step[0], step[1])] = self.q[(step[0], step[1])] + ((w /self.c[(step[0], step[1])]) * (returns - self.q[(step[0], step[1])]))

                w = w * (1 / self.find_probability(step[0], step[1]))

                if w == 0:
                    break
                # if (step[0], step[1]) not in self.q:
                #     self.q[(step[0], step[1])] = [returns, 1]

                # else:
                #     self.q[(step[0], step[1])] = [self.q[(step[0], step[1])][0] + returns, self.q[(step[0], step[1])][1] + 1]

        print(self.q)

        # for i in self.q:
        #     self.q[i] = self.q[i] / len(episodes)


        return self.q


    def generate_random_no(self):
        return np.random.uniform(0,1)

    # def update_policy(self):
    #     for i in range(0, self.n-1, 1):
    #         actions = dict()

    #         for k in self.q:
    #             if i == k[0]:
    #                 if k[1] not in actions:
    #                     actions[k[1]] = self.q[k]


    #         greedy_action = None
    #         soft_action = None
    #         max_val = float('-inf')

    #         for act in actions:
    #             if actions[act] > max_val:
    #                 max_val = actions[act]
    #                 greedy_action = act

    #         rand_no = self.generate_random_no()

    #         print(rand_no)
    #         print(list(actions.keys()))


    #         if rand_no <= self.eps:
    #             soft_action = random.choice(list(actions.keys()))
    #         else:
    #             soft_action = greedy_action

    #         self.policy[i] = soft_action

    #     return self.policy

obj = monte_carlo_off(3, [], 0.1, 0.9, episodes)
obj.update()



"""# TD"""

episodes

"""## SARSA"""

class sarsa:
    def __init__(self, n, alpha, gamma, eps, episodes):
        self.episodes = episodes
        self.n = n
        self.gamma = gamma
        self.eps = eps
        self.alpha = alpha
        self.q = dict()


    def choose_eps_action(self, state):

        actions = dict()

        if len(self.q) == 0:
            actions = list()
            for i in self.episodes:
                for ind,step in enumerate(i):
                    if step[0] == state:
                        actions.append(step[1])


            return random.choice(actions)


        for k in self.q:
            if state == k[0]:
                if k[1] not in actions:
                    actions[k[1]] = self.q[k]


        greedy_action = None
        soft_action = None
        max_val = float('-inf')

        for act in actions:
            if actions[act] > max_val:
                max_val = actions[act]
                greedy_action = act

        rand_no = self.generate_random_no()

        if rand_no <= self.eps:
            soft_action = random.choice(list(actions.keys()))
        else:
            soft_action = greedy_action

        print(soft_action)

        return soft_action

    def generate_random_no(self):
        return np.random.uniform(0,1)

    def update(self):
        for i in self.episodes:
            for ind, step in enumerate(i):
                a = self.choose_eps_action(step[0])
                r = step[2]
                s_ = step[3]
                s = step[0]
                a_ = self.choose_eps_action(s_)

                # print(a,r,s_,s,a_)

                if (s,a) not in self.q:
                    self.q[(s,a)] = 0

                if (s_,a_) not in self.q:
                    self.q[(s_,a_)] = 0

                self.q[(s,a)] = self.q[(s,a)] + self.alpha * (r + self.gamma * (self.q[(s_,a_)] - self.q[(s,a)]))

        return self.q

obj = sarsa(3, 0.1, 0.1, 0.1, episodes)

obj.update()

