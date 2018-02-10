# Facial Recognition with Tensorflow

![GudarJS Pycon Profile](images/profile.jpg)

Tensorflow pipeline to recognize faces for python 3.6.

## 1. Installing Dependencies

### FaceNet

Run the following command.

``` bash
git clone https://github.com/davidsandberg/facenet.git
export PYTHONPATH=~/<facenet_path>/src:~/<facenet_path>/contributed
```

* Replace **<facenet_path>** with the facenet installation folder.

### Python modules

Run the following command.

``` bash
pip install -r requirements.txt
```

## 2. Download resources

* [LFW dataset](http://vis-www.cs.umass.edu/lfw/lfw.tgz)

* [Model Checkpoint](https://drive.google.com/file/d/0B5MzpY9kBtDVZ2RpVDYwWmxoSUk)

## 3. Align the LFW dataset

Run the following command.

``` bash
for N in {1..4}; do python ~/<facenet_path>/src/align/align_dataset_mtcnn.py ~/<lfw_path>/raw ~/<lfw_path>/lfw_mtcnnpy_160 --image_size 160 --margin 32 --random_order --gpu_memory_fraction 0.25 & done
```

* Replace **<facenet_path>** with the facenet installation folder.
* Replace **<lfw_path>** with the lfw installation folder.

## 4. Copy the aligned faces to the dataset

Run the following command.

``` bash
cp ~/<lfw_path>/lfw_mtcnnpy_160/* ~/<repo_path>/datasets
```

* Replace **<repo_path>** with this repository installation folder.
* Replace **<lfw_path>** with the lfw installation folder.

## 5. Add a new person

Run the following command.

``` bash
~/<repo_path>/bin/add_new_face
```

* Replace **<repo_path>** with this repository installation folder.

## 6. Train a classifier

Run the following command.

``` bash
python ~/<facenet_path>/src/classifier.py TRAIN ~/<repo_path>/datasets ~/<repo_path>/20170512-110547/20170512-110547.pb ~/<repo_path>/classifier/face_classifier.pkl --batch_size 1000 --min_nrof_images_per_class 40 --nrof_train_images_per_class 40
```

* Replace **<facenet_path>** with the facenet installation folder.
* Replace **<repo_path>** with this repository installation folder.

## Credits

* [FaceNet Repository](https://github.com/davidsandberg/facenet)
* [Multi-task CNN](https://kpzhang93.github.io/MTCNN_face_detection_alignment/index.html)
* ["FaceNet: A Unified Embedding for Face Recognition and Clustering"](http://arxiv.org/abs/1503.03832)

## License

[MIT License](https://github.com/GudarJs/Facial-Recognition-Tensorflow/blob/master/LICENSE)
