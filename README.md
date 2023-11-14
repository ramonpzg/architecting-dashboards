# Architecting Dashboards

Welcome to Architecting Dashboards, a tutorial where we will be learning about how to deconstruct static 
and dynamic dashboards and put new ones together; how to save dashboards for the purpose of sharing them 
with colleagues and friends, and how to share our insights in a deployed version of our interactive dashboards.

# Table of Contents


1. Outline for the Tutorial
2. Prerequisites
3. Goals/Learning Outcomes
4. Setup
6. Data
9. Resources

## 1. Outline for the Tutorial

The time budgeted for this tutorial is about 3.5 hours including breaks. The tutorial will follow, as best as possible, the following schedule.
1. **Introduction and Setup**
   - Getting the environment set up. We will be using Jupyter Lab and some of the libraries in the Python scientific stack throughout the tutorial. If you experience any difficulties getting the setup going, please let me know as soon as possible. Otherwise, you can also access all of the content through Binder using the following link and we can work on your setup during one of the breaks.
   - Presentation including
     - A breakdown of the session
     - Introduction to DataViz
     - Introduction to Dashboards
     - Intro to the tools for the session
2. **5-minute break**
3. **Static Dashboards**
   - The Dashboard
   - Scenario
   - Use Cases
   - The Data
   - Top-Down Static Dashboard Breakdown
   - Exercise (7-min)
4. **10-minute break**
5. **Interactive Dashboards**
   - The Dashboard
   - Scenario
   - Use Cases
   - The Data
   - Top-Down Interactive Dashboard Breakdown
   - Exercise (7-min)
6. **15-minute break**
5. **Live Machine Learning Dashboards**
8. **Deploying Dashboard**


## 2. Prerequisites (P) and Good To Have's (GTH)

- **(P)** Attendees for this tutorial are expected to be familiar with Python (1 year of coding). 
- **(P)** Participants should be comfortable with loops, functions, lists comprehensions, and if-else statements.
- **(GTH)** While it is not necessary to know pandas, NumPy, bokeh, and Holoviews, a bit of experience with these libraries would be very beneficial throughout this tutorial.
- **(P)** Participants should have at least 6 GB of free memory in their computers.
- **(GTH)** While it is not required to have experience with an integrated development environment like Jupyter Lab, this would be very beneficial for the session


## 3. Goals/Learning Outcomes

It is okay not to understand everything in the tutorial, instead, I would like to challenge you to 
first, make sure you walk away with at least 2 new concepts from this lesson, and second, that you 
come back to it and go over the content you did not get the first time around and reinforce your understanding of it.

With that said, by the end of the tutorial you should be able to:

1. Introduce an accessible way to reproduce dashboards
2. Help you find a process for looking at data visualizations and figure out a way to break them down and reproduce them
3. Create static dashboards that you can share with friends and colleagues
4. Create interactive dashboards that your users can use to see different stories from the data

## 4. Setup

You should first make sure you have [Anaconda](https://www.anaconda.com/products/individual#download-section) 
or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed. This will allow you to have most of 
the packages you will need for this tutorial already installed once you open up Jupyter Lab.

Here are some of the ways in which you can get the setup for the tutorial ready.

#### First Step

Open up your terminal and navigate to a directory of your choosing in your computer. Once there, run the following command.

```sh
 git clone https://github.com/ramonprz01/architecting-dashboards.git
```

Conversely, you can click on the green `download` button at the top and download all files to your desired folder/directory. Once you download it, unzip it and move on to the second step.

#### Second Step

To get all dependencies, packages and everything else that would be useful in this tutorial, you can recreate the environment by first going into the directory for today

```sh
cd architecting-dashboards
```

and then running

```sh
mamba env create -f environment.yml
# or
conda env create -f environment.yml
```

#### Third Step

Then you will need to activate your environment using the following command.

```sh
conda activate pycon-d4a
```

#### Fourth Step

Open up Jupyter Lab and you should be ready to go.

```sh
jupyter lab
# or
code .
```

Navigate to notebook 01 and open it.


## 5. Data

For this tutorial, we will be using the following datasets.

- Domain’s Melbourne Housing Market

![inside_airbnb](images/kaggle_melb_auctions.png)

This dataset contains information about housing auctions from 2016 to 2017 in the metropolitan area of Melbourne, Victoria, Australia. The data was scraped from Domain, a popular properties solutions website.

- Sydney Airbnb Data

![inside_airbnb](images/inside_airbnb.png)

We will be using Airbnb data collected by a scraping tool called [Inside Airbnb](http://insideairbnb.com/about.html). The 
tool periodically scrapes data from Airbnb and publishes it for free on its website.

The data differs slightly (or by a lot) from country to country, and from time-frame to time-frame. Neither fact 
should be surprising, the former might be due to different countries having different regulations that may or may 
not prevent Airbnb from posting the same information regarding a listing. The latter makes sense as we would expect 
Airbnb to continue to improve its business from year to year and change the information collected from a listing and its host.

You can download all datasets using the following link.

Create a folder called `data` and add to it the folders in the following link using their respective names, `static` and `interactive`. Please make sure to add this new directory to the same folder you will be using for this tutorial.

### [LINK to the Data](https://web.tresorit.com/l/fk31I#ojoRDOFvtbWXSxiAmSF1sw)


## 9. Additional Resources

Here are a few great resources to get started with data analytics, data visualization, and dashboard creation. The first three, in particular, have guided my thinking and helped very much polish the content you have found in this tutorial.

- [Fundamentals of Data Visualisation](https://clauswilke.com/dataviz/) by Claus O. Wilke
- [The Big Book of Dashboards](http://bigbookofdashboards.com/) by Steve Wexler, Jeffrey Shaffer, and Andy Cotgreave
- [Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython](https://www.amazon.com/gp/product/1491957662/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=quantpytho-20&creative=9325&linkCode=as2&creativeASIN=1491957662&linkId=ea8de4253cce96046e8ab0383ac71b33) by Wes McKinney