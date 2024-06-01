---
title: Using the OpenAI API
date: 2024-06-02
---

Recently I [decided to figure out](using-a-llm-to-read-documents.md) how I can use a [large language model](https://en.wikipedia.org/wiki/Large_language_model) to read engineering and construction documents.
There is a lot for me to learn since I know nothing.
But, with the magic of the internet, I am overly confident that I can achieve something useful.

I am starting with a OpenAI cookbook on ["Question Answering Using Embeddings"](https://cookbook.openai.com/examples/question_answering_using_embeddings), this will be my first guide.

## The Goal:

Build a tool that uses the OpenAI API to analysis large amounts of text from a project and answer questions.
Preferably this tool returns not only the answer, but a list of locations within the documents where the answer can be found.

## Some potential road blocks (and things to learn)

### Hofstadter's Law

This will almost certainly follow [Hofstadter's Law](https://en.wikipedia.org/wiki/Hofstadter's_law), so I'll try to be patient.

### PDF Parsing

Parsing the pdf's systematically in order to meaningfully reference information sources will require breaking the text into chunks that are related.
Initially, I will try to do this on a document heading basis (i.e. from the table of contents).
However, reports are written by different groups so they will be formatted differently.
Even those written by the same person may have inconsistent formatting.
Executing this programmatically without thousands of special cases / exceptions might be nearly impossible in a reasonable amount of time.

### Source Referencing

Assuming I can parse the pdf's meaningfully, I'll then need to figure out a system to reference text chunks (and their locations).
I have some ideas on this, and think it will be significantly easier than parsing, but we'll see how delusional I am.

### Vector Databases

The shear mass of data might decrease the speed significantly.
To solve this, I think I will need to learn about [vector databases](https://en.wikipedia.org/wiki/Vector_database).

### Security

The information in the pdf's will likely be confidential.
Therefore, using OpenAI could be problematic since I am pretty sure whatever I feed their API they will likely hold on to.
So, I will need to find a more secure solution.
At the start, I will use publicly available work (probably mostly from US government guidance documents).
But I will eventually need to figure out how to (I think) store and use the model locally, so the information doesn't get out into the wild.
I think this will mean selecting a new model.
Since the bulk of the work will be in preparing content to use in the model (see [pdf parsing](#pdf-parsing)),
it's not critical to nail down my selection just yet.
