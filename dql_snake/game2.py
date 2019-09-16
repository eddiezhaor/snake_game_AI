from snake_core_dqn import rl
from tk_test3 import snake
import numpy as np
def run():
    step = 0
    for i in range(100):
        observation = [90,90,100,100]
        g.reset()
        while True:
            g.initGame()
            action = rl.choose_action(observation)
            print(action)
            s_, reward, end  = g.go(action)
            rl.store_transition(observation,action, reward, s_)

            if (step>200) and (step % 5==0):
                rl.learning()
            observation = s_
            g.master.after(10,g.master.update())
#            print(rl.cost_his)
            if end:
                break
            step +=1
    # g.canvas.mainloop()           
if __name__ == "__main__":
    g = snake(200,200)
    rl = rl(num_f =4, num_a=4)
    # g.master.after(100, run)
    # g.master.after(100,run)
    run()
    # g.master.after(100,run)
    g.master.mainloop()
    