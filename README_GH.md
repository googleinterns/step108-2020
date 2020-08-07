<h1>Scheduling</h1>
We used Google's or-tools to create the models and Gurobi to solve them. Other solvers may be very slow, or may not even be able to solve the problem.

An overview of NBA scheduling can be found [here](https://www.nbastuffer.com/analytics101/how-the-nba-schedule-is-made/).

<h3>First formulation: Daily ([solver.py](scheduler/solver.py))</h3>

<h5>Data and Variables</h5>
<p align="center"><img alt="\begin{align*}&#10;  \mathcal{T} &amp;:= &amp;&amp; \{\text{teams}\} \\&#10;  \mathcal{N} &amp;:= &amp;&amp; \{\text{total days}\} \\&#10;  W &amp; := &amp;&amp; \{\text{total weeks}\} \\&#10;  W_n &amp; := &amp;&amp; \{\text{days in week $n$}\} \\&#10;  L_{tu} &amp;:=&amp;&amp; \text{minimum number of times $t$ plays $u$ at home} \\&#10;  U_{tu} &amp;:=&amp;&amp; \text{maximum number of times $t$ plays $u$ at home} \\&#10;  x_{tu}^i  &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team $t$ plays a home game against team $u$ on day $i$}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;    y_t^i &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team $t$ is home on day $i$}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;    z_t^i &amp;:=&amp;&amp; \text{cost paid by team $t$ on day $i$} \\&#10;    v &amp;:=&amp;&amp; \text{max cost paid by any team}&#10;\end{align*}" src="svgs/739d01759e7f84a758eb6565a6723fb6.svg" align="middle" width="545.9145285pt" height="302.14670474999997pt"/></p>

<h5>Feasibility Constraints</h5>
<p align="center"><img alt="\begin{align*}&#10; &amp;(1) \hspace{3ex} \forall t \in \mathcal{T}:&amp;&amp; \sum_{i \in w} \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 4 \\&#10; &amp;(2) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&amp;&amp; \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 1 \\&#10; &amp;(3) \hspace{3ex} \forall u, t \in \mathcal{T} \text{ s.t. } u \neq t:&amp;&amp; \hspace{-6ex} L_{ut} \leq \sum_{i \in \mathcal{N}} x_{ut}^i \leq U_{ut} \\&#10; &amp;(4) \hspace{3ex} \forall u \in \mathcal{T}:&amp;&amp; \sum_{i \in \mathcal{N}} \sum_{t \in \mathcal{T}} x_{tu}^i \leq 41 \\&#10; &amp;(5) \hspace{3ex} \forall t \in \mathcal{T}:&amp;&amp; \sum_{i \in \mathcal{N}} \sum_{u \in \mathcal{T}} x_{tu}^i  41 \\&#10;\end{align*}" src="svgs/85d91e1539e810ecd226cd09ae11bdab.svg" align="middle" width="469.22092635pt" height="221.7521592pt"/></p>

<h5>Objective Constraints</h5>
<p align="center"><img alt="\begin{align*}&#10; &amp;(1) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&amp;&amp; y_t^i \geq \sum_{u \in \mathcal{T}}x_{tu}^i \\&#10; &amp;(2) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&amp;&amp; y_t^i \leq 1 - \sum_{u \in \mathcal{T}}x_{ut}^i \\&#10; &amp;(3) \hspace{3ex} \forall i \in \mathcal{N}, \; i \neq 0, \; \forall t \in \mathcal{T}:&amp;&amp;  z_t^i \geq 0 \\&#10; &amp;(4) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&amp;&amp;  z_t^i \geq y_t^i - y_t^{i-1} \\&#10; &amp;(5) \hspace{3ex} \forall t \in \mathcal{T}:&amp;&amp;  v \geq \sum_{i \in \mathcal{N}}z_t^i \\&#10; &amp;(6) &amp;&amp; \min v&#10;\end{align*}" src="svgs/77925fc9e8f9d198adb5ec881a1a82f6.svg" align="middle" width="450.70818705pt" height="209.93445494999997pt"/></p>

Our first approach was fairly naive—we just wanted to to see if we could solve this problem. We initially wanted to minimize travel cost, so without going through the hassle of collecting data on every team's home location, we decided to encode the cost as: any team that travels to or from an away game adds +1 to the cost. Since each team must play 41 away games, there is a fixed cost of 41 that we can ignore. Thus, minimizing the cost in this form is equivalent to minimizing the number of times each team travels from a home game to an away game and vice versa. To add "fairness," we decided to minimize the most expensive team instead of minimizing the sum of the teams' costs.

The feasibile solution took 30s to solve, but with the objective it tooks 70 hours. There is likely a bug in the encoding of the objective, as the objective value of 1 didn't match up with the number of times teams were switching between home and away.

<h3>Second formulation: Weekly</h3>
After looking at the schedule created by our first formulation, we realized that minimizing the travel cost our way resulted in very wonky schedules. Teams were, for the most part, playing the first half of their games home/away and the second half away/home. This didn't really make sense for an NBA schedule, and the runtime with the objective was too long. If we wanted to have an online solve, the runtime couldn't be more than a few minutes let alone a few days.

By simply assigning games to weeks instead of days, we could speedup the runtime considerably.

<h5>New Variables</h5>
<p align="center"><img alt="\begin{align*}&#10;  x_t^w  &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team is home for week w}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;  y_t^w &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team $t$ plays team $u$ in week $w$ when $t$ is home}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;  z_t^w &amp;:=&amp;&amp; \begin{cases}&#10;      1 &amp; \text{if team $t$ plays 4 games in week $w$}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;\end{align*}" src="svgs/aba7bc24fc2144be254bebec93c36acc.svg" align="middle" width="522.45703455pt" height="161.09734575pt"/></p>

<h5>Constraints</h5>