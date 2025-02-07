# MUGE Multimodal Retrieval Baseline

本仓库用于天池电商多模态图文检索挑战赛Baseline算法复现及改进。Baseline来自仓库[image-retrieval-baseline](https://github.com/MUGE-2021/image-retrieval-baseline)

## baseline.ipynb

由于baseline提供的方法将全部数据存入字典，最后保存npz。对于此数据集也就意味着电脑内存需要有100G。由于电脑内存受限，所以本notebook尝试使用部分数据集进行训练。

### 修改部分

* 只读取图片数据集中前12000张。src/preprocess/transform_images.py 中读取tsv行时，增设12000行的限制。
* 由于图片数据集有更改，所以标签文件中 (query-image对) 有些图片数据会不存在，因此将标签文件中不存在的图片删去，重新保存标签。具体见notebook里对应代码。
* 由于baseline采用8 GPU 32 batchsize进行训练。由于条件受限，仅有1块GPU，因此对应将baseline学习率除以8，设为1e-5。

### 结果

此方法在测试集的选取上也是部分的，导致结果缺失图片信息。因此结果较低，仅为9.4125分。

## baseline_full.ipynb

本notebook采用全量数据进行训练。为克服baseline解压时全部存入字典对内存要求的限制，此方法将图片分别存npy文件。

### 修改部分

* 新增 src/preprocess/transform_images_to_npy.py。将每张图片分别保存为npy。
* 修改 src/training/data.py 和 src/eval/data.py 以适应新数据集。
* 单卡 32batchsize 学习率1e-5

### 结果

与[image-retrieval-baseline](https://github.com/MUGE-2021/image-retrieval-baseline)中提到的 **mean-recall of around 50** 对齐。

## cn_clip.ipynb

基于[Chinese-CLIP](https://github.com/OFA-Sys/Chinese-CLIP)进行训练

### baseline结果

使用 CN-CLIP ViT-B/16 预训练模型直接预测。结果为 70.8633 分

### fine-tune


#### test-1

```
warmup=100
batch_size=64
valid_batch_size=64
lr=5e-5
wd=0.001
max_epochs=3
valid_step_interval=150
valid_epoch_interval=1
vision_model=ViT-B-16
text_model=RoBERTa-wwm-ext-base-chinese
```

最后一轮模型提交结果64.3419

#### test-2

```
warmup=100
batch_size=16
valid_batch_size=16
lr=1e-5
wd=0.001
max_epochs=3
valid_step_interval=10000
valid_epoch_interval=1
vision_model=ViT-B-16
text_model=RoBERTa-wwm-ext-base-chinese
```

冻结bert模型。最后一轮提交得分为68.8849。第一轮得分为63.1303。

#### test-2

```
warmup=100
batch_size=16
valid_batch_size=16
lr=1e-5
wd=0.001
max_epochs=3
valid_step_interval=10000
valid_epoch_interval=1
vision_model=ViT-B-16
text_model=RoBERTa-wwm-ext-base-chinese
```

同时冻结bert模型和vision模型。最后一轮提交得分为72.6619。

#### test-3

```
warmup=100
batch_size=16
valid_batch_size=16
lr=1e-5
wd=0.001
max_epochs=3
valid_step_interval=10000
valid_epoch_interval=1
vision_model=ViT-B-16
text_model=RoBERTa-wwm-ext-base-chinese
```

冻结vision模型。最后一轮提交得分为73.2148。

#### test-4

```
warmup=100
batch_size=32
valid_batch_size=32
lr=1e-5
wd=0.001
max_epochs=6
valid_step_interval=10000
valid_epoch_interval=1
vision_model=ViT-B-16
text_model=RoBERTa-wwm-ext-base-chinese
```

冻结vision模型。最后一轮提交得分为74.0741。

#### test-5

```
warmup=100
batch_size=32
valid_batch_size=32
lr=1e-5
wd=0.001
max_epochs=19
valid_step_interval=10000
valid_epoch_interval=1
vision_model=ViT-B-16
text_model=RoBERTa-wwm-ext-base-chinese
```

冻结vision模型。最后一轮提交得分为72.0624。