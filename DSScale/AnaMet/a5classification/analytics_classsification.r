#Practical Predictive Analitycs, Models and Methods
#--------------------------------------------------
#UW - Bill Howe
#----------

library(caret); library(kernlab); 


## Step 1: Read and summarize the data
data <- read.csv(file="/media/sf_as/Dropbox/files/DSScale/AnaMet/a5classification/seaflow_21min.csv", header=TRUE, sep=",")

library(caret); library(kernlab); 


## Step 1: Read and summarize the data
data <- read.csv(file="/media/sf_as/Dropbox/files/DSScale/AnaMet/a5classification/seaflow_21min.csv", header=TRUE, sep=",")
summary(data)

# frequency over seconds
hist(data$time)

#frequency over column values
hist(data$pe)
hist(data$fsc_big)

# counts for each output value
table(data$pop)


## Step 2: Split the data into test and training sets
# file_id, time, cell_id, d1, d2, fsc_small, fsc_perp, fsc_big, pe, chl_small, chl_big, pop

trainIndex = createDataPartition(y = data$pop, 
                    times = 1, list = FALSE,
                    p = 0.5)

train <- data[ trainIndex,]
test  <- data[-trainIndex,]
dim(train); dim(test);
mean(train$time)


## Step 3: Plot the data
# Plot pe against chl_small and color by pop
featurePlot(x=train[,c('chl_small', 'pe')], 
            y=train$pop,
            plot='pairs')

library(ggplot2)
#qplot(x=chl_small, y= pe, data=data, fill=as.factor(pop))
ggplot(data, aes(chl_small, pe, color=pop))+geom_line()


##Step 4: Train a decision tree.
library(rpart)
fol <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
model <- rpart(fol, method="class", data=train)
print(model)



#Step 5: Evaluate the decision tree on the test data.
pred5 <- predict(model, newdata=test,type="class")
table(test$pop, pred5)

mean(test$pop==pred5)



#Step 6: Build and evaluate a random forest.
library(randomForest) 
model <- randomForest(fol, data=train)
pred6 <- predict(model, newdata=test,type="class")
table(test$pop, pred6)

mean(test$pop==pred6)

importance(model)


## Step 7: Train a support vector machine model and compare results.
library(e1071)
model <- svm(fol, data=train)
pred7 <- predict(model, newdata=test,type="class")
table(test$pop, pred7)

mean(test$pop==pred7)


##Step 8: Construct confusion matrices
table(pred5, test$pop)

table(pred6, test$pop)

table(pred7, test$pop)


## Step 9: Sanity check the data
hist(data$fsc_small)
hist(data$fsc_big)
hist(data$chl_big)

plot(data$time,data$chl_big)

# Remove this data from the dataset by filtering out all data associated with file_id 208, then repeat the experiment for all three methods, making sure to split the dataset into training and test sets after filtering out the bad data.
#----------------------------------------------------------------------------------------------------------
data2=data[data$file_id!=208,]

ind2 <- createDataPartition(y=data2$pop, p=0.5, list=F)
train2 <- data2[ind2,]
test2  <- data2[-ind2,]

model2 <- rpart(fol, method="class", data=train2)
pred25  <- predict(model2, newdata=test2,type="class")
mean(test2$pop==pred25) - mean(test$pop==pred5)


model2 <- rpart(fol, method="class", data=train2)
pred26  <- predict(model2, newdata=test2,type="class")
mean(test2$pop==pred26)
mean(test$pop==pred6)


model2 <- svm(fol, data=train2)
pred27 <- predict(model2, newdata=test2,type="class")
table(test$pop, pred27)
mean(test$pop==pred27)

#15. The variables in the dataset were assumed to be continuous, but one of them takes on only a few discrete values, suggesting a problem. Which variable exhibits this problem?
hist(data$fsc_big)

