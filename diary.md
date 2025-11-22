# Phase 11 Development Diary

## What This Phase Is About

Until now, Phase 3's MLP was the only model architecture available. It works fine and gets
about 97%, but MLPs flatten the image into a long list of pixels and lose where things actually are in the image. A pixel at (10, 15) and one at (10, 16) might be right next to each other, but
the MLP doesn't know that. CNNs (Convolutional Neural Networks) fix this by using small
filters that slide across the image and pick up things like edges and curves. I wanted
to add a Small CNN and a Deeper CNN as options alongside the MLP.

## Learning About CNNs

I spent a while reading the Keras docs on Conv2D layers. From what I understand, you set up a bunch of small filters (like 32 of them, each 3×3 pixels) and each filter learns to spot a different pattern in the image. The early layers find basic stuff like edges. If you stack more layers, the later ones start recognising combinations of those edges - curves, loops, that sort of thing. MaxPooling shrinks everything down by keeping only the strongest signal from each small region, which also helps if the digit is slightly off-centre.

For the Deeper CNN I also added Dropout layers. The idea is you randomly turn off some neurons during each training step - 25% of them after the conv layers and 50% before the final output. It felt wrong at first because you're deliberately making the network worse during training. But apparently it forces the remaining neurons to pick up the slack, so the final model ends up more robust.

## The Reshape Problem

This tripped me up for a bit. My first CNN attempt crashed immediately with "expected 4D
input, got 3D". The MLP takes flat (28, 28) data, but Conv2D needs (28, 28, 1) - that extra
1 is the channel dimension (1 for greyscale, would be 3 for RGB). Once I understood what
the error actually meant, the fix was simple: add a Reshape layer at the start of each CNN
to tack on that channel dimension. Felt obvious afterwards, but the error message on its
own wasn't immediately clear about what was missing.

## Building the Architectures and UI

I defined `create_small_cnn()` and `create_deeper_cnn()` in models.py alongside the
existing `create_mlp()`. The Small CNN is pretty minimal: one Conv2D layer (32 filters,
3×3), one MaxPooling, Flatten, then Dense(64) before the 10-class softmax output. The
Deeper CNN stacks two Conv2D layers (32 and 64 filters) before pooling, adds Dropout(0.25),
then Dense(128) with Dropout(0.5) before output. Both start with a Reshape layer for the
channel dimension.

On the Gradio side, I added a `gr.Dropdown` with the three architecture choices and updated
the training function to accept it as the first parameter, using if/elif to create the right
model. Had to update the imports too. I initially only had `create_mlp` imported, which gave
a NameError when trying to call `create_small_cnn()`.

## Testing

I ran all three architectures at 3 epochs, batch size 32:

| Architecture | Final Val Accuracy | Rough Time per Epoch |
|---|---|---|
| MLP | ~97% | ~15s |
| Small CNN | ~98.5% | ~25s |
| Deeper CNN | ~99%+ | ~40s |

The accuracy gap isn't massive on MNIST but the CNNs are clearly better. The downside is training time - Deeper CNN takes nearly three times as
long per epoch. I also checked the dropdown returns the actual string ("MLP", not an index),
which made the if/elif matching straightforward.

## Reflection

This was the interesting one. CNNs feel like a proper step up from
the MLP. The idea that you can stack layers so the first one finds edges and the later ones recognise
whole digits is genuinely cool. Dropout felt counterintuitive at first (deliberately
breaking things during training to make the final model better?) but the results clearly show it works.

One problem I can already see: all three architectures save to the same model file, so
training a Deeper CNN just overwrites whatever was there before. Can't actually compare
models side by side, which defeats the point of having multiple architectures. Phase 12
should sort that out with proper history tracking.

Took a couple hours but CNNs were completely new so I actually spent time learning how they work rather than just copying tutorial code.
