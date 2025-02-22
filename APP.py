import numpy as np
import pandas as pd 
import streamlit as st 
import altair as alt
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import Perceptron
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier 
from sklearn.model_selection import RandomizedSearchCV


###########################################################

st.title("Comparator of usual classification models")

st.subheader("Authors:")
st.markdown("Georges RAHAL    \n Yassine BOUKHARI    \n Othmane ESSADDEK     \n    \n Pape ALE FALL")


st.subheader("1. Introduction")

st.markdown("We begin by presenting the dataset, in all the study we are using a unique database of patients history for heart condition with respect to some atributes.  ")
st.markdown("The **target variable** represents the presence **1**, or not **0** of a heart condition")
st.markdown("The **explicative variables** are the following:")
st.markdown("age : *age in years*  \n sex : *(1 = male; 0 = female)*  \n cp : *chest pain type*  \n trestbps : *resting blood pressure (in mm Hg on admission to the hospital)*  \n chol : *serum cholestoral in mg/dl)*  \n fbs : *(fasting blood sugar > 120 mg/dl) (1 = true; 0 = false)*  \n restecg : *resting electrocardiographic results*  \n thalach : *maximum heart rate achieved*  \n exang : *exercise induced angina (1 = yes; 0 = no)*  \n oldpeak : *ST depression induced by exercise relative to rest*  \n slope : *the slope of the peak exercise ST segment*  \n ca : *number of major vessels (0-3) colored by flourosopy*  \n thal : *3 = normal; 6 = fixed defect; 7 = reversable defect*")

st.markdown("We present you the dataset:")
df=pd.read_csv('heart.csv')
st.dataframe(df)

st.subheader("2. Data visualisation")
st.markdown("First, let's explore the distribution conditioning to having or not a heart condition  of the continious variables.   \n We leave the choice for the user.")

##########################################################

variables_continues=['age','chol','trestbps','thalach','oldpeak']

a = pd.get_dummies(df['cp'], prefix = "cp")
b = pd.get_dummies(df['thal'], prefix = "thal")
c = pd.get_dummies(df['slope'], prefix = "slope")

frames = [df, a, b, c]
df_dum = pd.concat(frames, axis = 1)
df_dum = df_dum.drop(columns = ['cp', 'thal', 'slope'])

y = df_dum.target.values
x_data = df_dum.drop(['target'], axis = 1)


####################################

class variable (str):
  
  def __init__(self,str):
    
    if str=='Age':
      self.name='age'
      
    if str=='Cholesterol':
      self.name='chol'
    if str=='Sex':
      self.name='sex'
    if str=='Chest pain':
      self.name='cp'
    if str=='Resting blood pressure':
      self.name='trestbps'
    if str=='Fasting blood sugar':
      self.name='fbs'
    if str=='Resting electrocardiographic results':
      self.name='restecg'
    if str=='Maximum heart rate achieved':
      self.name='thalach'
    if str=='Exercise induced angina':
      self.name='exang'
    if str=='ST depression induced by exercise relative to rest':
      self.name='oldpeak'
    if str=='The slope of the peak exercise ST segment':
      self.name='slope'
      
     
    
class classifieur:#(str):#,par,X_trai,Y_train,X_test,Y_test):
  
  def __init__(self,str):#,par,X_trai,Y_train,X_test,Y_test):
    
    if str=='KNeighbors':
      self.name='KNeighbors'
      self.url="https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html"
      self.algo=KNeighborsClassifier()
      self.grid_param= {"n_neighbors": [k for k in range(1,12)],
             "leaf_size": [k for k in range(1,50)],
             "weights": ["uniform", "distance"],
             "algorithm": ["brute","auto", "ball_tree", "kd_tree"]}
                       
     
    if str=='Logistic Regression':
      self.name = 'Logistic Regression'
      self.url="https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html"
      self.algo= LogisticRegression()
      self.grid_param={'solver':['newton-cg', 'lbfgs', 'liblinear'],
                        'penalty':['none', 'l1', 'l2', 'elasticnet'],
                      'C':[1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]}
      
    if str=='Support Vector Machine Algorithm':
      self.name = 'Support Vector Machine Algorithm'
      self.url="https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html"
      self.algo=SVC(random_state = 1)
      self.grid_param={'C': [0.1, 1.0, 10.0, 100.0, 1000.0],
                       'gamma': [1.0, 0.1, 0.01, 0.001, 0.0001],
                       'kernel': ['rbf','linear']}
      
    if str=='Naive Bayes Algorithm':
      self.name = 'Naive Bayes Algorithm'
      self.url="https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html"
      self.algo=GaussianNB() 
      self.grid_param={}
      
    if str == 'Decision Tree':
      self.name = 'Decision Tree'
      self.url="https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html"
      self.algo = DecisionTreeClassifier()
      self.grid_param = {'criterion':['gini','entropy'], 
                         'max_depth':[k for k in range(2,25)]}
      
    if str == 'Random Forest':
      self.name = 'Random Forest'
      self.url="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html"
      self.algo = RandomForestClassifier()
      self.grid_param={"n_estimators": [k for k in range(50,150)],
                       "criterion": ["gini", "entropy"],
                       "min_samples_split": [k for k in range(2,12)]}
      
    if str == 'Perceptron':
      self.name = 'Perceptron' 
      self.url="https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html"
      self.algo = Perceptron(tol=1e-3, random_state=0)
      self.grid_param={"penalty": ["l2","l1","elasticnet"],
                      "l1_ratio": [k/20 for k in range(1,20)]}     
    
    if str=='Extra Trees':	
      self.name = 'Extra Trees'
      self.url="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html"
      self.algo=ExtraTreesClassifier()
      self.grid_param={"n_estimators": [k for k in range(50,150)],
                       "criterion": ["gini", "entropy"],
                       "min_samples_split": [k for k in range(2,12)]}
    
    if str == 'XGBoost':
      self.name = 'XGBoost'
      self.url="https://xgboost.readthedocs.io/en/stable/python/python_api.html"
      self.algo = XGBClassifier()
      self.grid_param={"booster": ["gbtree", "gblinear", "dart"]}
    
    if str == 'Adaboost':
      self.name = 'Adaboost'
      self.url="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html"
      self.algo = AdaBoostClassifier(n_estimators=50, random_state=0)
      self.grid_param={"n_estimators": [k for k in range(20,100)],
                       "learning_rate": [k/20 for k in range(1,20)],
                       "algorithm": ["SAMME", "SAMME.R"]}
      
  def train_classifieur(self,X_train,Y_train):
    self.algo.fit(X_train,Y_train)
 

  def zones_erreur(self,X_train, X,Y_train, y,i):
    #renvoie la liste contenant les zones où le classifieur s'est trompé
    self.train_classifieur(X_train,Y_train)
    erreurs = list(abs(self.algo.predict(X) - y))
    zones_err =[i*(erreurs[k]==1) for k in range(len(y))] #[k for k in range(len(erreurs)) if erreurs[k] == 1]
    return zones_err, [k for k in range(len(y))]
  
  
  
  def get_feature(self):
    #Get features avec Random forest
# from sklearn.feature_selection import RFE
# from sklearn.linear_model import LogisticRegression
# rfe_selector = RFE(estimator=LogisticRegression(), n_features_to_select=num_feats, step=10, verbose=5)
# rfe_selector.fit(X_norm, y)
# rfe_support = rfe_selector.get_support()
# rfe_feature = X.loc[:,rfe_support].columns.tolist()
# print(str(len(rfe_feature)), 'selected features')
    return self.algo.get_feature
  
  
#   def get_parametrs(self):
#     param=self.param_deflt
#     return(param)
  
  def scor_classifieur(self,X_test,Y_test):
    return(self.algo.score(X_test,Y_test)*100)


################################ 

#Data visualisation
      
      
var = st.radio(
     "What is the variable that you choose?  ",
     ('Age', 'Cholesterol','ST depression induced by exercise relative to rest','Resting blood pressure','Maximum heart rate achieved'))

var_target=pd.crosstab(df[variable(var).name],df.target)

dicvar=var_target.to_dict()
dfvar=pd.concat({k: pd.Series(v) for k, v in dicvar.items()}).reset_index()
dfvar.columns = ['0_1', 'level','variable']


gp_chartvar = alt.Chart(dfvar).mark_bar().encode(
  alt.Column('0_1'), alt.X('level'),
  alt.Y('variable', axis=alt.Axis(grid=False)), 
  alt.Color('0_1'))

 
st.altair_chart(gp_chartvar, use_container_width=False)
 
  
st.markdown("Now, let's try to see if there exists some correlation between the choosen two variables at each time with respect to having or not a heart condition. ")
var1 = st.radio(
     "What is the first variable that you choose?  ",
      ('Age', 'Cholesterol','ST depression induced by exercise relative to rest','Resting blood pressure','Maximum heart rate achieved'))

var2 = st.radio(
     "What is the second variable that you choose?  ",
     ('Cholesterol','Age','ST depression induced by exercise relative to rest','Resting blood pressure','Maximum heart rate achieved'))

 
scater_var1_var2=alt.Chart(df).mark_point().encode(
    x=variable(var1).name,
    y=variable(var2).name,
    color=alt.Color('target',  scale=alt.Scale(scheme='dark2'),legend=alt.Legend(title="age VS chol"))
)

st.altair_chart(scater_var1_var2, use_container_width=False)

###################################################################

st.subheader("3. Preprocessing Data")
st.markdown("We can see that some of our explicative variables (*'cp', 'thal' and 'slope'*) are categorical, we'll turn them into dummy variables. ")
st.markdown("For the continious variables, since the notion of distance is used to do the classification, we dont want to influence the algorithm by an important discrepancy between the variables we will normalise/standardise them as the folowing")
st.latex(r'''
     X_{sta}=\frac{X-\mathbb{E}[X]}{sd[X]}
     ''')
st.latex(r'''
     X_{nor}=\frac{X-min(X)}{max(X)-min(X)}
     ''')
###################################################################

processing = st.radio(
                      "How would you like to preprocess the dataset ?",
                      ("None", "Normalised", "Standardised"))

if processing == "None":
  x = x_data.copy()
  
elif processing == "Normalised":
  x = x_data.copy()
  x=(x_data - np.min(x_data)) / (np.max(x_data) - np.min(x_data)).values
  
elif processing == "Standardised":
  x =x_data.copy()
  for n in variables_continues:
    x[n]=(x[n]-np.mean(x[n]))/np.std(x[n])
    
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2,random_state=0)  

###################################################################

st.subheader("4. Choice of the classifier")
st.markdown("In this section we are going to explore the algorithm of your choice   ")
scoreList = []
#testdicc =st.slider( "For the parameter:",step= 11.5,min_value=0.0, max_value=100.98,value=10.5) 
Model=st.radio(
     "What is the model you want to use for the classification? ",
     ('KNeighbors','Logistic Regression','Support Vector Machine Algorithm','Naive Bayes Algorithm','Decision Tree','Extra Trees', 'Random Forest', 'Perceptron', 'XGBoost','Adaboost'))


st.markdown("At first hand, one may choose an arbitrary selection for the model's parameters and see how it performs. ")
st.markdown ("**Remark :** The score of the choosen model depends also on one's choice in the data processing section.")

####################################################################

choix_classifieur=classifieur(Model)
dicc={}
dic_cont={}
for k in choix_classifieur.grid_param.keys():
  l=choix_classifieur.grid_param[k]
  if (isinstance(l[0],int) or isinstance(l[0],float)):
    l.sort()
    dic_cont[k]=l
    #dicc[k]=choix_classifieur.grid_param[k][0]
    dicc[k] =st.slider( f"For the parameter: {k}",step= (l[1]-l[0]),min_value=l[0], max_value=l[-1],value= l[-1]) 
  else:
    dicc[k]=st.radio(f"For the parameter: {k}",l)
  
    
#user_input = st.text_input("You can plug in the parametr you want", 5)
#choix_classifieur
choix_classifieur.algo.set_params(**dicc)

choix_classifieur.train_classifieur(x_train,y_train)


st.write("The precision of the ",Model," model is :", choix_classifieur.scor_classifieur(x_test,y_test))

st.markdown("Now, we are going to show a graph that may help tuning the model with better parameters. It's a kind of grid search on the numerical parameters, but one parametr at a time. ")

choice_svsparam = st.radio("Do you wish to see the score versus the numerical parameters graph ?",
                           ('No','Yes'))

if choice_svsparam == 'Yes':
  for (k,u) in dic_cont.items():
    N_mean = 5
    params_mean = np.zeros(len(u))
    for n in range(N_mean):
      
      params = []
      for par in u:
        
        params_m=dicc.copy()
        params_m[k]=par
        modl = choix_classifieur.algo.set_params(**params_m)  
        modl.fit(x_train, y_train)
        #tree3.score(X_test, y_test)
        params.append(modl.score(x_test, y_test))
        
      params_mean += np.array(params)
    error={k:u,'score': 1/N_mean*params_mean}
    df_err=pd.DataFrame.from_dict(error, orient='columns', dtype=None, columns=None)
    base=alt.Chart(df_err)
    line11o = base.mark_line(color='#8A2BE2').encode(
        x=k,
        y='score',)
    st.altair_chart(line11o, use_container_width=True)
  
else:
  pass
  
                   



st.markdown("From sklearn we can use some methods that can help tune our models")  
      

grid=st.radio("Do you wish to use the GridSearchCV or  RandomizedSearchCV to tune your model ?",
                           ('No','GridSearchCV','RandomizedSearchCV'))

if grid=='GridSearchCV':
  search = GridSearchCV(choix_classifieur.algo,choix_classifieur.grid_param)
  result = search.fit(x_train, y_train)
  st.write("The precision of the tuned model using GridSearchCV is :",100*result.best_score_)
 
elif grid=='RandomizedSearchCV':
  search =RandomizedSearchCV(choix_classifieur.algo,choix_classifieur.grid_param)
  result = search.fit(x_train, y_train)
  st.write("The precision of the tuned model using RandomizedSearchCV is :",100*result.best_score_)

  
else:
  pass
# search = GridSearchCV(choix_classifieur.algo,choix_classifieur.grid_param)#, scoring='accuracy', n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1) #, scoring='accuracy', n_jobs=-1, cv=cv)
# #search =RandomizedSearchCV(choix_classifieur.algo,choix_classifieur.grid_param)#, n_iter = 100, cv = 20, verbose=2, random_state=1, n_jobs = -1)
# result = search.fit(x_train, y_train)
# st.write("The precision of the tuned model using grid searsh is :",100*result.best_score_)
st.markdown("**Use tip** : Please click on No and None in the past section in order to optimize the performance of the app.")
#############################################################################

st.subheader("5. Prediction error comparison for the models")
st.markdown("The objective of this section is to see if the models misclassify for the same individuals. The test will be done on $ X_{test}=(X_i)_{i\leq N} $ and $ Y_{test}=(y_i )_{i\leq N} $.    \n We will show the graphes of the folowing fonctions: $f_k:\{1,...,N\} \longrightarrow \{0,k\}$ ")

st.latex(r'''
     f_{k}(i)=k\mathbb{1}_{\{C_k(X_i)\neq y_i\}}
     ''')
st.markdown("Where,")
st.latex(r'''
     k\in\{1,2,3\} , \text{ the k-th classification model } C_k()\text{ . And } i\leq N \text{ the i-th individual}
     ''')
option = st.multiselect('Select the three models you want to compaire :', ['KNeighbors','Logistic Regression','Support Vector Machine Algorithm','Naive Bayes Algorithm','Decision Tree','Extra Trees', 'Random Forest', 'Perceptron', 'XGBoost','Adaboost'])
st.write(option)  
  
if len(option)==3:
  st.write("You have finished choosing ")
  algo1=classifieur(option[0])
  algo2=classifieur(option[1])
  algo3=classifieur(option[2])
  algos = [algo2, algo3]
  df_err1=pd.DataFrame()
  erreur1,X_plot1 = algo1.zones_erreur(x_train, x_test,y_train, y_test,1)
  df_err1[algo1.name] =  erreur1
  df_err1['X_plot1']=X_plot1
  #df_err.columns =['X']
  i = 2
  #st.dataframe(df_err)
  for a in algos:
    #a.train_classifieur(x_train, y_train)
    erreurs,X_plot = a.zones_erreur(x_train, x_test,y_train, y_test,i)
    df_err1[a.name] =  erreurs
    df_err1[f"X_plot{i}"]=X_plot
    i += 1
  #st.dataframe(df_err1)  
  
  basez=alt.Chart(df_err1)
  line1 = basez.mark_line(color='#458B00').encode(
        x='X_plot1',
        y=algo1.name,)
  line2 = basez.mark_line(color='#8A2BE2').encode(
        x='X_plot2',
        y=algo2.name,)
  line3 = basez.mark_line(color='#E3CF57').encode(
        x='X_plot3',
        y=algo3.name,)
  st.altair_chart(line1+line2+line3, use_container_width=True)
    


  dferpl=df_err1.drop(columns=['X_plot1', 'X_plot2','X_plot3'])
  st.dataframe(dferpl) 
 
  
  

