# Chapter 3 Finite Markov Decision Processes

$$
p(s',r|s,a) := \Pr\{S_t=s', R_t=r | S_{t-1}=s, A_{t-1}=a\}
$$

$$
p(s'|s,a) := \Pr\{S_t=s'|S_{t-1}=s, A_{t-1}=a\} = \sum_{r\in\mathcal{R}} p(s',r|s,a)
$$

$$
r(s,a) := \mathbb{E}[R_t|S_{t-1}=s, A_{t-1}=a] = \sum_{r\in\mathcal{R}}r \sum_{s'\in\mathcal{S}} p(s',r|s,a)
$$

$$
r(s,a,s') := \mathbb{E}[R_t|S_{t-1}=s, A_{t-1}=a, S_t=s'] = \sum_{r\in\mathcal{R}}r \frac{p(s',r|s,a)}{p(s'|s,a)}
$$

$$
v_\pi(s) := \mathbb{E}_\pi [G_t|S_t=s]
$$

$$
q_\pi(s,a) := \mathbb{E}_\pi [G_t | S_t=s, A_t=a]
$$

$$
\begin{align}
v_\pi(s) := & \mathbb{E}_\pi [G_t|S_t=s] \\
          = & \mathbb{E}_\pi [R_{t+1}+\gamma G_{t+1}|S_t=s] \\
          = & \sum_a \pi(a|s) \sum_{s'}\sum_r p(s',r|s,a)[r+\gamma\mathbb{E}_\pi [G_{t+1}|S_{t+1}=s']] \\
          = & \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r+\gamma v_\pi(s')] 
\end{align}
$$


$$
\begin{align}
q_\pi(s,a) := & \mathbb{E}_\pi [G_t|S_t=s,A_t=a] \\
            = & \mathbb{E}_\pi [R_{t+1}+\gamma G_{t+1}|S_t=s,A_t=a] \\
            = & r(s,a) + \gamma \sum_{s',a'} \pi(a'|s') p(s'|s,a) q_\pi(s',a') \\
            = & \sum_{s',r}rp(s',r|s,a) + \gamma \sum_{s',a',r}  p(s',r|s,a) \pi(a'|s') q_\pi(s',a')
\end{align}
$$
