import numpy as np


class Bandit:
    def __init__(self, μ, σ, seed=0):
        self.k = len(μ)
        self.μ = μ
        self.σ = [σ] * self.k if np.isscalar(σ) else σ
        self.rng = np.random.default_rng(seed)
 
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def pulled(self, arm):
        return self.rng.normal(self.μ[arm], self.σ[arm])


class Greedy:
    def __init__(self, k, ε=0, reward=None, count=None, seed=0):
        self.k = k
        self.ε = ε
        self.reward = reward or np.zeros(k)
        self.count = count or np.zeros(k)
        self.rng = np.random.default_rng(seed)
   
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
        
    def pull(self):
        if self.rng.random() < self.ε:
            return self.rng.integers(0, self.k)
        else:
            return np.argmax(self.reward / self.count) # nan comes first
        
    def update(self, reward, arm):
        self.reward[arm] += reward
        self.count[arm] += 1


class Optimistic:
    def __init__(self, k, ε=0., α=0.1, q0=0., seed=0):
        self.k = k
        self.ε = ε
        self.α = α
        self.q = np.full(k, q0, dtype=np.float_)
        self.rng = np.random.default_rng(seed)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def pull(self):
        if self.rng.random() < self.ε:
            return self.rng.integers(0, self.k)
        else:
            return np.argmax(self.q)

    def update(self, reward, arm):
        self.q[arm] += self.α * (reward - self.q[arm])        
        

class NonStationaryGreedy:
    def __init__(self, k, ε=0.1, α=0.5, denom=0., initial=0., seed=0):
        self.k = k
        self.ε = ε
        self.α = α
        self.denom = np.full(k, denom, dtype=np.float_)
        self.q = np.full(k, initial, dtype=np.float_)
        self.rng = np.random.default_rng(seed)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def pull(self):
        if self.rng.random() < self.ε:
            return self.rng.integers(0, self.k)
        else:
            return np.argmax(self.q)

    def update(self, reward, arm):
        self.denom[arm] += self.α * (1 - self.denom[arm])
        self.q[arm] += self.α / self.denom[arm] * (reward - self.q[arm])  


class UCB:
    def __init__(self, k, c=1, t=1, q=None, n=None):
        self.k = k
        self.c = c
        self.t = t
        self.q = q or np.zeros(k)
        self.n = n or np.zeros(k)
   
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
        
    def pull(self):
        return np.argmax(self.q + self.c*np.sqrt(np.log(self.t)/self.n)) # nan comes first
        
    def update(self, reward, arm):
        self.t += 1
        self.n[arm] += 1
        self.q[arm] += (reward - self.q[arm]) / self.n[arm]


class Gradient:
    def __init__(self, k, α=0.1, h=None, t=0, baseline=None, seed=0):
        self.k = k
        self.α = α
        self.h = h or np.zeros(k)
        self.t = t
        self.baseline = baseline
        self.objective = False if np.isscalar(baseline) else True
        self.rng = np.random.default_rng(seed)
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def pull(self):
        π = np.exp(self.h)
        π /= np.sum(π)
        return self.rng.choice(self.k, p=π)
    
    def update(self, reward, arm):
        self.t += 1
        
        π = np.exp(self.h)
        π /= -np.sum(π)
        π[arm] += 1
        
        if self.objective and self.t == 1:
            self.baseline = reward

        self.h += self.α * (reward - self.baseline) * π
        
        if self.objective and self.t > 1:
            self.baseline += (reward - self.baseline) / self.t


def play(bandit, player, t=1):
    reward = np.zeros(t)
    hit = np.zeros(t)
    champion = np.argmax(bandit.μ)
    
    for i in range(t):
        arm = player.pull()
        hit[i] = arm == champion
        reward[i] = bandit.pulled(arm)
        player.update(reward[i], arm)   
        
    return reward, hit