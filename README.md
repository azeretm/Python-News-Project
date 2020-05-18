# Python "News" Project

In the project we download and scrutinize the headlines of articles from Aktuálně.cz and iDnes.cz.

## Usage
Follow the steps bellow to download and visualize the data.

### 1. Download the content

In [HeadlinesAnalysis.ipynb](HeadlinesAnalysis.ipynb) initialize the class Downloader, which is located in scripts/downloader.py. For specific media server import either DownloaderAktualne or DownloaderIdnes, which handle the download and parse methods for specific media server. Turn verbose=True for logging.

##### Important methods
- downloadHeadlines
Downlaods the desired range of headlines defined by archive pages on the given server. For Aktuálně.cz is it approximately 18 articles per page, for iDnes.cz circa 36 articles per archive page.
- saveToCsv
Saves the data to the file given at the Downloader init. If file exists, the method adds new data to the file, when duplicates are found it keeps the most recent record.


### 2. Analyse the data
In the [HeadlinesAnalysis.ipynb](HeadlinesAnalysis.ipynb), H2O Word2vec model is constructed for each source of news headlines. Consequently, the differences between the synonyms of a given word for both news domains can be examined. At the end of the notebook, one can try to predict the likelihood on which the headline was published by putting the title into the Predict model. See example in [HeadlinesAnalysis.ipynb](HeadlinesAnalysis.ipynb), functions w2v_model.find_synonyms("dotace", count = 10) and predict(["Here comes headline"], w2v_model, gbm_model).

For this purpose a [H2O.ai](https://www.h2o.ai/) open-source platform is used.


### 3. Visualize the data
In [HeadlinesPlots.ipynb](HeadlinesPlots.ipynb) we used Plotly to display frequencies of articles on Aktuálně.cz and iDnes.cz. One can observe different patterns according to month, weekday or time of the day.
