import tensorflow as tf
import numpy as np
import os
import random
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from tensorflow import keras
from keras.utils import to_categorical
from partA.data import preprocess_img, get_resized_image

best_model = keras.models.load_model('best_model')
test = preprocess_img(datatype='test',batch_size=32,target_size=(240,240))

def report_accuracy():
	best_model.summary()
	# Reference: https://stackoverflow.com/questions/61742556/valueerror-shapes-none-1-and-none-2-are-incompatible
	one_hot_label = to_categorical(test.y)
	""" Evaluates the mean loss for a batch of inputs and accuracy.
		If the model has lower loss (score) at test time, it will have lower prediction error and hence higher the accuracy. 
		Similarly, when test accuracy is low the score is higher.
	"""
	score, acc = best_model.evaluate(test.x,one_hot_label, batch_size=32, verbose = 0)
	print('Test accuracy:', acc)

def plot_test_predictions(no_of_files=30,target_size=(240,240)):
	test_data = []
	base_path=os.path.join(os.path.dirname(os.getcwd()),'iNaturalist_Dataset','inaturalist_12K','test')
	label_dict = {'Amphibia': 0, 'Reptilia': 1, 'Plantae': 2, 'Mollusca': 3, 'Fungi': 4, 'Aves': 5, 'Mammalia': 6,
					  'Animalia': 7, 'Insecta': 8,
					  'Arachnida': 9}
	true_class = []

	for i in range(no_of_files):
		class_label = random.choice(list(label_dict.keys()))
		true_class.append(class_label)
		# folder_path stores the name of the random folder corresponding to a class label chosen
		folder_path=os.path.join(base_path,class_label)
		# random_file stores the name of the random file chosen
		random_file=random.choice(os.listdir(folder_path))
		file_path=os.path.join(folder_path,random_file)
		new_im = get_resized_image(desired_size=target_size[0], file=file_path)
		img = np.array(new_im)
		test_data.append(img)
	""" 
		Since Keras expects the input format to be of type (n_samples, height, width, channels) 
		so we convert the test_data to numpy array.
	"""
	plt.figure(figsize=(30,30))
	classes = best_model.predict_classes(np.array(test_data))
	predicted_class = []
	for i in range(0,len(classes)):
		for key, value in label_dict.items():
			if value == classes[i]:
				predicted_class.append(key)
				ax=plt.subplot(10, 3, i + 1)  # the number of images in the grid is 10*3 (30)
				ax.get_xaxis().set_visible(False)
				ax.get_yaxis().set_visible(False)
				if true_class[i] == predicted_class[i]:
					color ='green'
				else:
					color ='red'
				ax.set_title(key,color=color)
				plt.tight_layout(pad=5)
				plt.imshow(test_data[i])

	plt.show()

report_accuracy()
plot_test_predictions(no_of_files=30,target_size=(240,240))