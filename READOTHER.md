<h1>Scheduling</h1>
We used Google's or-tools to create the models and Gurobi to solve them. Other solvers may be very slow, or may not even be able to solve the problem.

An overview of NBA scheduling can be found [here](https://www.nbastuffer.com/analytics101/how-the-nba-schedule-is-made/).

<h3>First formulation: Daily ([solver.py](scheduler/solver.py))</h3>

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
 &(1) \hspace{3ex} \forall w \in W, \; \forall t \in \mathcal{T}:&& \sum_{i \in w} \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 4 \\
 &(2) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&& \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 1 \\
 &(3) \hspace{3ex} \forall u, t \in \mathcal{T} \text{ s.t. } u \neq t:&& \hspace{-6ex} L_{ut} \leq \sum_{i \in \mathcal{N}} x_{ut}^i \leq U_{ut} \\
 &(4) \hspace{3ex} \forall u \in \mathcal{T}:&& \sum_{i \in \mathcal{N}} \sum_{t \in \mathcal{T}} x_{tu}^i \leq 41 \\
 &(5) \hspace{3ex} \forall t \in \mathcal{T}:&& \sum_{i \in \mathcal{N}} \sum_{u \in \mathcal{T}} x_{tu}^i \leq 41 \\
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

Our first approach was fairly naive—we just wanted to to see if we could solve this problem. We initially wanted to minimize travel cost, so without going through the hassle of collecting data on every team's home location, we decided to encode the cost as: any team that travels to or from an away game adds +1 to the cost. Since each team must play 41 away games, there is a fixed cost of 41 that we can ignore. Thus, minimizing the cost in this form is equivalent to minimizing the number of times each team travels from a home game to an away game and vice versa. To add "fairness," we decided to minimize the most expensive team instead of minimizing the sum of the teams' costs.

The feasibile solution took 30s to solve, but with the objective it tooks 70 hours. There is likely a bug in the encoding of the objective, as the objective value of 1 didn't match up with the number of times teams were switching between home and away.

<h3>Second formulation: Weekly</h3>
After looking at the schedule created by our first formulation, we realized that minimizing the travel cost our way resulted in very wonky schedules. Teams were, for the most part, playing the first half of their games home/away and the second half away/home. This didn't really make sense for an NBA schedule, and the runtime with the objective was too long. If we wanted to have an online solve, the runtime couldn't be more than a few minutes let alone a few days.

By simply assigning games to weeks instead of days, we could speedup the runtime considerably.

<h5>New Variables</h5>
\begin{align*}
  x_t^w  &:=&&
    \begin{cases}
      1 & \text{if team is home for week w}\\
      0 & \text{otherwise}
    \end{cases} \\
  y_t^w &:=&&
    \begin{cases}
      1 & \text{if team $t$ plays team $u$ in week $w$ when $t$ is home}\\
      0 & \text{otherwise}
    \end{cases} \\
  z_t^w &:=&& \begin{cases}
      1 & \text{if team $t$ plays 4 games in week $w$}\\
      0 & \text{otherwise}
    \end{cases} \\
\end{align*}

<h5>Feasibility Constraints</h5>
\begin{align*}
 &(1) \hspace{3ex} \forall w \in W, \; \forall t \in \mathcal{T}:&& \sum_{u \in \mathcal{T}} (x_{ut}^w + x_{tu}^w) \leq 4 \\
 &(2) \hspace{3ex} \forall t \in \mathcal{T}: && y_{tu}^w \leq x_t^w \\
 &(3) \hspace{3ex} \forall t \in \mathcal{T}: && y_{ut}^w \leq 1 - x_t^w \\
 &(4) \hspace{3ex} \forall u, t \in \mathcal{T} \text{ s.t. } u \neq t:&& \hspace{-6ex} L_{ut} \leq \sum_{w \in W} y_{ut}^w \leq U_{ut} \\
 &(5) \hspace{3ex} \forall u \in \mathcal{T}:&& \sum_{i \in \mathcal{N}} \sum_{t \in \mathcal{T}} y_{tu}^i \leq 41 \\
 &(6) \hspace{3ex} \forall t \in \mathcal{T}:&& \sum_{i \in \mathcal{N}} \sum_{u \in \mathcal{T}} y_{tu}^i \leq 41 \\
\end{align*}

<h5>Objective Constraints</h5>
\begin{align*}
 &(1) \hspace{3ex} \forall w \in W, \; \forall t \in \mathcal{T}:&& z_t^w \geq \sum_{u \in \mathcal{T}}(y_{tu}^w + y_{ut}^w ) -3 \\
 &(2) && \min \, \max_{t \in \mathcal{T}}\sum_{w \in W}z_t^w
\end{align*}

We can convert a weekly schedule into a daily schedule through edge coloring. For each week, let every team be a vertex in the graph, and create an edge between two vertices if the teams play a match against each other that week. Since home teams do not play matches against other home teams and away teams do not play matches against other away teams, we have a partition of the vertices s.t. no edge exists within a partition. [Erdős & Wilson (1977)](https://www.renyi.hu/~p_erdos/1977-20.pdf) showed that all bipartite graphs have a chromatic index equal to its maximum degree. Each team is limited to 4 games a week, so the maximum degree is 4 and the games can all be scheduled with 4 days every week. However, this schedule would again not be very realistic. If we use all 7 colors instead of minimizing the number of colors used, it turns out any algorithm that assigns colors based on their availability will always find a feasible coloring.

Proof:

Let $G = (V, E)$ be the graph for an arbitrary week. We define a color $c$ to be "adjacent" to a vertex $v$ if $v$ is incident to an edge that is colored by $c$. By way of contradiction, suppose that we are coloring an edge $e = (u ,t)$ and there are no available colors. It must be the case that there are seven distinct colors adjacent to $u$ and $t$ collectively. However, the maximum degree in $G$ is 4, so $u$ and $t$ can be incident to at most 3 other edges excluding $e$. $u$ and $t$ together can only be adjacent to 6 distinct colors. Since we are able to use seven colors, there will always be a color available. We reach a contradiction and conclude that an algorithm will always find a coloring.

The feasible solution took 84s to solve, but with the objective the runtime was only 3 hours. If we remove the constraint that each team needs to be only home or only away for a week (constraints 2-3), we can bring the runtime for the feasible solution down to 0.3s and the runtime for the objective to 3 minutes.

<h3>Symmetry & Preprocessing</h3>
One possible way to further reduce runtime would be to solve the schedule symmetrically. We solve the same problem for half of the games using only the first half of the season, then we can just mirror the first half onto the second half, changing home games to away and vice versa. Doing so would satisfy all of the original constraints as long as the $L_{tu} = U_{tu}$ for all $t, u \in \mathcal{T}$. Unfortunately, one of constraints requires each team to play 3 games against 4 of the in-conference, out-of-division teams. In that case $L_{tu} = 1$ but $U_{tu} = 2$, violating the symmetry condition.

Since MIPs are NP-Hard, cutting the search space in half should reduce the runtime considerably. Instead of simply copying the games from the first half to the second half, we could first solve a preprocessing problem where we could fix the teams which play 3 games agianst each other and which halves they play 2 games in. Passing this to the "Weekly" solver, we could solve the problem twice over half the search space and still find an optimal solution. The preprocessing was never finished, but the model would look something similar to this:

<h5>Data and Variables</h5>
\begin{align*}
  \mathcal{T} &:= && \{\text{teams}\} \\
  \mathcal{C}_t &:= && \{\text{teams in the same conference as team $t$ but in different divisions}\} \\
  x_{tu}  &:=&&
    \begin{cases}
      1 & \text{if team $t$ plays against team $u$ 3 times}\\
      0 & \text{otherwise}
    \end{cases} \\
  y_{tu}  &:=&&
    \begin{cases}
      1 & \text{if team $t$ plays 2 home games against team $u$}\\
      0 & \text{otherwise}
    \end{cases} \\
  z_{tu} & :=&&
  \begin{cases}
      1 & \text{if team $t$ plays 2 games against team $u$ in the first half}\\
      0 & \text{otherwise}
    \end{cases}
\end{align*}

<h5>Constraints</h5>
\begin{align*}
 &(1) \hspace{3ex} \forall t \in \mathcal{T}:&& \sum_{u \in \mathcal{C}_t} x_{ut} = 4 \\
 &(2) \hspace{3ex} \forall t \in \mathcal{T}:&& \sum_{u \in \mathcal{C}_t} y_{ut} = 2 \\
 &(3) \hspace{3ex} \forall t \in \mathcal{T}:&& \sum_{u \in \mathcal{C}_t} z_{ut} = 2 \\
\end{align*}
