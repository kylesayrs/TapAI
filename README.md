# TapAI
Game where you and a partner have to communicate while avoiding a wiretapping AI

## TODO: Usage

## TODO: Setup Guide

## Web Interface Setup
To run the game in the web interface:
1. Install Node.js and npm (https://nodejs.org/en/download/)
2. Clone this repository if you haven't already: `git clone https://github.com/kylesayrs/TapAI.git`
3. Go to web interface folder: `cd TapAI/web_interface`
5. Go to the server folder, run `npm i`, and then start the server with `npm run dev`
6. Open another terminal window, go to the client folder, run `npm i`, and then start the client with `npm start`
7. Go to `http://localhost:8080`

The web app is also live at https://tapai.herokuapp.com.

## Data Collection
Here are a few card sets along with relevant data sources
* Animals
    * Wikipedia
* ATLA Characters
    * Wikipedia
    * Avatar Wiki
* Food
    * Wikipedia
    * Amazon fine food reviews
* Products
    * Wikipedia
    * Amazon reviews
    * Home depot product search relevance
* Slang
    * Wikipedia
    * Urban dictionary words and definitions

## TODO: Preprocessing

## Models
| Model Name          | Status | Difficulty (1-5)
| --------------------|:------:|:-------:|
| Naive Embeddings    |   🟢   |    1    |
| Naive Bayes         |   🟡   |    2    |
| SVM                 |   🔴   |   (2)   |
| Logistic Regression |   🔴   |   (2)   |
| 1D Convolution      |   🔴   |   (3)   |
| RNN                 |   🔴   |   (3)   |
| LSTM                |   🔴   |   (4)   |
| BERT                |   🔴   |   (4)   |
| GPT2                |   🔴   |   (5)   |
| GPT3 (api)          |   🔴   |   (5)   |
| GAN Approach        |   🔴   |   (?)   |

## TODO: Results

## Authors
Kyle Sayers
Jimmy Maslen
