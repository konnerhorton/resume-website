---
title: Using a Large Language Model to Read Documents
date: 2024-05-27
---

In this industry we pass around a ridiculous amount of pdf's.
Last year I was given 30+ thousand pages of pdf reports and asked to summarize the geotechnical information in it.
This year, I was given 10 GB worth of reports and drawings and asked to provide some opinions on schedule, cost, and risk.
No human can reasonably read through and understand all this stuff, especially when you consider that many of them are 2+ years in the making.
But, in the fall of 2022, us laypeople were introduced to [ChatGPT](https://openai.com/index/chatgpt/).

Reading and summarizing gigabytes of text seems like an excellent task for a machine.
That way, the human can be left to do the more human task of making informed decisions.
But, like most things that appear to be magical, there are complications. Among other things, large language models can't be fed an infinite amount of data, and training on large, new datasets takes time and can be expensive.

And, for my specific use case of reading contract documents, I need to be able to reference where the "answer" came from within the documents.
If I can't verify the answer is not a hallucination, I am back to square one: look through every piece of text myself.

There is an [OpenAI cookbook](https://cookbook.openai.com/examples/question_answering_using_embeddings) on using "embeddings" to answer questions through the [OpenAI API](https://openai.com/api/).
It seems like this would be a good place to start, though I can see sizable pitfalls already.
As I work through it, I'll try to document what I learn here.