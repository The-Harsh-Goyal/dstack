---
title: md or html? That's a dumb question
gap: 0.5
---

## opening
A couple of days ago, [[cue:thariq]]Thariq from the Claude Code team published a viral post.
The title was a single sentence: HTML is the new markdown.
He said he barely writes md files anymore and has AI generate HTML for him instead.
5 million views, and X immediately erupted into an argument.
One side is the md camp, [[cue:two-camps]]who think md is the source code of the AI era.
The other side thinks Thariq is right and HTML is the ultimate answer.

## md-side
The md camp's evidence is actually pretty solid.
Look at AGENTS.md, which OpenAI released last year: [[cue:agents-md]]over 60,000 projects use it, and AWS, Anthropic, Google, Microsoft and OpenAI, half of the AI world, donated it together to the Linux Foundation as an open standard.
Karpathy's llm-wiki is basically three layers of markdown, and a single CLAUDE.md file got 50,000 stars.
Cloudflare measured it: [[cue:token-saving]]the same blog post is sixteen thousand tokens as HTML and only three thousand once converted to md.
An 80% saving.
GitHub has also said it officially: documentation no longer describes code, [[cue:doc-is-code]]documentation is code.

## html-side
But the html camp isn't wrong either.
I agree with several of the arguments in Thariq's post.
First, spatial information. [[cue:spatial]]Diffs, call graphs and architecture diagrams have a spatial dimension to begin with. md squashes them into a line of text, while html can lay them out side by side, and the difference in comprehension is an order of magnitude.
Second, dynamic experience. [[cue:dynamic]]When you're building a product prototype, what color a button turns when pressed, what easing curve it uses, no amount of written description helps. html lets you see it directly.
Third, structured reading. [[cue:structured]]Collapsible sections, tabbed code blocks and a sidebar glossary are a different thing from the same words piled up in a line.
With Anthropic's Live Artifacts today, HTML has gone from a static artifact to a dashboard you can interact with that pulls live data.

## the-real-question
After reading all this, what I want to say is, [[cue:reveal]]both sides are fighting over a dumb question.
Both sides won.
But they won different questions.
The md camp is answering, [[cue:question-md]]what do we write in.
The html camp is answering, [[cue:question-html]]what do we show people.
These are two questions.
How could one replace the other?

## the-split
I think this is the real question.
md and html aren't substitutes for each other; [[cue:split]]they divide the work.
Before, you wrote md and read md yourself.
Back then you had to compromise, so md won.
But once AI arrived, [[cue:ai-changes]]there was a new situation for the first time.
The cost of production can be absorbed by AI.
The heavy cost of the HTML part, AI carries for you.
You're only responsible for consuming it.
A need that used to require a compromise got split into an extreme optimum at each end.
The production end needs to be light, fast and token efficient, [[cue:md-side-win]]and that's md.
The consumption end needs to be rich, visual and easy to share, [[cue:html-side-win]]and that's html.
Each end reaches its own peak.
Nobody needs the compromise position in the middle anymore.

## activity-proof
The cleanest living example is Thariq himself.
In March he published a Skills guide, [[cue:thariq-march]]stressing that the core is still markdown.
In May he published HTML is the new markdown.
The same person, [[cue:same-person]]each end reaching its own peak, with no conflict between them.
The Karpathy and Lex Fridman pairing is the same.
The core is a markdown wiki, [[cue:karpathy-lex]]and the shell is dynamic HTML.
It's not that Lex replaced Karpathy; he added a consumption layer on top of Karpathy's foundation.

## closing
So next time you want to argue about this, [[cue:final]]first ask yourself one thing.
Are you facing "writing" right now, or "reading"?
Writing, [[cue:md-final]]use md.
Reading, [[cue:html-final]]use html.
The tools handle the switch for you.
You can put down your side in the argument.
