# Revising an Architecture I Designed

Author: [Vadim Vladymtsev](https://vadimohka.com/about.html)
Published: 2026-11-02
Updated: 2026-11-03
Canonical: https://vadimohka.com/essays/revising-my-architecture/

Taking responsibility for an engineering decision includes being willing to revise it when it gets in the way of the work. That is easy to accept when discussing someone else's architecture. With your own, you also have to deal with the desire to remain right.

Early in my work with microservices, I built an application in which each service had its own database. Over time, that arrangement began to create problems. I consolidated some of the databases and reworked the application. The transition required many migrations. I had chosen the architecture, so I considered correcting it part of my responsibility.

Microservices divide an application into services with separate responsibilities. Giving a service its own database can support its independence. A sound principle, however, does not establish whether a particular system benefits from the way it has been applied. In my case, the separation needed to change. That gives me a specific decision to examine; it does not settle the wider argument about microservices.

An architecture you designed has a layer of protection that never appears in the technical documentation. You have invested time in it and grown used to how it works. You may have explained to other people why the design makes sense. Revising it can feel like admitting that you were not competent enough to make the original choice. It becomes tempting to find one more reason to defend it.

Those reasons are usually available. Somewhere, a similar architecture works well. There are convincing articles explaining its advantages. Another workaround might let you preserve the original structure. But none of that tells you whether the design is helping the application you actually have to maintain.

I bring the discussion back to the work the system needs to support. What has become difficult, and what is causing that difficulty? Is removing the limitation worth the cost of the transition? These questions make the consequences of a decision available for discussion. The answers can be uncomfortable for its author. They also provide a basis for deciding what to do next.

Acknowledging the problem still leaves the migration to carry out. The transition needs planning, and the data needs to survive it. The people who will maintain the application need to understand what changed. A thoughtful statement about lessons learned will not do any of that work. The cost of the original choice becomes visible in the effort required to correct it.

Taking responsibility can also mean asking someone with deeper expertise to help. My job then is to give them an honest account of the context and allow them to change what I built. Protecting my authorship from useful changes would be an odd way to look after the system.

Revision needs justification too. If every doubt triggers a rewrite, the product can spend a long time under repair. Some inconveniences are reasonable to live with for now. Other constraints already prevent necessary work. Distinguishing between them requires attention to the task and the cost of changing direction. The desire for a cleaner design is not enough on its own.

I want professional trust to be able to withstand this conversation. An engineer should be able to explain the original choice, describe its consequences, and propose a correction. There is no need to recast every turn as part of a plan that existed from the beginning. We can take responsibility for what we understand now.

The database experience left me with a practical standard: when a decision stops helping the system, I need to help the system move beyond it. That includes decisions I made myself.
