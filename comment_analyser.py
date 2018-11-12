import colorama
import os
import data_cleaning
import numpy as np
import matplotlib.pyplot as plt
from data_cleaning import DataCleaner
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from java_file_inspector import JavaFileInspector


def main():
    colorama.init()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    inspector = JavaFileInspector("{}/comment_resources".format(dir_path))

    comments_data = inspector.get_comments()
    comments_file = open("comments.txt", "w+")
    comments = []
    print("Comment data obtained")

    for key, value in comments_data.items():
        print(colorama.Fore.GREEN + "[FILE] : " + key)
        comments_file.write("** [FILE] : " + key + "\n")

        for item in value:
            if item.comment not in comments:
                if len(item.comment.split()) > 10:
                    if not DataCleaner.check_if_copyright(item.comment):
                        print(colorama.Fore.YELLOW + "      [COMMENT] : " + item.comment + "\n")
                        comments_file.write("      [COMMENT] : " + item.comment + "\n")
                        comments.append(item.comment)
        comments_file.write("\n")

    print(colorama.Fore.RESET)
    print("Corpus preparation done. Size: ", len(comments))
    comments_file.write("Found {} comments in {} files".format(len(comments), len(comments_data.items())))
    comments_file.close()

    count_vector = CountVectorizer()
    count_result = count_vector.fit_transform(comments)
    print("CountVectorizer Array:")
    print(count_result.toarray())

    vector = TfidfVectorizer(analyzer='word', stop_words='english', lowercase=True, max_features=5000,
                             tokenizer=data_cleaning.data_tokenize_clean, strip_accents='ascii', ngram_range=(0, 1))
    tfidf_v = vector.fit_transform(comments)

    print(colorama.Fore.YELLOW + "Number of feature names : ", len(vector.get_feature_names()))
    print(colorama.Fore.YELLOW + "Number of comments : ", len(comments))
    print(colorama.Fore.RESET)

    print("TF-IDF Vectorizer size : ", len(tfidf_v.toarray()))

    db = DBSCAN(eps=0.7, min_samples=3).fit(tfidf_v)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)  # Remove noise (with cluster id -1)

    print('Estimated number of clusters: %d' % n_clusters_)

    cluster_data = {}
    avg = []
    for index, item in enumerate(labels, start=0):
        if cluster_data.get(item) is None:
            cluster_data[item] = []

        cluster_data[item].append(comments[index])

    print("Cluster data prepared")
    cluster_file = open("comments_cluster_dbscan.txt", "w+")

    for index, data in cluster_data.items():
        if index == -1:
            continue

        print(colorama.Fore.YELLOW + "Cluster ", index)
        cluster_file.write("** [CLUSTER] : {} \n".format(index))
        for comment in data:
            cluster_file.write("      [COMMENT] : " + comment + "\n")
            print(colorama.Fore.GREEN + comment + "\n")

        print("TOTAL : ", len(data))
        print(colorama.Fore.YELLOW + "** END **\n")
        cluster_file.write("\n")
        avg.append(len(data))

    cluster_file.close()

    total = 0
    for i in avg:
        total = total + i

    print("AVERAGE: ", total / len(avg))

    plt.subplot(121)
    plt.imshow(count_result.toarray())
    plt.colorbar()
    plt.title("CountVectorizer")

    plt.subplot(122)
    plt.imshow(tfidf_v.toarray())
    plt.colorbar()
    plt.title("TF-IDF Vectorizer")

    plt.show()


if __name__ == '__main__':
    main()
