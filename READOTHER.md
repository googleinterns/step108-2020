<h1>Scheduling</h1>
We used Google's or-tools to create the models and Gurobi to solve them. Other solvers may be very slow, or may not even be able to solve the problem.
An overview of NBA scheduling can be found [here](https://www.nbastuffer.com/analytics101/how-the-nba-schedule-is-made/).

<h3>First formulation: Daily ([solver.py](https://github.com/googleinterns/step108-2020/blob/svgs/scheduler/solver.py))</h3>


<h5>Data and Variables</h5>
\begin{align*}
  \mathcal{T} &:= && \{\text{teams}\} \\
  \mathcal{N} &:= && \{\text{total days}\} \\
  W & := && \{\text{total weeks}\} \\
  W_n & := && \{\text{days in week $n$}\} \\
  L_{tu} &:=&& \text{minimum number of times $t$ plays $u$ at home} \\
  U_{tu} &:=&& \text{maximum number of times $t$ plays $u$ at home} \\
  x_{tu}^i  &:=&&
    \begin{cases}
      1 & \text{if team $t$ plays a home game against team $u$ on day $i$}\\
      0 & \text{otherwise}
    \end{cases} \\
    y_t^i &:=&&
    \begin{cases}
      1 & \text{if team $t$ is home on day $i$}\\
      0 & \text{otherwise}
    \end{cases} \\
    z_t^i &:=&& \text{cost paid by team $t$ on day $i$} \\
    v &:=&& \text{max cost paid by any team}
\end{align*}

<h5>Feasibility Constraints</h5>
\begin{align*}
 &(1) \hspace{3ex} \forall t \in \mathcal{T}:&& \sum_{i \in w} \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 4 \\
 &(2) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&& \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 1 \\
 &(3) \hspace{3ex} \forall u, t \in \mathcal{T} \text{ s.t. } u \neq t:&& \hspace{-6ex} L_{ut} \leq \sum_{i \in \mathcal{N}} x_{ut}^i \leq U_{ut} \\
 &(4) \hspace{3ex} \forall u \in \mathcal{T}:&& \sum_{i \in \mathcal{N}} \sum_{t \in \mathcal{T}} x_{tu}^i \leq 41 \\
 &(5) \hspace{3ex} \forall t \in \mathcal{T}:&& \sum_{i \in \mathcal{N}} \sum_{u \in \mathcal{T}} x_{tu}^i  41 \\
\end{align*}

<h5>Objective Constraints</h5>
\begin{align*}
 &(1) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&& y_t^i \geq \sum_{u \in \mathcal{T}}x_{tu}^i \\
 &(2) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&& y_t^i \leq 1 - \sum_{u \in \mathcal{T}}x_{ut}^i \\
 &(3) \hspace{3ex} \forall i \in \mathcal{N}, \; i \neq 0, \; \forall t \in \mathcal{T}:&&  z_t^i \geq 0 \\
 &(4) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&&  z_t^i \geq y_t^i - y_t^{i-1} \\
 &(5) \hspace{3ex} \forall t \in \mathcal{T}:&&  v \geq \sum_{i \in \mathcal{N}}z_t^i \\
 &(6) && \min v
\end{align*}
