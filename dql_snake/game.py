from snake_core import rl
from tk_test import snake

def run():
    for i in range(100):
        observation = [90,90,100,100]
        g.reset()
        while True:
            g.initGame()
            action = rl.choose_action(str(observation))
            s_, reward, end  = g.go(action)
            rl.learning(str(observation),action, reward, str(s_))
            observation = s_
            g.master.after(10,g.master.update())
            print(reward)
            if end:
                break
    # g.canvas.mainloop()           
if __name__ == "__main__":
    g = snake(200,200)
    rl = rl(action=list(range(g.n_actions)))
    # g.master.after(100, run)
    # g.master.after(100,run)
    run()
    # g.master.after(100,run)
    g.master.mainloop()
    