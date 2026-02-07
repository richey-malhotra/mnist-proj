# Test Scripts and Video Recordings

## what this is

Mr Davies said I should record myself actually testing the app to prove it works, not just have the written test log. Fair enough. So I went back and wrote proper test scripts for the 7 main features and recorded screen captures of each one.

## the videos

1. Model training (Phase 3 terminal) — just the MLP training running in the terminal
2. Image upload predictions (Phase 7) — uploading digit images and getting predictions
3. CNN comparison training (Phase 11) — training all three architectures back to back
4. Database history (Phase 13) — showing runs saving to SQLite and appearing in the table
5. Charts dashboard (Phase 15-16) — the Plotly accuracy and training time charts
6. Error handling and drawing (Phase 20) — input validation, the drawing canvas, edge cases
7. Full end-to-end system demo — everything working together from scratch

## how long

About 4 hours across two evenings (5th-6th Feb). Writing the scripts was quick but had to redo a couple recordings when things went wrong. The CNN training one took ages because it actually trains 3 models in the recording. Named the folders by the date of the phase they're testing, not when I actually recorded them — probably shouldnt have done that but I'd already committed them before I thought about it.

## what I learned

Recording yourself doing something is way harder than just doing it. You notice all the little UI glitches you normally ignore. But its decent evidence that everything actually works and I'm not just saying it does in the test log.
