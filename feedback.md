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
---

## Phase 9 — Video call with Petros (early November)

### When and how

Video called Petros to show him how the project was going. Screen-shared the Gradio app running in the browser. He was in Athens so we did it over Google Meet. We chatted for a bit first about how uni was going - he's doing a machine learning module this term which is partly why he had so much to say about the technical side.

### What he could see

Working Gradio interface with tabs. You can upload an image and get a prediction. The MLP model is trained and loaded. The UI has a Train tab and a Predict tab.

### What he said

**Petros:** "The interface is clean, nice work. I have a couple of thoughts though."

"First — you're only using an MLP right now. So the thing with MLPs is they flatten the image into a single vector, right? Which means you basically lose all the spatial information — the model doesn't know that pixel (1,1) is next to pixel (1,2). Have you looked into convolutional neural networks? They use these filters that slide across the image, so they can pick up on edges and shapes and that kind of thing. For image stuff they pretty much always do better than MLPs. I'd try at least two different CNN architectures so you can compare."

"Second thing — when I clicked 'Start Training' the page just froze for about 30 seconds. I thought it had crashed. There's no indication that anything is happening. You should show some kind of progress, even if it's just printing the epoch number as it goes."

He also mentioned data augmentation — "you could rotate, shift, or zoom the training images slightly to create more training data. It helps the model generalise better, especially for small datasets. MNIST is big enough that you probably don't need it, but it's worth knowing about for future reference." I wrote this down but it's not something I'm going to implement for this project since MNIST has 60,000 images already.

Before we hung up he asked how much of the coursework mark is for the code vs the write-up. I said it's split across the whole thing — analysis, design, testing, evaluation. He said "make sure you document your design decisions properly, not just what you built but WHY you chose that approach. That's what they look for at uni too." Good advice.

### My thoughts

Both really good points about the MLP and progress display. I've heard of CNNs but haven't tried implementing one yet. The progress thing is embarrassing — I should've noticed that myself. From the user's perspective it looks completely broken when it freezes.

Petros doesn't tell me HOW to do things which is good because I need to figure it out myself for the coursework, but he points me in the right direction. I'll look up CNN architecture in TensorFlow and also look into how Gradio handles streaming output.

The data augmentation idea is interesting but I've got enough to do already. Might look into it later if I have time.

### What I'll do next

- Research CNN model architecture (convolutional layers, pooling, etc.)
- Fix the training progress to show live updates somehow
- Try at least 2 different CNN designs (small and deeper)
---

## Phase 11 — Thanos visiting over the weekend (end of November)

### When and how

Thanos was visiting the family over the weekend. Showed him the project on my laptop after dinner, we were in the living room and my dad kept interrupting to offer us tea. He sat next to me and I walked him through the code as well, not just the app. Had to explain the project brief first because he didn't know what the coursework actually required.

### What he could see

Full app with three model architectures (MLP, Small CNN, Deeper CNN), live training progress, and image upload prediction. Training results only show during the session — nothing persists.

### What he said

**Thanos:** He spent the first few minutes just clicking around the interface without saying much. Trained an MLP, looked at the prediction page, tried uploading an image. Then he said "OK this is actually pretty decent for a school project. The UI looks professional — what framework is this?" I told him Gradio and he said he hadn't heard of it but it looks decent.

"What IDE are you using?" — I said VS Code and he said "good choice, we use it at work too. Make sure you're using the Python extension, it catches a lot of bugs." (I already am.)

Then he got more specific: "Alright so I've got a few things."

"One — you're training these models and comparing them, but where does the data go when you close the app? If I train three models today and come back tomorrow, can I see those results? Right now it looks like everything disappears."

"Two — you need some kind of data persistence. For a project like this I'd use a database. SQLite would work perfectly — it's just a file, no server needed, and Python has a built-in module for it."

"Three — your code is getting a bit long. How many lines is app_ui.py right now? Everything's in one file. At some point you should think about seperating things out. The model definitions could go in one file, utility functions in another. It's easier to maintain and test."

At one point I was scrolling through the code and he said "hang on, go back — what does that function do?" pointing at the training function. I explained the generator works with yield and he seemed impressed that I'd figured that out. "That's not something most students would know about," he said.

He also said "I work with APIs and backend stuff, not machine learning, so I can't comment on the model architecture side. But the engineering practices apply to any project."

Then he suggested adding proper error logging — "you should log errors to a file so you can debug issues without looking at the console. In production systems we always have logging." I said I'd think about it but honestly for a school project with one user (me) I didn't think logging to a file was worth the effort. The console output is enough for my purposes.

### My thoughts

He's right about the data persistence and code structure for sure. Was a bit nervous showing it to him because he's an actual developer but he seemed genuinely interested rather than just being nice about it. The data disappearing is a real problem I hadn't really thought about because I've been focused on the model side. And the code IS getting messy, app_ui.py is already quite long and it's going to get worse.

I'm not going to add file-based error logging though. It's good practice in industry but for this project it's overkill. The console shows errors fine and I'm the only user.

### What I'll do next

- Set up an SQLite database for storing training history
- Start thinking about splitting the code into separate files
- Save training runs automatically with architecture, epochs, accuracy, and date
---

## Phase 15 — Christmas holiday catch-up (mid-December)

### When and how

Getting close to Christmas holidays so I showed a few people the progress. FaceTimed Lefteris and Yiannis separately, and also had a call with Petros. Wanted to get feedback before I stopped working over Christmas.

### What they could see

Full app with multi-model prediction comparison, training history in a database table, and the accuracy chart I'd just finished adding.

### What Lefteris said

First he asked me to remind him what MLP and CNN mean — "you told me last time but I forgot." I explained again and he said "right yeah, the one with the filters."

"The chart is nice but all the numbers are really similar — like 97%, 98%, 99%. Can you zoom in or something? Also I didn't know which colour was which until I hovered over them."

He also said "which model should I actually use though? They're all really close." I explained that the CNNs are technically better but take longer to train.

He also asked "can't the AI just learn as people use it? Like every time someone draws a digit and confirms what it is, it gets better?" I said that's actually a real thing (online learning) but it's way more complicated than what I'm doing and you'd have to worry about people feeding it bad data.

He then asked "what if instead of uploading a photo you could draw the digit yourself? Like with your finger?" I said that was actually already on my to-do list, so his timing was perfect.

### What Yiannis said

"OK the accuracy is almost the same but how long does each one take to train? Because if the deeper CNN is barely better but takes way longer, is it worth it? Can you add something that shows the training time too?"

He said in his Java project they had to think about efficiency vs quality trade-offs too. He also said "it's come a long way since the terminal version, I barely recognise it" which was nice to hear.

He also suggested "you could add keyboard shortcuts — like press Enter to submit the prediction instead of clicking the button." I thought about it but Gradio doesn't support custom keyboard shortcuts easily and it's not a high priority.

### What Petros said

"Plotly is a good choice for interactive charts. I like the hovering thing where you see the values. If you want to show the trade-off between accuracy and training time, a scatter plot would work well — accuracy on one axis, training time on the other. That way you can see at a glance which models give the best accuracy relative to their training cost."

"Also, you might want to think about cross-validation rather than a single train/test split. It gives a more reliable accuracy estimate." I asked what that means and he explained — basically training multiple times on different subsets of data. Interesting but sounds complicated and I'm running low on time.

### My thoughts

Lefteris is right that when all the accuracies are close together the chart is hard to read. I can't really fix that - it's just that the models really are within a few percent of each other. The y-axis scaling issue is noted in my testing log.

Yiannis's idea about showing training time is really good. I'm not tracking training time yet but it wouldn't be hard to add a duration column to the database and then chart it. The keyboard shortcuts idea is reasonable but lower priority than actual features.

Petros's scatter plot suggestion makes sense — it would show the trade-off between speed and accuracy much more clearly than separate charts for each metric. Cross-validation is beyond what I'm doing — maybe I'll mention it in the evaluation as a "what I'd do next" thing.

### What I'll do next

- Add a training time comparison chart
- Look into a scatter plot for time vs accuracy (the dashboard idea)
