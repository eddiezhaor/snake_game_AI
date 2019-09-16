import pandas as pd
import numpy as np 

class rl:
    def __init__(self,action, reward_decay=0.9, greedy=0.9,learing_rate=0.1):
        self.actions = action
        self.lr = learing_rate
        self.gamma = reward_decay
        self.epislon = greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def choose_action(self, obs):
        self.check_state(obs)
        if np.random.uniform() < self.epislon:
            s_action = self.q_table.loc[obs,:]
            action = np.random.choice(s_action[s_action==np.max(s_action)].index)
        else:
            action = np.random.choice(self.actions)
        return action

    def learning(self,n,a,r,n_):
        self.check_state(n_)
        q_predict = self.q_table.loc[n,a]
        if n_ != 'terminal':
            q_target = r + self.gamma * (self.q_table.loc[n_,:].max())
        else:
            q_target = r
        self.q_table.loc[n,a] += self.lr*(q_target - q_predict)

    def check_state(self,state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index = self.q_table.columns,
                    name = state
                )
            )