# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 11:34:51 2018

@author: gni
"""
c=[[None for i in range(10)] for i in range (10)]
def LCS(x,y,i,j):    
    if c[i][j] != None:
        return c[i][j]
    if i < 0 or j < 0:
        return 0
    if x[i] == y[j]:
        c[i][j]=LCS(x,y,i-1,j-1)+1
    else:
        c[i][j]=max(LCS(x,y,i-1,j),LCS(x,y,i,j-1))
    return c[i][j]

value = [1,2,4,6,7,10,13]
sub=[]

#def add_sub(total, v_list, index):
#    if total == 0:
#        print sub
#        return
#    if index < 0:
#        return
#    if total >= v_list[index]:
#        sub.append(v_list[index])
#        add_sub(total-v_list[index], v_list, index-1)
#        if sub:
#            sub.pop()
#        add_sub(total, v_list, index-1)
#    else:
#        add_sub(total,v_list, index -1)


def add_sub1(total, v_list, index):
    global sub
    if total == 0:
        print sub
        return
    if index >= len(v_list):
        return
    if total >= v_list[index]:
        sub.append(v_list[index])
        add_sub1(total-v_list[index],v_list, index + 1)
        if sub:
            sub.pop()
        add_sub1(total, v_list, index + 1)


if __name__ == '__main__':
#    x="BDCABA"
#    y="ABCBDAB"
#    i = len(x)-1
#    j = len(y)-1
#    print LCS(x,y,i,j)
#    add_sub(10,value,len(value)-1)
    add_sub1(10, value,0)
    