# Professor-Questionnaire-Response-vis
Visualization of average response scores through SQCT questionnaire data created using R.
Data was scraped from SQCT website using a Python script to create a CSV. I used Selenium for scraping the data rather than Requests due to the website requiring a password.  

Repository includes the Python file used to scrape SQCT, an R script for plotting the data, and an example dataset and plot generated using both

The python script requries a valid UWO username and password due to this, and also requries a Selenium chrome webdriver.exe to work.

This project was used as an opportunity to practise data scraping using Python and data vis in R. The ggrepel package used to label data points.

Note: Large departments such as biology can create cramped labels, and can make the figure look messy

Future improvements that could be made include switching over to requests along with BeautifulSoup rather than Selenium, which would require less dependencies.
