# [ball.ai]([https://bj-de-jw-step-2020.uc.r.appspot.com/](https://bj-de-jw-step-2020.uc.r.appspot.com/))

Hello! You may be wondering, what is [ball.ai]([https://bj-de-jw-step-2020.uc.r.appspot.com/](https://bj-de-jw-step-2020.uc.r.appspot.com/))? In terms of what it actually is, it's the world's first fantasy basketball engine, a unified solution for any time you've asked yourself a question about an impossible basketball scenario. If you've ever wondered just how overpowered the 2018 Warriors would have been if they had LeBron James on their team, or what would have happened if Michael Jordan had joined the Nets instead of the Wizards in 2002, ball.ai is the place for you. 

In terms of why we (developers Diego Escobedo, Brandon Jones, and Jeremy Weiss) did it, the answer is that it is the capstone for our Google STEP internship. Typically, STEP interns would work on the same area as their host, aiming to develop a feature that would become part of the product. Unfortunately, due to the fact that COVID-19 forced the internship online, this meant that giving interns access to Google's codebase was no longer feasible from a securitry perspective. So, as STEP interns, we were tasked with making an entire website from scratch. For those of us who hadn't done webdev before, this was obviously challenging, but it was a great learning experience, and we hope you enjoy it! Below is a quick summary of everyone's feature, and then within each folder you can find more details about everyone's work.


## Build
> Brandon Jones

## Schedule
> Jeremy Weiss

## Simulate
> Diego Escobedo

The code used to research the simulation model can be found in the `h2h` folder, and the deployed model is within the `ball.ai` folder.

The purpose of this feature was to be able to predict the outcome of any game, without having to rely on team statistics. Since the point of the website is to be able to create a team from any player from any era, then to predict the outcome of the game, then we couldn't use any stats related to W/L record, head-to-head matchups, or player rotations. Additionally, we had to make sure that our representation of the game was reasonable and accurate, since the only training data we have is based on real games. 

We ended up settling on a [Deep Neural Network](https://towardsdatascience.com/a-laymans-guide-to-deep-neural-networks-ddcea24847fb) for our problem, using around 40 statistical categories with which to represent each player. Additionally, we augmented the model with 'player embeddings', which is just like [word embeddings](https://towardsdatascience.com/what-the-heck-is-word-embedding-b30f67f01c81) but using the player identities. 

More details on the iterative process that led to this model, including data collection, domain research, and the different models we used, can be located in the README of the `h2h` folder. 

