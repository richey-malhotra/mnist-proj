# Test 1: Model Training

**Date:** 1st October 2025  
**Phase tested:** Phase 3 (first MLP model)  
**What I'm testing:** that the model actually trains and accuracy improves each epoch

## Setup

1. Open terminal in project folder
2. Activate venv: `source venv/bin/activate`
3. Run `python app.py`

## Steps to show

| Step | What to do on screen | What to say |
|------|---------------------|-------------|
| 1 | Show the terminal, run the training script | "So I'm going to train the model now. It's a basic MLP — multilayer perceptron — which is like a simple neural network with flat layers." |
| 2 | Point out the epoch counter as it goes up | "You can see it going through the epochs here. Each epoch is one full pass through all the training data." |
| 3 | Watch the accuracy numbers going up each epoch | "The accuracy starts around 90% and then climbs up. The val_accuracy is the important one because that's on data the model hasn't seen before." |
| 4 | Wait for training to finish, point at final accuracy | "It finished at about 97% validation accuracy, which is decent for a basic MLP on MNIST." |
| 5 | Show the saved model file in artifacts/ | "And it saved the model to a .keras file so I don't have to retrain every time I want to use it." |

## Expected vs Actual

| Thing being checked | Expected | Actual |
|---|---|---|
| Training starts without errors | Yes | Yes ✓ |
| Accuracy improves each epoch | Goes up from ~90% to ~97% | Started at 91.2%, finished at 97.4% ✓ |
| Model file saved | .keras file appears in artifacts/ | model_mlp_run1.keras created ✓ |
| No crashes or warnings | Clean output | One TensorFlow info message but nothing bad ✓ |

## Notes

First time training took about 30 seconds on my Mac. The accuracy numbers jump around a bit between epochs which I think is normal — it's not perfectly smooth.
