import pandas as pd
import numpy as np 
import tensorflow as tf
class rl:
    def __init__(self,num_f, num_a, reward_decay=0.9, greedy=0.9,learing_rate=0.01, replace_num=300, batch_size=50,e_greedy_increment=None, memory_size=500):
        self.num_f = num_f
        self.num_a = num_a
        self.lr = learing_rate
        self.gamma = reward_decay
        self.epsilon_max = greedy
        self.replace_num = replace_num
        self.batch_size = batch_size
        self.memory_size = memory_size
        self.learn_step_counter = 0
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max
        self.memory = np.zeros((self.memory_size, self.num_f*2+2))
        self.nnet()
#        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        t_params =  tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='target_net')
        print(t_params)
        eval_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='pred_net')
        self.cost_his = []
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        with tf.variable_scope('hard_replacement'):
            self.target_replace_op = [tf.assign(t, e) for t, e in zip(t_params, eval_params)]
    def nnet(self):
        # ------------------ all inputs ------------------------
        self.s = tf.placeholder(tf.float32, [None, self.num_f], name='s')  # input State
        self.s_ = tf.placeholder(tf.float32, [None, self.num_f], name='s_')  # input Next State
        self.r = tf.placeholder(tf.float32, [None, ], name='r')  # input Reward
        self.a = tf.placeholder(tf.int32, [None, ], name='a')  # input Action
        w_init, b_init = tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)
        with tf.variable_scope('pred_net'):
            e1 = tf.layers.dense(self.s, 100, tf.nn.tanh, kernel_initializer=w_init,
                                 bias_initializer=b_init, name='e1')
            self.q_eval = tf.layers.dense(e1, self.num_a, kernel_initializer=w_init,
                                          bias_initializer=b_init, name='q')
        
        # ------------------ build target_net ------------------
        with tf.variable_scope('target_net'):
            t1 = tf.layers.dense(self.s_, 100, tf.nn.tanh, kernel_initializer=w_init,
                                 bias_initializer=b_init, name='t1')
            self.q_next = tf.layers.dense(t1, self.num_a, kernel_initializer=w_init,
                                          bias_initializer=b_init, name='t2')

        with tf.variable_scope('q_target'):
            q_target = self.r + self.gamma * tf.reduce_max(self.q_next, axis=1, name='Qmax_s_')    # shape=(None, )
            self.q_target = tf.stop_gradient(q_target)
        with tf.variable_scope('q_eval'):
            a_indices = tf.stack([tf.range(tf.shape(self.a)[0], dtype=tf.int32), self.a], axis=1)
            self.q_eval_wrt_a = tf.gather_nd(params=self.q_eval, indices=a_indices)    # shape=(None, )
        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval_wrt_a, name='TD_error'))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)
                        
    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0
        transition = np.hstack((s, [a, r], s_))
        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition
        self.memory_counter += 1
        
    def choose_action(self, obs:np.array):
#        print(obs,'hello')
        # to have batch dimension when feed into tf placeholder
        obs = np.array(obs)[np.newaxis,:]
        
        if np.random.uniform() < self.epsilon:
            # forward feed the observation and get q value for every actions
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: obs})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.num_a)
        return action

    def learning(self):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_num == 0:
            self.sess.run(self.target_replace_op)
            print('\ntarget_params_replaced\n')

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        _, cost = self.sess.run(
            [self._train_op, self.loss],
            feed_dict={
                self.s: batch_memory[:, :self.num_f],
                self.a: batch_memory[:, self.num_f],
                self.r: batch_memory[:, self.num_f + 1],
                self.s_: batch_memory[:, -self.num_f:],
            })

        self.cost_his.append(cost)
        print(cost)
        # increasing epsilon
        self.epsilon = 0.9
        self.learn_step_counter += 1
