from sklearn.decomposition import PCA
from sklearn import preprocessing
import src.image_operations as image_operations
import numpy as np
import matplotlib.pyplot as plt
from src import KNN_sklearn as knn_sklearn


def plot_sample_reductions(train_list, raw_training, test_list, reduced_train, reduced_images, scaler, original_dimensions):
    """
    Gets reduced images, recognizes them via KNN, reverse transforms and plots them
    :param train_list: 784D training images fit to scaler
    :param raw_training: non-reduced train images for plotting
    :param test_list: 784D test images fit to scaler
    :param reduced_train: dimensionally reduced train images for inverse transform
    :param reduced_images: dimensionally reduced test images for inverse transform
    :param scaler: object that was fit to the training images, required for proper inverse transform
    :param original_dimensions: number of dimensions of reduced images
    :return:
    """
    images = list()
    for i in range(4):
        images.append(increase_dimensions(train_list, reduced_images, original_dimensions, scaler, i))
    pred = knn_sklearn.knn_sk(reduced_train, reduced_images, [csv_image.label for csv_image in raw_training], 3, 0, 4)
    plt.figure(figsize=(5, 10))
    for i in range(4):
        plt.subplot(4, 2, 2 * i + 1)
        plt.imshow(np.asarray(test_list[i].image).reshape(28, 28),
                   cmap=plt.cm.gray, interpolation='nearest',
                   clim=(0, 255))
        plt.xlabel(f"Original image", fontsize=14)
        plt.subplot(4, 2, 2 * i + 2)
        plt.imshow(np.asarray(images[i]).reshape(28, 28),
                   cmap=plt.cm.gray, interpolation='nearest',
                   clim=(0, 255))
        plt.xlabel(f"Reduced image \n prediction: {pred[i][1]}", fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_inverse_transforms(train_list, reduced_images, scaler):
    """
    Plots same image reduced to different number of dimensions
    :param train_list: training images normalized by scaler object, required for the PCA object in inverse transform
    :param reduced_images: test images after PCA to 784 dimensions
    :param scaler: scaler object fit to the training images
    :return: None
    """
    # Invert pca for multiple values and draw the yielded images to one plot
    plt.figure(figsize=(10, 5))
    for idx, i in enumerate([10, 20, 40, 70, 100, 200, 400, 784]):
        image = increase_dimensions(train_list, [red[:i] for red in reduced_images], i, scaler, 87)
        plt.subplot(2, 4, idx+1)
        plt.imshow(image.reshape(28, 28),
                   cmap=plt.cm.gray, interpolation='nearest',
                   clim=(0, 255))
        plt.xlabel(f"n(dim) = {i}", fontsize=14)
    plt.tight_layout()
    plt.show()


def increase_dimensions(train_list, reduced_images, original_dimensions, scaler, index):
    """
    Reconstructs visible 28×28 images from dimension reduced ones
    :param train_list: preprocessed training images -> no scaler object necessary
    :param reduced_images: dimension reduced images created by reduce_dimensions
    :param original_dimensions: number of dimensions the images were reduced to
    :return: numpy array of one reconstructed image
    """
    pca = PCA(n_components=original_dimensions)
    pca.fit(train_list)
    approximation = pca.inverse_transform(reduced_images)
    approximation = scaler.inverse_transform(approximation)
    new_image = approximation[index]
    new_image = np.interp(new_image, (new_image.min(), new_image.max()), (0, 255))
    # # For debug: min and max values after scaling
    # print(min(new_image))
    # print("--")
    # print(max(new_image))

    # # Draw scaled image
    # new_image.tolist()
    # new_image = [round(x) for x in new_image]
    # image_operations.draw(new_image)

    return np.around(new_image)

  
def reduce_dimensions(train_list, test_list, target_dimensions) -> tuple:
    """
    Performs pca
    :param train_list: train list
    :param test_list: test list
    :param target_dimensions: number of dimensions to reduce to
    :return: reduced input lists as tuple
    """

    scaler = preprocessing.StandardScaler()

    # Fit on training set only.
    scaler.fit(train_list)

    # Apply transform to both the training set and the test set.
    train_list = scaler.transform(train_list)
    test_list = scaler.transform(test_list)

    # Create instance of pca and fit it only to the training images
    pca = PCA(n_components=target_dimensions)
    pca.fit(train_list)

    # Apply pca to both image lists
    train_pca = pca.transform(train_list)
    test_pca = pca.transform(test_list)

    return train_pca, test_pca, train_list, scaler
