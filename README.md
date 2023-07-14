# studious-chatbot
Python ChatBot Project
## Description
This chatbot is a machine learning project executed in python. It takes in a message by the user, then uses the model to predict a tag from the examples. Then prints a message corresponding to the tag.

### Libraries 
I have used tensorflow and keras for backpropagation of error. For analysing data, I have used Bag-of-Words(BoW) model and examples were stored in the .json file. In the .json file, patterns is a feature; label as tag. Then from there the model would spit out any item from the responses array corresponding to that particular tag.

### Directions for use
Clone or download the repository. Run the chatbot.py. You should be able to print a response by feeding in any of the items in 'patterns'. To learn the model, you can edit the intents.json to your preference and start using it to predict by feeding in various strings. Have machine learning!

### Credits
This project is my first attempt into taming the Machine Learning space. I have closely followed the steps and descriptions enumerated in ProjectPro's blog: Python Chatbot Project - Learn to build a chatbot from Scratch. This blog was a helpful guide and I am looking forward to trying more advanced projects on my own.
