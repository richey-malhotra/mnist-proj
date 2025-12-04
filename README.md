# Phase 13 (Part 2): Moved Shared Code into utils.py

## What Changed

- Created `utils.py` with a shared `preprocess_image()` function
- Moved ~15 lines of image conversion code out of `app_ui.py`
- `predict_uploaded_image()` now calls the shared function instead of doing it all inline
- No visible changes to the app — just tidier code underneath

I was about to start Phase 14 which needs the same preprocessing, and was going to copy-paste the whole block when I realised that'd mean maintaining the same code in two places. Annoying if there's ever a bug. So I pulled it into its own file instead.

VS Code actually has a thing where you select code and it offers to "extract" it into a function for you (little lightbulb in the margin). I tried it and it worked, but it put the function in the same file. I wanted it in a separate file so Phase 14 can import it too. Ended up doing it manually — created `utils.py` with the preprocessing function, then replaced the 15 lines in `app_ui.py` with a single function call. The idea is `models.py` has model definitions, `utils.py` has shared helpers, and `app_ui.py` has the UI. Each file does one thing.

Apparently reorganising code like this without changing what it does is called "refactoring". Felt a bit like overkill for what's basically moving lines between files, but it does make the code easier to work with.

## The PIL Type Issue

My first version just did `Image.fromarray(image)` directly, but Gradio can pass float32 arrays and PIL's `fromarray` only accepts uint8. Got a `ValueError` about unhandled data types. The fix was converting to uint8 first, then handling both RGB and greyscale inputs:

```python
if isinstance(image, np.ndarray):
    if len(image.shape) == 3:
        img = Image.fromarray(image.astype('uint8')).convert('L')
    else:
        img = Image.fromarray(image.astype('uint8'))
```

Not complicated, just fiddly. The kind of thing where you write three lines to fix a type issue that would otherwise crash on certain inputs.

## Testing

Uploaded a test digit and got the same prediction and confidence as Phase 12. Trained a model to make sure that path still works, checked the History tab. Everything working exactly the same, so the reorganisation didn't break anything. If you opened the app you wouldn't notice any difference.

Knocked this out in under an hour. Probably the fastest phase so far.

## A Couple of Gotchas

### uint8 Cast Before PIL

```python
img = Image.fromarray(image.astype('uint8'))
```

Gradio passes images as float32 NumPy arrays but PIL's `Image.fromarray()` only accepts uint8. Without the `.astype('uint8')` it throws a `ValueError`. I wasn't sure why at first - turns out PIL is just stricter about data types than NumPy is.

### Separate utils.py Instead of Keeping It in app_ui.py

I could have just made `preprocess_image()` a function at the top of `app_ui.py`. I went with a separate file because Phase 14 will need to import it too, and having shared code sitting inside the UI file felt messy. If I ever need to change how preprocessing works, there's exactly one place to look.

## File Structure

```
gradio_phase13/
├── app_ui.py          # Main application (~320 lines, slightly less than Phase 12)
├── utils.py           # Preprocessing function (42 lines, NEW)
├── init_db.py         # Database initialisation (49 lines, unchanged)
├── models.py          # 3 architectures (unchanged)
├── requirements.txt   # Dependencies (unchanged)
└── artifacts/
    ├── training_history.db
    └── model_{arch}_run{id}.keras
```
