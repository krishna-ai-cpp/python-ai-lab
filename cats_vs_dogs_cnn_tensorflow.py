import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Rescaling, Dropout, BatchNormalization
import matplotlib.pyplot as plt

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import classification_report, confusion_matrix

# Load datasets
train_data = tf.keras.preprocessing.image_dataset_from_directory(
    r"C:\Users\Krishna\Downloads\archive\training_set",
    image_size=(128,128),
    batch_size=32,
    label_mode="binary"
)

test_data = tf.keras.preprocessing.image_dataset_from_directory(
    r"C:\Users\Krishna\Downloads\archive\test_set\test_set",
    image_size=(128,128),
    batch_size=32,
    label_mode="binary"
)

# Build CNN
nn = Sequential([
    Rescaling(1./255, input_shape=(128,128,3)),
    Conv2D(16, 3, activation="relu"),
    MaxPooling2D(),
    Conv2D(32, 3, activation="relu"),
    MaxPooling2D(),
    Conv2D(64, 3, activation="relu"),
    MaxPooling2D(),
    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    BatchNormalization(),
    Dense(64, activation="relu"),
    Dropout(0.5),
    BatchNormalization(),
    Dense(32, activation="relu"),
    Dropout(0.5),
    BatchNormalization(),
    Dense(16, activation="relu"),
    Dropout(0.5),
    BatchNormalization(),
    Dense(8, activation="relu"),
    Dropout(0.5),
    BatchNormalization(),
    Dense(4, activation="relu"),
    Dropout(0.5),
    BatchNormalization(),
    Dense(1, activation="sigmoid")
])

nn.compile(loss="binary_crossentropy", optimizer=Adam(learning_rate=0.001), metrics=["accuracy"])

# Train
history = nn.fit(
    train_data,
    validation_data=test_data,
    epochs=20,
    callbacks=[EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True)]
)

plt.plot(history.history['accuracy'],label = "Training Accuracy")
plt.plot(history.history['val_accuracy'],label = "Validation Accuracy")
plt.legend()
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.grid(True)
plt.show()
plt.plot(history.history['loss'],label = "Training Loss")
plt.plot(history.history['val_loss'],label = "Validation Loss")
plt.legend()
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.grid(True)
plt.show()

# Evaluate
test_loss, test_acc = nn.evaluate(test_data)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_acc)

# Collect test data into arrays
x_test, y_test = [], []
for images, labels in test_data:
    x_test.append(images.numpy())
    y_test.append(labels.numpy())

x_test = np.concatenate(x_test)
y_test = np.concatenate(y_test)

# Predict probabilities
pred_probs = nn.predict(x_test)

# Convert to binary predictions (0 = cat, 1 = dog)
pred = (pred_probs > 0.5).astype("int64")

# Evaluate with sklearn
from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(y_test, pred))
print(confusion_matrix(y_test, pred))
