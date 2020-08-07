# [ball.ai]([https://bj-de-jw-step-2020.uc.r.appspot.com/](https://bj-de-jw-step-2020.uc.r.appspot.com/))

Hello! You may be wondering, what is [ball.ai]([https://bj-de-jw-step-2020.uc.r.appspot.com/](https://bj-de-jw-step-2020.uc.r.appspot.com/))? In terms of what it actually is, it's the world's first fantasy basketball engine, a unified solution for any time you've asked yourself a question about an impossible basketball scenario. If you've ever wondered just how overpowered the 2018 Warriors would have been if they had LeBron James on their team, or what would have happened if Michael Jordan had joined the Nets instead of the Wizards in 2002, ball.ai is the place for you. 

In terms of why we (developers Diego Escobedo, Brandon Jones, and Jeremy Weiss) did it, the answer is that it is the capstone for our Google STEP internship. Typically, STEP interns would work on the same area as their host, aiming to develop a feature that would become part of the product. Unfortunately, due to the fact that COVID-19 forced the internship online, this meant that giving interns access to Google's codebase was no longer feasible from a securitry perspective. So, as STEP interns, we were tasked with making an entire website from scratch. For those of us who hadn't done webdev before, this was obviously challenging, but it was a great learning experience, and we hope you enjoy it! Below is a quick summary of everyone's feature, and then within each folder you can find more details about everyone's work.


## Build
> Brandon Jones

## Schedule
> Jeremy Weiss

We used Google's or-tools to create the models and Gurobi to solve them. Other solvers may be very slow, or may not even be able to solve the problem.

An overview of NBA scheduling can be found [here](https://www.nbastuffer.com/analytics101/how-the-nba-schedule-is-made/).

<h3>First formulation: Daily ([solver.py](scheduler/solver.py))</h3>

<h5>Data and Variables</h5>
<p align="center"><img alt="\begin{align*}&#10;  \mathcal{T} &amp;:= &amp;&amp; \{\text{teams}\} \\&#10;  \mathcal{N} &amp;:= &amp;&amp; \{\text{total days}\} \\&#10;  W &amp; := &amp;&amp; \{\text{total weeks}\} \\&#10;  W_n &amp; := &amp;&amp; \{\text{days in week $n$}\} \\&#10;  L_{tu} &amp;:=&amp;&amp; \text{minimum number of times $t$ plays $u$ at home} \\&#10;  U_{tu} &amp;:=&amp;&amp; \text{maximum number of times $t$ plays $u$ at home} \\&#10;  x_{tu}^i  &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team $t$ plays a home game against team $u$ on day $i$}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;    y_t^i &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team $t$ is home on day $i$}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;    z_t^i &amp;:=&amp;&amp; \text{cost paid by team $t$ on day $i$} \\&#10;    v &amp;:=&amp;&amp; \text{max cost paid by any team}&#10;\end{align*}" src="svgs/739d01759e7f84a758eb6565a6723fb6.svg" align="middle" width="545.9145285pt" height="302.14670474999997pt"/></p>

<h5>Feasibility Constraints</h5>
<p align="center"><img alt="\begin{align*}&#10; &amp;(1) \hspace{3ex} \forall w \in W, \; \forall t \in \mathcal{T}:&amp;&amp; \sum_{i \in w} \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 4 \\&#10; &amp;(2) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&amp;&amp; \sum_{u \in \mathcal{T}} (x_{ut}^i + x_{tu}^i) \leq 1 \\&#10; &amp;(3) \hspace{3ex} \forall u, t \in \mathcal{T} \text{ s.t. } u \neq t:&amp;&amp; \hspace{-6ex} L_{ut} \leq \sum_{i \in \mathcal{N}} x_{ut}^i \leq U_{ut} \\&#10; &amp;(4) \hspace{3ex} \forall u \in \mathcal{T}:&amp;&amp; \sum_{i \in \mathcal{N}} \sum_{t \in \mathcal{T}} x_{tu}^i \leq 41 \\&#10; &amp;(5) \hspace{3ex} \forall t \in \mathcal{T}:&amp;&amp; \sum_{i \in \mathcal{N}} \sum_{u \in \mathcal{T}} x_{tu}^i \leq 41 \\&#10;\end{align*}" src="svgs/48a677d7db38568112b6361764496d70.svg" align="middle" width="469.22092635pt" height="221.7521592pt"/></p>

<h5>Objective Constraints</h5>
<p align="center"><img alt="\begin{align*}&#10; &amp;(1) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&amp;&amp; y_t^i \geq \sum_{u \in \mathcal{T}}x_{tu}^i \\&#10; &amp;(2) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&amp;&amp; y_t^i \leq 1 - \sum_{u \in \mathcal{T}}x_{ut}^i \\&#10; &amp;(3) \hspace{3ex} \forall i \in \mathcal{N}, \; i \neq 0, \; \forall t \in \mathcal{T}:&amp;&amp;  z_t^i \geq 0 \\&#10; &amp;(4) \hspace{3ex} \forall i \in \mathcal{N}, \; \forall t \in \mathcal{T}:&amp;&amp;  z_t^i \geq y_t^i - y_t^{i-1} \\&#10; &amp;(5) \hspace{3ex} \forall t \in \mathcal{T}:&amp;&amp;  v \geq \sum_{i \in \mathcal{N}}z_t^i \\&#10; &amp;(6) &amp;&amp; \min v&#10;\end{align*}" src="svgs/77925fc9e8f9d198adb5ec881a1a82f6.svg" align="middle" width="450.70818705pt" height="209.93445494999997pt"/></p>

Our first approach was fairly naive—we just wanted to to see if we could solve this problem. We initially wanted to minimize travel cost, so without going through the hassle of collecting data on every team's home location, we decided to encode the cost as: any team that travels to or from an away game adds +1 to the cost. Since each team must play 41 away games, there is a fixed cost of 41 that we can ignore. Thus, minimizing the cost in this form is equivalent to minimizing the number of times each team travels from a home game to an away game and vice versa. To add "fairness," we decided to minimize the most expensive team instead of minimizing the sum of the teams' costs.

The feasibile solution took 30s to solve, but with the objective it tooks 70 hours. There is likely a bug in the encoding of the objective, as the objective value of 1 didn't match up with the number of times teams were switching between home and away.

<h3>Second formulation: Weekly ([solver_v2.py](scheduler/solver_v2.py))</h3>
After looking at the schedule created by our first formulation, we realized that minimizing the travel cost our way resulted in very wonky schedules. Teams were, for the most part, playing the first half of their games home/away and the second half away/home. This didn't really make sense for an NBA schedule, and the runtime with the objective was too long. If we wanted to have an online solve, the runtime couldn't be more than a few minutes let alone a few days.

By simply assigning games to weeks instead of days, we could speedup the runtime considerably.

<h5>New Variables</h5>
<p align="center"><img alt="\begin{align*}&#10;  x_t^w  &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team is home for week w}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;  y_t^w &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team $t$ plays team $u$ in week $w$ when $t$ is home}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;  z_t^w &amp;:=&amp;&amp; \begin{cases}&#10;      1 &amp; \text{if team $t$ plays 4 games in week $w$}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;\end{align*}" src="svgs/aba7bc24fc2144be254bebec93c36acc.svg" align="middle" width="522.45703455pt" height="161.09734575pt"/></p>

<h5>Feasibility Constraints</h5>
<p align="center"><img alt="\begin{align*}&#10; &amp;(1) \hspace{3ex} \forall w \in W, \; \forall t \in \mathcal{T}:&amp;&amp; \sum_{u \in \mathcal{T}} (x_{ut}^w + x_{tu}^w) \leq 4 \\&#10; &amp;(2) \hspace{3ex} \forall t \in \mathcal{T}: &amp;&amp; y_{tu}^w \leq x_t^w \\&#10; &amp;(3) \hspace{3ex} \forall t \in \mathcal{T}: &amp;&amp; y_{ut}^w \leq 1 - x_t^w \\&#10; &amp;(4) \hspace{3ex} \forall u, t \in \mathcal{T} \text{ s.t. } u \neq t:&amp;&amp; \hspace{-6ex} L_{ut} \leq \sum_{w \in W} y_{ut}^w \leq U_{ut} \\&#10; &amp;(5) \hspace{3ex} \forall u \in \mathcal{T}:&amp;&amp; \sum_{i \in \mathcal{N}} \sum_{t \in \mathcal{T}} y_{tu}^i \leq 41 \\&#10; &amp;(6) \hspace{3ex} \forall t \in \mathcal{T}:&amp;&amp; \sum_{i \in \mathcal{N}} \sum_{u \in \mathcal{T}} y_{tu}^i \leq 41 \\&#10;\end{align*}" src="svgs/a88548a4330594f526aad0f232920a82.svg" align="middle" width="451.56494295pt" height="226.71679964999998pt"/></p>

<h5>Objective Constraints</h5>
<p align="center"><img alt="\begin{align*}&#10; &amp;(1) \hspace{3ex} \forall w \in W, \; \forall t \in \mathcal{T}:&amp;&amp; z_t^w \geq \sum_{u \in \mathcal{T}}(y_{tu}^w + y_{ut}^w ) -3 \\&#10; &amp;(2) &amp;&amp; \min \, \max_{t \in \mathcal{T}}\sum_{w \in W}z_t^w&#10;\end{align*}" src="svgs/4ba78d8d58d8ce4c569e87b8d55d6331.svg" align="middle" width="460.4245635pt" height="83.7693714pt"/></p>

We can convert a weekly schedule into a daily schedule through edge coloring. For each week, let every team be a vertex in the graph, and create an edge between two vertices if the teams play a match against each other that week. Since home teams do not play matches against other home teams and away teams do not play matches against other away teams, we have a partition of the vertices s.t. no edge exists within a partition. [Erdős & Wilson (1977)](https://www.renyi.hu/~p_erdos/1977-20.pdf) showed that all bipartite graphs have a chromatic index equal to its maximum degree. Each team is limited to 4 games a week, so the maximum degree is 4 and the games can all be scheduled with 4 days every week. However, this schedule would again not be very realistic. If we use all 7 colors instead of minimizing the number of colors used, it turns out any algorithm that assigns colors based on their availability will always find a feasible coloring.

Proof:

Let <img alt="$G = (V, E)$" src="svgs/0e144c0667d70604b5028e656cc22ebf.svg" align="middle" width="78.51806489999998pt" height="24.65753399999998pt"/> be the graph for an arbitrary week. We define a color <img alt="$c$" src="svgs/3e18a4a28fdee1744e5e3f79d13b9ff6.svg" align="middle" width="7.11380504999999pt" height="14.15524440000002pt"/> to be "adjacent" to a vertex <img alt="$v$" src="svgs/6c4adbc36120d62b98deef2a20d5d303.svg" align="middle" width="8.55786029999999pt" height="14.15524440000002pt"/> if <img alt="$v$" src="svgs/6c4adbc36120d62b98deef2a20d5d303.svg" align="middle" width="8.55786029999999pt" height="14.15524440000002pt"/> is incident to an edge that is colored by <img alt="$c$" src="svgs/3e18a4a28fdee1744e5e3f79d13b9ff6.svg" align="middle" width="7.11380504999999pt" height="14.15524440000002pt"/>. By way of contradiction, suppose that we are coloring an edge <img alt="$e = (u ,t)$" src="svgs/065f8bb23a2812f1427de2195f2b0090.svg" align="middle" width="65.00945549999999pt" height="24.65753399999998pt"/> and there are no available colors. It must be the case that there are seven distinct colors adjacent to <img alt="$u$" src="svgs/6dbb78540bd76da3f1625782d42d6d16.svg" align="middle" width="9.41027339999999pt" height="14.15524440000002pt"/> and <img alt="$t$" src="svgs/4f4f4e395762a3af4575de74c019ebb5.svg" align="middle" width="5.936097749999991pt" height="20.221802699999984pt"/> collectively. However, the maximum degree in <img alt="$G$" src="svgs/5201385589993766eea584cd3aa6fa13.svg" align="middle" width="12.92464304999999pt" height="22.465723500000017pt"/> is 4, so <img alt="$u$" src="svgs/6dbb78540bd76da3f1625782d42d6d16.svg" align="middle" width="9.41027339999999pt" height="14.15524440000002pt"/> and <img alt="$t$" src="svgs/4f4f4e395762a3af4575de74c019ebb5.svg" align="middle" width="5.936097749999991pt" height="20.221802699999984pt"/> can be incident to at most 3 other edges excluding <img alt="$e$" src="svgs/8cd34385ed61aca950a6b06d09fb50ac.svg" align="middle" width="7.654137149999991pt" height="14.15524440000002pt"/>. <img alt="$u$" src="svgs/6dbb78540bd76da3f1625782d42d6d16.svg" align="middle" width="9.41027339999999pt" height="14.15524440000002pt"/> and <img alt="$t$" src="svgs/4f4f4e395762a3af4575de74c019ebb5.svg" align="middle" width="5.936097749999991pt" height="20.221802699999984pt"/> together can only be adjacent to 6 distinct colors. Since we are able to use seven colors, there will always be a color available. We reach a contradiction and conclude that an algorithm will always find a coloring.

The feasible solution took 84s to solve, but with the objective the runtime was only 3 hours. If we remove the constraint that each team needs to be only home or only away for a week (constraints 2-3), we can bring the runtime for the feasible solution down to 0.3s and the runtime for the objective to 3 minutes.

<h3>Symmetry & Preprocessing</h3>
One possible way to further reduce runtime would be to solve the schedule symmetrically. We solve the same problem for half of the games using only the first half of the season, then we can just mirror the first half onto the second half, changing home games to away and vice versa. Doing so would satisfy all of the original constraints as long as
<p align="center"><img alt="$$\forall t, u \in \mathcal{T}:\; L_{tu} = U_{tu}$$" src="svgs/8768b81c938d494f09abc784d5bb83db.svg" align="middle" width="153.89790075pt" height="14.611878599999999pt"/></p>
Unfortunately, one of constraints requires each team to play 3 games against 4 of the in-conference, out-of-division teams. In that case
<p align="center"><img alt="$$L_{tu} = 1 \neq 2 = U_{tu}$$" src="svgs/323c96bb18423b1d7df67832f76b9f4c.svg" align="middle" width="130.90007204999998pt" height="14.61184725pt"/></p>
violating the symmetry condition.<br/>
<br/>
Since MIPs are NP-Hard, cutting the search space in half should reduce the runtime considerably. Instead of simply copying the games from the first half to the second half, we could first solve a preprocessing problem where we could fix the teams which play 3 games agianst each other and which halves they play 2 games in. Passing this to the "Weekly" solver, we could solve the problem twice over half the search space and still find an optimal solution. The preprocessing was never finished, but the model would look something similar to this:

<h5>Data and Variables</h5>
<p align="center"><img alt="\begin{align*}&#10;  \mathcal{T} &amp;:= &amp;&amp; \{\text{teams}\} \\&#10;  \mathcal{C}_t &amp;:= &amp;&amp; \{\text{teams in the same conference as team $t$ but in different divisions}\} \\&#10;  x_{tu}  &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team $t$ plays against team $u$ 3 times}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;  y_{tu}  &amp;:=&amp;&amp;&#10;    \begin{cases}&#10;      1 &amp; \text{if team $t$ plays 2 home games against team $u$}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases} \\&#10;  z_{tu} &amp; :=&amp;&amp;&#10;  \begin{cases}&#10;      1 &amp; \text{if team $t$ plays 2 games against team $u$ in the first half}\\&#10;      0 &amp; \text{otherwise}&#10;    \end{cases}&#10;\end{align*}" src="svgs/0814c0585fcc15a58c04b6edb31b6a4d.svg" align="middle" width="584.25346815pt" height="210.5768379pt"/></p>

<h5>Constraints</h5>
<p align="center"><img alt="\begin{align*}&#10; &amp;(1) \hspace{3ex} \forall t \in \mathcal{T}:&amp;&amp; \sum_{u \in \mathcal{C}_t} x_{ut} = 4 \\&#10; &amp;(2) \hspace{3ex} \forall t \in \mathcal{T}:&amp;&amp; \sum_{u \in \mathcal{C}_t} y_{ut} = 2 \\&#10; &amp;(3) \hspace{3ex} \forall t \in \mathcal{T}:&amp;&amp; \sum_{u \in \mathcal{C}_t} z_{ut} = 2 \\&#10;\end{align*}" src="svgs/642ba298127b1742d2b72ec9a8d095f6.svg" align="middle" width="358.39352175pt" height="132.0828003pt"/></p>

<h3>Visualization</h3>
All of the visualizations and animations were created with D3, based off of this [tutorial](https://blog.risingstack.com/tutorial-d3-js-calendar-heatmap/). You can see the source [here](ball.ai/src/main/webapp/schedule.js).

## Simulate
> Diego Escobedo

The code used to research the simulation model can be found in the `h2h` folder, and the deployed model is within the `ball.ai` folder.

The purpose of this feature was to be able to predict the outcome of any game, without having to rely on team statistics. Since the point of the website is to be able to create a team from any player from any era, then to predict the outcome of the game, then we couldn't use any stats related to W/L record, head-to-head matchups, or player rotations. Additionally, we had to make sure that our representation of the game was reasonable and accurate, since the only training data we have is based on real games. 

We ended up settling on a [Deep Neural Network](https://towardsdatascience.com/a-laymans-guide-to-deep-neural-networks-ddcea24847fb) for our problem, using around 40 statistical categories with which to represent each player. Additionally, we augmented the model with 'player embeddings', which is just like [word embeddings](https://towardsdatascience.com/what-the-heck-is-word-embedding-b30f67f01c81) but using the player identities. 

More details on the iterative process that led to this model, including data collection, domain research, and the different models we used, can be located in the README of the `h2h` folder. 

