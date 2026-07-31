import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
import matplotlib.pyplot as plt
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import classification_report, confusion_matrix

# Data generators
train_data = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    validation_split=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    fill_mode='nearest'
)

test_data = ImageDataGenerator(
    rescale=1./255,
    rotation_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_img = train_data.flow_from_directory(
    directory='dataset/train',
    batch_size=32,
    target_size=(128,128),
    class_mode='sparse'
)

test_img = train_data.flow_from_directory(
    directory='dataset/test',
    batch_size=32,
    target_size=(128,128),
    class_mode='sparse'
)

# CNN model
nn = Sequential([
    Conv2D(32,(3,3), activation='relu', padding='valid', input_shape=(128,128,3)),
    MaxPooling2D(pool_size=(2,2), strides=(2,2)),
    Conv2D(64,(3,3), activation='relu', padding='valid'),
    MaxPooling2D(pool_size=(2,2), strides=(2,2)),
    Conv2D(128,(3,3), activation='relu', padding='valid'),
    BatchNormalization(),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dropout(0.5),
    Dense(5, activation='softmax')
])

nn.compile(loss="sparse_categorical_crossentropy", optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])

checkpoints = ModelCheckpoint(
    filepath='best_model.keras',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

history = nn.fit(
    train_img,
    validation_data=test_img,
    epochs=32,
    batch_size=32,
    callbacks=[EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True), checkpoints],
    verbose=1
)

# Plot accuracy
plt.plot(history.history['accuracy'], label="Accuracy")
plt.plot(history.history['val_accuracy'], label="Validation Accuracy")
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()

# Plot loss
plt.plot(history.history['loss'], label="Loss")
plt.plot(history.history['val_loss'], label="Validation Loss")
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

# Load best model
model = load_model("best_model.keras")

try:
    path = input("Enter the image path or folder path: ")
except FileNotFoundError:
    print("File not found...")
except Exception as e:
    print("Error: ", e)

if os.path.isfile(path):
    print("Single file processing...\n")
    img_obj = image.load_img(path, target_size=(128,128))
    img_arr = image.img_to_array(img_obj, dtype=np.float32)
    re_img = img_arr/255.0
    re_img = np.expand_dims(re_img, axis=0)
    prob = model.predict(re_img)
    pred = np.argmax(prob)
    classes = ["Good","crack","scratch","Dent","Broken"]
    print(f"Predicted class: {classes[pred]}")

elif os.path.isdir(path):
    print("Folder processing...")
    for filename in os.listdir(path):
        img_path = os.path.join(path, filename)
        img_obj = image.load_img(img_path, target_size=(128,128))
        img_arr = image.img_to_array(img_obj, dtype=np.float32)
        re_img = img_arr/255.0
        re_img = np.expand_dims(re_img, axis=0)
        prob = model.predict(re_img)
        pred = np.argmax(prob)
        classes = ["Good","crack","scratch","Dent","Broken"]
        print(f"{filename} → Predicted class: {classes[pred]}")
else:
    print("Invalid path...")
