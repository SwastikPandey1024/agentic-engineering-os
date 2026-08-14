---
name: deep-learning
description: Deep learning workflows, PyTorch/TensorFlow, transfer learning, medical/image processing (DICOM), GPU memory management, mixed precision, and checkpointing.
---

# Deep Learning Skill

## 1. When Should I Use This?

Use this skill when:
* Developing or training computer vision, CNN, transfer learning, or sequence models with **PyTorch** or **TensorFlow 2.16+ / Keras 3**.
* Processing image, medical imaging (DICOM via `pydicom`), or audio datasets.
* Managing GPU training resources, mixed precision (`torch.cuda.amp` / `keras.mixed_precision`), batch memory limits, and checkpointing.
* Setting up multi-GPU distributed strategies or Kaggle/Colab training pipelines.

---

## 2. What Should I Inspect First?

1. **Hardware & CUDA State**:
   * Inspect GPU availability: `nvidia-smi` or `torch.cuda.is_available()` / `tf.config.list_physical_devices('GPU')`.
   * Check VRAM size (8GB, 16GB, 24GB) to establish safe batch sizes (e.g. batch size 16/32 for 224x224 images).
2. **Dataset Format & Split Strategy**:
   * Inspect raw image resolutions, color channels, and metadata manifests.
   * For medical data: Group by `patient_id` to ensure 0% patient leakage between train and validation.
3. **Pretrained Weights**: Determine backbone architecture (DenseNet121, ResNet50, EfficientNet-B0).

---

## 3. What Workflow Should I Follow?

```text
Smoke Test on Tiny 50-Sample Subset (Verify Forward/Backward Pass)
                     ↓
Group-Aware / Leak-Free Data Partitioning
                     ↓
Build High-Throughput Input Pipeline (tf.data.Dataset / DataLoader)
                     ↓
Initialize Backbone with Pretrained Weights
                     ↓
Phase 1 Training: Freeze Backbone (Train Classification Head Only)
                     ↓
Phase 2 Fine-Tuning: Unfreeze Top Layers with Low LR (Keep BatchNorm Frozen)
                     ↓
Monitor Validation Loss & Early Stopping
                     ↓
Save Best Checkpoints & Confusion / ROC Curves
```

### High-Throughput TensorFlow/Keras Input Pipeline

```python
# ml/data_loader.py
import tensorflow as tf

def build_dataset(image_paths: list[str], labels: list[int], img_size=(224, 224), batch_size=32, is_training=True):
    def parse_image(path, label):
        raw = tf.io.read_file(path)
        img = tf.io.decode_jpeg(raw, channels=3)
        img = tf.image.resize(img, img_size)
        img = tf.cast(img, tf.float32) / 255.0  # Normalize to [0, 1]
        return img, tf.cast(label, tf.float32)

    ds = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    if is_training:
        ds = ds.shuffle(buffer_size=1000)
    
    ds = ds.map(parse_image, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(batch_size)
    ds = ds.prefetch(buffer_size=tf.data.AUTOTUNE)
    return ds
```

### Transfer Learning with BatchNorm Protection

```python
# ml/models/transfer_learning.py
import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras import layers, models

def build_densenet_model(input_shape=(224, 224, 3), num_classes=1, fine_tune_layers=20):
    base_model = DenseNet121(weights="imagenet", include_top=False, input_shape=input_shape)
    
    # Phase 1: Freeze all base model weights
    base_model.trainable = False

    inputs = layers.Input(shape=input_shape)
    x = base_model(inputs, training=False) # Keep BatchNorm in inference mode!
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    outputs = layers.Dense(num_classes, activation="sigmoid" if num_classes == 1 else "softmax")(x)

    model = models.Model(inputs, outputs)
    return model, base_model

def unfreeze_for_finetuning(model, base_model, fine_tune_layers=30, learning_rate=1e-5):
    base_model.trainable = True
    # Freeze all layers except the last fine_tune_layers
    for layer in base_model.layers[:-fine_tune_layers]:
        layer.trainable = False
        
    # Crucial Rule: Keep BatchNormalization layers frozen during fine-tuning to prevent weight destruction
    for layer in base_model.layers:
        if isinstance(layer, layers.BatchNormalization):
            layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc")]
    )
    return model
```

---

## 4. What Decisions Should I Make?

| Challenge | Engineering Best Practice |
| :--- | :--- |
| **Out-Of-Memory (OOM) Errors** | 1. Reduce batch size (e.g. 64 → 32 → 16).<br>2. Enable Mixed Precision (`float16`).<br>3. Use Gradient Accumulation if effective batch size must remain large. |
| **Overfitting on Small Datasets** | Apply spatial data augmentations (random rotations, horizontal flips, zooming, color jitter), increase dropout (0.3-0.5), and use early stopping with `patience=5`. |
| **Model Checkpointing** | Always save checkpoints with `save_best_only=True` monitoring `val_loss` or `val_auc`. |

---

## 5. What Should I Avoid?

* **NEVER launch an overnight training run without a 1-epoch smoke test**: Always verify the pipeline runs end-to-end on 50 samples first.
* **NEVER unfreeze BatchNorm layers during fine-tuning on small datasets**: Unfrozen BatchNorm destroys pretrained statistics and causes validation divergence.
* **NEVER evaluate on unnormalized test data**: Ensure test images undergo the exact same normalization and resizing applied during training.

---

## 6. How Should I Verify Success?

```bash
# 1. Run quick GPU smoke test (1 epoch on 50 dummy samples)
python ml/training/smoke_test.py

# 2. Verify model summary and trainable parameter counts
python -c "
from ml.models.transfer_learning import build_densenet_model
model, base = build_densenet_model()
print('Trainable params:', sum([tf.size(w).numpy() for w in model.trainable_weights]))
"

# 3. Verify saved model artifact format and inference
python ml/inference/predict.py --image-path test_sample.jpg
```
