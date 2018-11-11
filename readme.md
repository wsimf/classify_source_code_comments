# Clustering Source code comments

### System Requirements

  - [Python 3.6] (pythonw (Python GUI) is required to view the plot results)
  - [pip3] (for installing python dependent modules) 
  
### Python Dependencies
 - [nltk]
 - [pandas]
 - [sklearn]
 - colorma
 - javalang
 - python-dateutil

### Preparing Environment
- Unzip or clone (```git clone https://github.com/wsimf/classify_source_code_comments.git```) the project to a convenient location
- Open the command prompt / terminal and navigate to the project folder
- Make sure Python3 is installed (```python -V```)
- Install pythonw (if you are using [anaconda] for python environment management, you can use ```conda install python.app``` on a macOS environment)
- Install dependencies (```pip install -r requirements.txt```)

### Running the application
- Copy Java source files into ```/comment_resources``` directory
- Run ```pythonw comment_analyser.py ```
- All the found comments will be written into ```comments.txt``` file 
- The clustered result will be written into ```comments_cluster_dbscan.txt``` file
- The count and TF-IDF vectorizer results will open in a seperate window

Python GUI (plot results) were tested on a macOS environment. The ```pythonw``` should be installed depending on the operating system used. Not all operating systems support python GUI. The program would fail with an error if it was unable to draw the GUI component. However, the ```comments.txt``` and ```comments_cluster_dbscan.txt``` will get generated irrespective of this issue.


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[Python 3.6]: <https://www.python.org/downloads/>
[pip3]: <https://docs.python.org/3/installing/index.html>
[nltk]: <http://www.nltk.org>
[pandas]: <https://pandas.pydata.org>
[sklearn]: <https://scikit-learn.org/stable/>
[anaconda]: <https://anaconda.org>
