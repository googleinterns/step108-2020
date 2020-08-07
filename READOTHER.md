<h1>Scheduling</h1>

<h3>First formulation: Daily ([solver.py](scheduler/solver_v1.py))</h3>

<h5>Data and Variables</h5>
\begin{align*}
  \mathcal{T} &:= && \{\text{teams}\} \\
  \mathcal{N} &:= && \{\text{total days}\} \\
  W & := && \{\text{total weeks}\} \\
  W_n & := && \{\text{days in week $n$}\} \\
  L_{tu} &:=&& \text{The minimum number of times $t$ plays $u$ at home} \\
  U_{tu} &:=&& \text{The maximum number of times $t$ plays $u$ at home} \\
  x_{tu}^i &:=&&
    \begin{cases}
      1 & \text{if team $t$ plays a home game against team $u$ on day $i$}\\
      0 & \text{otherwise}
    \end{cases}       
\end{align*}

<h5>Constraints</h5>
\begin{align*}
 &(1) \hspace{3ex} \forall t \in \mathcal{T}:&& \sum_{i \in w} \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 4 \\
 &(2) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&& \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 1 \\
 &(3) \hspace{3ex} \forall u, t \in \mathcal{T} \text{ s.t. } u \neq t:&& \hspace{-6ex} L_{ut} \leq \sum_{i \in \mathcal{N}} x_{ut}^i \leq U_{ut} \\
 &(4) \hspace{3ex} \forall u \in \mathcal{T}:&& \sum_{i \in \mathcal{N}} \sum_{t \in \mathcal{T}} x_{tu}^i \leq 41 \\
 &(5) \hspace{3ex} \forall t \in \mathcal{T}:&& \sum_{i \in \mathcal{N}} \sum_{u \in \mathcal{T}} x_{tu}^i  41 \\
\end{align*}
