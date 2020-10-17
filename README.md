### Quick overview ###
I've decided to practice my knowledge of Keras on some real case from [Kaggle](https://www.kaggle.com/c/mercedes-benz-greener-manufacturing)

I've downloaded all data from this competition and set myself a task: `create a NN that can predict Y column (test time of each car) from train.csv file`

- First of all, I've preprocessed the data. Normalized it.
- Then I've created a hand-made NN of 3 layers with dropout and trained it
- After that I've used a Keras Tuner to let it find a better solution for the net architecture. 
- Also drew some graphs of Y distribution, calculated the correlation coefficient and compared true and predicted values

(sorry for Russian comments)


