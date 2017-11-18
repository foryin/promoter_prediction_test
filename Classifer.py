#!/bin/env python

import random
from sklearn import svm
import numpy as np 

def load_data(file_in):
     FI=open(file_in,'r')
     promoter=[[],[]]
     intron=[[],[]]
     for line in FI:
         if not line.startswith('GC'):
            Line=line.strip().split()
            tag=int(Line[-1])
            feature=map(float,Line[0:-1])
            if tag==1:
               promoter[1].append(tag)
               promoter[0].append(feature)
            else :
                intron[1].append(tag)
                intron[0].append(feature)
     return promoter,intron

def get_data_set(promoter,intron,test_size):
    promoter_len=len(promoter[1])
    intron_len=len(intron[1])
    print(promoter_len)
    print(intron_len)
    promoter_test_index=[]
    intron_test_index=[]
    
    
    for i in range(test_size):
        a=random.randint(0,promoter_len-1)
        while a in promoter_test_index:
              a=random.randint(0,promoter_len-1)
              if a not in promoter_test_index:
                 break
        promoter_test_index.append(a)
        b=random.randint(0,intron_len-1)
        while b in intron_test_index:
              b=random.randint(0,intron_len-1)
              if b not in intron_test_index:
                 break
        intron_test_index.append(b)
    print(promoter_test_index,len(promoter_test_index))
    print(intron_test_index,len(intron_test_index))
    test_feature=[]
    test_tag=[]
    train_feature=[]
    train_tag=[]
    for i in range(test_size):
        test_feature.append(promoter[0][promoter_test_index[i]])
        test_tag.append(promoter[1][promoter_test_index[i]])
        test_feature.append(intron[0][intron_test_index[i]])
        test_tag.append(intron[1][intron_test_index[i]])
    for i in range(promoter_len):
        if i not in promoter_test_index:
           train_feature.append(promoter[0][i])
           train_tag.append(promoter[1][i])
        if i <=intron_len-1 and i not in intron_test_index:
           train_feature.append(intron[0][i])
           train_tag.append(intron[1][i])

    return test_feature,test_tag,train_feature,train_tag
def train_test(train_feature,train_tag,test_feature,test_tag):
    X=np.array(train_feature)
    print(X.shape)
    Y=np.array(train_tag).transpose()
    print(Y.shape)
    clf = svm.SVC()
    fit_result=clf.fit(X, Y)
    print(fit_result)
    sum_test=0
    correct_test=0
    error_test=0
    for i in range(len(test_feature)):
        sum_test=sum_test+1
        X_test=np.array(test_feature[i]).reshape(1,-1)
        #print(X_test.shape)
        pre=clf.predict(X_test)
        #print(pre)          
        if pre[0] == test_tag[i]:
           correct_test=correct_test+1
        else:
            error_test=error_test+1
    return fit_result,sum_test,correct_test,error_test

if __name__=="__main__":
   file_in='/public/home/yinyuan/improvement/MachineLearning/course/01.work/cds.promoter.txt'
   FO=open('/public/home/yinyuan/improvement/MachineLearning/course/01.work/report1.txt','w')
   promoter,intron=load_data(file_in)
   out_line='index\ttest_number\tcorrect_number\terror_number\tcorrect_rate\n'
   FO.write(out_line)
   Sum=0
   Cor=0
   Error=0
   for i in range(5):
       test_feature,test_tag,train_feature,train_tag=get_data_set(promoter,intron,50)
       fit_result,sum_test,correct_test,error_test=train_test(train_feature,train_tag,test_feature,test_tag)
       print(fit_result)
       cor_rate=round(correct_test/float(sum_test),3)
       out_line=str(i+1)+'\t'+str(sum_test)+'\t'+str(correct_test)+'\t'+str(error_test)+'\t'+str(cor_rate)+'\n'
       FO.write(out_line)
       Sum=Sum+sum_test
       Cor=Cor+correct_test
       Error=Error+error_test
   for j in range(5):
        num=50+(j+1)*2
        test_feature,test_tag,train_feature,train_tag=get_data_set(promoter,intron,num)
        fit_result,sum_test,correct_test,error_test=train_test(train_feature,train_tag,test_feature,test_tag)
        print(fit_result)
        cor_rate=round(correct_test/float(sum_test),3)
        out_line=str(i+j+2)+'\t'+str(sum_test)+'\t'+str(correct_test)+'\t'+str(error_test)+'\t'+str(cor_rate)+'\n'
        FO.write(out_line)
        Sum=Sum+sum_test
        Cor=Cor+correct_test
        Error=Error+error_test
   cor_rate=round(Cor/float(Sum),3)
   out_line='total\t'+str(Sum)+'\t'+str(Cor)+'\t'+str(Error)+'\t'+str(cor_rate)+'\n'
   FO.write(out_line)
