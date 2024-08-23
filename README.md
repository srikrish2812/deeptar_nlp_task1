# deeptar_nlp_task1


The hardware used for this project is Macbook M1 pro 16gb ram. The environment creation steps are exclusive to macOS only. Please refer online guide to create a python virtual environment in Windows.

1. First clone the repository to your local machine and move to that directory. Then create a virtual environment and install the packages from requirements.txt file.
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
2. The data from (https://www.nhs.uk/conditions) can be extracted and nlp-related statistics can be saved using the [python notebook](notebooks/scrape_and_analyse.ipynb)

3. A better way to extract data is by running the code from the command line using [scraper.py](scraper.py) file. Before running it make sure that you are in the project directory and virtual environment is activated. After taking care of above things, run the following code from terminal. This step may take 4 to 5 mins based on your machine's configuration. The statistics report is saved to [statistics](statistics) folder.
```
python scraper.py
```

4. After the above step is successful, lets launch the flask server and compare the input text with the aggregate results. This project uses [index.html](templates/index.html) and [comparison.html](templates/comparison.html) in the [templates](templates) folder. To launch the server run the following command in terminal
```
python app.py
```

5. After the server launches successfully enter the following url in your browser: http://127.0.0.1:5000/ and enter any text from health related website to compare the statistics. 

6. After you enter the text, please click on the Analyze Text button present below to go to a new page showing comparison results.

7. After working with the website close the server by pressing ctrl+c in terminal and deactivate the environment.



