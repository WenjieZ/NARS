# Chapter 4 Dynamic Programming

## Policy Improvement Theorem

Let $\pi$ and $\pi'$ be any pair of deterministic policies such that, for all $s\in S$,
$$
q_\pi (s, \pi'(s)) \ge v_\pi (s).
$$
 Then the policy $\pi'$ must be as good as, or better than, $\pi$ . That is, it must obtain greater or equal expected return from all states $s\in S$:
$$
v_{\pi'} (s) \ge v_\pi (s).
$$
Moreover, if there is strict inequality at any state in the condition, then there must be strict inequality at that state in the conclusion.

## Policy Improvement

$$
\begin{align}
\pi'(s) :=& \arg\max_a q_\pi (s, a) \\
         =& \arg\max_a \mathbb{E} [R_{t+1} + \gamma v_\pi (S_{t+1}) | S_t=s, A_t=a] \\
         =& \arg\max_a \sum_{s', r} p(s', r|s, a)[r + \gamma v_\pi (s')]
\end{align}
$$



