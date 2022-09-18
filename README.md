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
| Feature Extractor | Model Name | Status | Performance (1-5) |
| ----------------- | -----------|:------:|:-----------------:|
| Tfidf         | Naive Bayes         |   🟢   |    1    |
| Avg Tokenizer | Cosine Similarity   |   🟡   |    2    |
| Tfidf         | Logistic Regression |   🔴   |   (2)   |
| Tokenizer     | 1D Convolution      |   🔴   |   (3)   |
| Tokenizer     | LSTM                |   🔴   |   (4)   |
| Tokenizer     | Zero Shot Bert MNLI |   🔴   |   (4)   |
| Tokenizer     | Bert                |   🔴   |   (4)   |
| Tokenizer     | Bert Pretrained MLM |   🔴   |   (4)   |
| Tokenizer     | Zero Shot GPT2      |   🔴   |   (5)   |
| Tokenizer     | Zero Shot GPT3      |   🔴   |   (5)   |

## TODO: Results

## Authors
Kyle Sayers
Jimmy Maslen
