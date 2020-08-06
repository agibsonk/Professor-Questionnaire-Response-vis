# Professor-Questionnaire-Response-vis
Visualization of average response scores through SQCT questionnaire data created using R.
Data was scraped from SQCT website using a Python script to create a CSV. I used Selenium for scraping the data rather than Requests due to the website requiring a password.  

Repository includes the Python file used to scrape SQCT, an R script for plotting the data, and an example dataset and plot generated using both

The python script requries a valid UWO username and password, and also requries a Selenium chrome webdriver.exe to work, which can be obtained from https://sites.google.com/a/chromium.org/chromedriver/downloads.

This project was used as an opportunity to practise data scraping using Python and data visualization in R. The ggrepel package used to label data points.

### An example plot is shown below:
![example plot](https://github.com/agibsonk/Professor-Questionnaire-Response-vis/blob/master/Example%20Plot.png)

Note: Large departments such as biology can create cramped labels, and can make the figure look messy

Future improvements that could be made include switching over to requests along with BeautifulSoup rather than Selenium, which would require less dependencies.
