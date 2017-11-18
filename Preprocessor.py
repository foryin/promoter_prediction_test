#!/bin/env python

import re



def get_good_kmer(kmer_dict):
    """get the most frequent kmer"""
    max_count=0
    sum_kmer=0
    for kmer in list(kmer_dict.keys()):
        sum_kmer=sum_kmer+1
        if kmer_dict[kmer]== max_count:
           max_kmer.append(kmer)
        if kmer_dict[kmer] > max_count:
           max_kmer=[]
           max_kmer.append(kmer)
           max_count=kmer_dict[kmer]
    
    return max_kmer,max_count,sum_kmer

def get_kmer(seq,k,kmer_dict):
    """get kmer"""
    for j in range(len(seq)-k+1):
        kmer=seq[j:j+k]
        if kmer not in list(kmer_dict.keys()):
           kmer_dict[kmer]=1
        else :
           kmer_dict[kmer]=kmer_dict[kmer]+1
    return kmer_dict

class Seq(object):
    """Sequence"""
    def __init__(self,id,seq,tag):
        self.id=id
        self.seq=seq
        self.tag=tag
    def calculate_GC_precent(self,seq):
        length=float(len(seq))
        j=0
        for i in seq:
            if i=='C' or i=='G':
               j=j+1
            else:
                next
        GC_P=round(j/length,3)
        return GC_P
    def calculate_kmer_percent(self,seq,good_kmer,k):
        length=len(seq)+k-1
        j=0
        for i in range(length):
            kmer=seq[i:i+k]
            if kmer==good_kmer:
               j=j+1
            else:
                next
        kmer_P=round(j/float(length),3)
        return kmer_P


def preprocessor(type_list,dir_in):
    """data preprocessing,reformat(many line to one line), remove record including Ns, calculate kmer frequency"""
    Sequence=[]
    Good_kmers=[]
    
    for type in type_list:
        kmer3_dict={}
        kmer4_dict={}
        FI=open(dir_in+'/'+type+'.raw.txt')
        #print(type)
        if type=='promoter':
           tag=1
        else:
            tag=0
        i=0
        for line in FI:
            #print(line)
            if line.startswith('>'):
               if i==0:
                  ID='_'.join(line.strip()[1:].split())
                  Seq=''
                  i=i+1
                  next
               else :
                   if re.search(r'.*N.*',Seq):
                      ID='_'.join(line.strip()[1:].split())
                      Seq=''
                      next
                   else :
                       Sequence.append([ID,Seq,tag])
                       kmer3_dict=get_kmer(Seq,3,kmer3_dict)
                       kmer4_dict=get_kmer(Seq,4,kmer4_dict)
                       ID='_'.join(line.strip()[1:].split())
                       Seq=''
            else:
                Seq=Seq+line.strip()
                next
       # print(kmer_dict)
        good_kmer3=get_good_kmer(kmer3_dict)
        good_kmer4=get_good_kmer(kmer4_dict)
        print(good_kmer3)
        print(good_kmer4)
        Good_kmers.extend(good_kmer3[0])
        Good_kmers.extend(good_kmer4[0])
        #print(Good_kmers)
    return Sequence,Good_kmers

def get_input_data(Sequence,Good_kmers):
    
    Tags=[]
    Features=[]
    for rec in Sequence:
        ID=rec[0]
        seq=rec[1]
        tag=rec[2]
        Tags.append(tag)
        features=[]
        a_seq=Seq(ID,seq,tag)
        GC=a_seq.calculate_GC_precent(seq)
        features.append(GC)
        for kmer in Good_kmers:
            k=len(kmer)
            kmer_freq=a_seq.calculate_kmer_percent(seq,kmer,k)
            features.append(kmer_freq)
        Features.append(features)
    return Features,Tags
            
if __name__=="__main__":
   list_type=['intron','promoter']
   dir_in='/public/home/yinyuan/improvement/MachineLearning/course/00.data'
   Sequence,Good_kmers=preprocessor(list_type,dir_in)
   Features,Tags=get_input_data(Sequence,Good_kmers)
   FO=open('/public/home/yinyuan/improvement/MachineLearning/course/01.work/cds.promoter.txt','w')
   length=len(Tags)
   out_line='\t'.join(Good_kmers)
   out_line='GC\t'+out_line+'\ttag\n'
   FO.write(out_line)
   for i in range(length):
       out_line='\t'.join(map(str,Features[i]))+'\t'+str(Tags[i])+'\n'
       FO.write(out_line)
#print(Features)
#   print(Good_kmers)
   #print(Tags)
