# Stakeholder Feedback
## Phase 5 — Half-term family gathering (October)

### When and how

Half-term break, showed the project to Lefteris and Yiannis at a family gathering. We were at my uncle's house and I had my laptop. Had to wait until after dinner because my mum said no laptops at the table (fair enough). Ran them through the terminal output showing predicted digits vs actual labels.

### What they could see

At this point it's all terminal-based. You type a command and it loads an image from the test set, runs the model, and prints what digit it thinks it is. No GUI, no web interface, just text output.

### What they said

**Lefteris:** First thing he asked was "wait so is this like AI? Like ChatGPT?" and I had to explain that it's machine learning but not the same thing as a chatbot — this just looks at images of numbers. I don't think he fully got the difference but he nodded along.

Then: "OK so you just type a number and it guesses what digit it is? That's cool but like... it's from a dataset right? What if I wanted to try my own handwriting? Could I take a photo of a number I wrote and test it?"

He also asked what an epoch was and I tried to explain it but I don't think I did a great job. He's planning to do something similar for his project next year so he was actually curious, not just being polite.

He then said "could you make this work on a phone? Like an app where you point the camera at a number and it tells you what it is?" I said maybe but that would be a completely different project — you'd need a mobile app framework and a camera API and stuff. The phone thing is way beyond what I'm doing but it was a fun idea.

**Yiannis:** "In Java we'd build a GUI for something like this. Does Python have anything like that? A window where you can upload an image and click a button?"

He said the terminal output is fine for testing but if this is supposed to be an actual application someone uses, it needs a proper interface. Fair point.

He also asked when the project is due and whether the code or the write-up matters more for the grade. I said it's all weighted together - analysis, design, implementation, testing, evaluation. He said "that sounds like a lot of writing" which... yeah.

He also mentioned "you should add some kind of logging — like save what the model predicted and whether it was right. Then you can track the accuracy over time." I nodded but honestly I didn't really know what he meant by logging at this point. Looking back I think he meant something like a log file or audit trail.

### My thoughts

They're both right about the interface. The terminal thing is fine for development and testing but it's not really an "application" yet. I've already seen Gradio mentioned for Python web interfaces so I'll look into that next. Lefteris's point about testing with your own handwriting is a good feature idea — the whole point of the project is digit recognition so you should be able to give it your own digits, not just ones from the dataset.

The phone app idea from Lefteris is interesting but completely out of scope. I'll stick to a web interface. Yiannis's logging idea is something I might come back to but I've got more important things to build first.

### What I'll do next

- Look into Gradio for building a web interface
- Add the ability to upload your own images (not just test set indices)
