using CSV
using DataFrames 

x = CSV.read("/Volumes/GoogleDrive/My Drive/Research2020/MyPoker/modelTrain/x2.csv"; header=false);
convert(DataFrame,x);

y = CSV.read("/Volumes/GoogleDrive/My Drive/Research2020/MyPoker/modelTrain/y2.csv"; header=false);
y = y[:,1];

grid = IAI.GridSearch(IAI.OptimalTreeClassifier(random_seed=1,),max_depth=15,cp=0)

IAI.fit!(grid, x, y)

IAI.score(grid, x, y, criterion=:misclassification)

a = IAI.get_learner(grid)

a

IAI.write_json("/Users/alexpaskov/Downloads/treetest.json",a)

b = IAI.read_json("/Users/alexpaskov/Downloads/treetest.json")

IAI.get_learner(grid)
