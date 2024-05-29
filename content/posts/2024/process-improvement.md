---
title: Process Improvement
date: 2024-05-27
---

Civil engineering and construction is notorious for being conservative: it takes us FOREVER to adopt new methods and ideas.
When the industry started using computers in the 90's, it seems not much thought was given as to who our processes should change in light of these (cheap computers) paradigm shifting tools. They just transferred their paper processes into digital ones.
Thirty years later, we work in a world where copies of our new paper (pdf's) are free.
And our typewriters (Microsoft Word) have so few constraints that it's almost impossible to guarantee consistent formatting on anything with more than ten pages.

This leads to thousands of pdf sheets produced for a simple design that has just as many engineer's hours in formatting and aesthetic quality control than engineering and technical quality control.
Not only does this distract from doing good work, it also encourages potential entrants in to the industry to avoid it.
Who wants to spend half their time formatting word documents and the other half trying to figure out where these fat-fingered numbers are from in excel?

There are several ways I think we can improve how we work, so I'll try to write a little more in the coming months on some practical implementation of those ideas.
For starters, here is a list I am thinking of:

- Use a Large Language Model to read project documents and provide responses that include document references.
    - This probably needs to be hosted on secure systems since it will typically involve private information.
    - It doesn't fix the problem of too many documents, but it might help us more effectively use the documents we do have.
- Use plain text (like [markdown](https://www.markdownguide.org/)) to write reports / memos / project documents via:
    - Services like [hedgedoc](https://hedgedoc.org/) or [hackmd](https://hackmd.io/).
    - Github/gitlab and a plain text editors.
    - For fancy presentation, we can use [ReportLab](https://docs.reportlab.com/reportlab/userguide/ch1_intro/) or something simliar.
- Use open source tools like [Viktor](https://www.viktor.ai/), [Streamlit](https://streamlit.io/), or [Solara](https://solara.dev/) to standardize and document calculations.
    - These could also be a part of an open source ecosystem that standardizes (and democratizes) the way we perform calculations.
- Produce project documents as a wikipedia-like system instead of (what is essentially) a pile of papers in the form of pdf's.
    - Documents could be rendered from markdown to html and be filled with internal links.
    - This is already being done by companies like Procore, though they still have to extract the original text from the pdf's that are part of the contract documents.

Hopefully along the way I can think of some more things to try out,