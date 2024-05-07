# -*- coding: utf-8 -*-
"""[Phân tích nhận dạng mẫu]Nhận dạng chữ viết tay.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oP9OTfxzNbg482Z8TdE4JdTmgY-8YTXM
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import tensorflow as tf
from tensorflow.keras.models import Sequential , Model
from tensorflow.keras.layers import Dense, Dropout
import seaborn as sns
sns.set()

np.random.seed(0)

from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

missing_values = np.isnan(x_train).sum() + np.isnan(x_test).sum()
if missing_values > 0:
    print(f"Số lượng giá trị bị thiếu: {missing_values}")
    x_train = np.nan_to_num(x_train, nan=np.mean(x_train))
    x_test = np.nan_to_num(x_test, nan=np.mean(x_test))

num_classes = 10

f, ax = plt.subplots(1, num_classes, figsize = (20,20))

for i in range(0, num_classes):
    sample = x_train[y_train == i][0]
    ax[i].imshow(sample, cmap='gray')
    ax[i].set_title(f'Label: {i}', fontsize=16)

for i in range(10):
    print(y_train[i])

y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes)

for i in range(10):
    print(y_train[i])

x_train = x_train / 255.0
x_test = x_test / 255.0

x_train = x_train.reshape(x_train.shape[0], -1)
x_test = x_test.reshape(x_test.shape[0], -1)

print(x_train.shape)

# Trích xuất đặc trưng từ tầng trung gian
intermediate_layer_model = Model(inputs=model.input, outputs=model.layers[1].output)
features = intermediate_layer_model.predict(x_test)

# In kích thước của đặc trưng
print(f"Kích thước đặc trưng: {features.shape}")

# Gom nhóm các đặc trưng theo kiểu dữ liệu
numeric_features = x_train.shape[1]
categorical_features = 0  # Không có đặc trưng phân loại trong trường hợp này

print(f"Số lượng đặc trưng số học: {numeric_features}")
print(f"Số lượng đặc trưng phân loại: {categorical_features}")

# Hiển thị đặc trưng của một số mẫu
plt.figure(figsize=(12, 6))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(features[i].reshape(16, 8), cmap='viridis')  # Thay đổi kích thước hiển thị nếu cần
    plt.title(f'Label: {np.argmax(y_test[i])}')
    plt.axis('off')
plt.show()

model = Sequential()

model.add(Dense(units = 128, input_shape = (784,), activation = 'relu'))
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dropout(0.25))
model.add(Dense(units = 10, activation = 'softmax'))

model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

model.summary()

history = model.fit(x=x_train, y=y_train, batch_size=512, epochs=10, validation_data=(x_test, y_test))

plt.figure(figsize=(12, 6))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

test_loss, test_acc = model.evaluate(x_test, y_test)

print(f'Test Loss: {test_loss}, \nTest Accuracy: {test_acc}')

y_pred = model.predict(x_test)
y_pred_classes = np.argmax(y_pred, axis = 1)
print(y_pred)
print(y_pred_classes)

random_idx = np.random.choice(len(x_test))
x_sample = x_test[random_idx]
y_true = np.argmax(y_test, axis = 1)
y_sample_true = y_true[random_idx]
y_sample_pred_class = y_pred_classes[random_idx]

plt.title(f'Predicted: {y_sample_pred_class}, \nTrue: {y_sample_true}', fontsize = 16)
plt.imshow(x_sample.reshape(28,28), cmap = 'gray')