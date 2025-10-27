import numpy as np
from functools import lru_cache
import copy

#check anyone won
def E(S,k):
    #check rowise win
    for i in range(3):
        for j in range(3):
            if S[i][j]!=k:
                break
        else:
            return 100
     
    #check colwise win
    for j in range(3):
        for i in range(3):
            if S[i][j]!=k:
                break
        else:
            return 100
            
    #check diag top right to left bottom
    for i in range(3):
        if S[i][i]!=k:
            break
    else:
        return 100
      
    #check opposite diag
    i=0
    for j in range(2,-1,-1):
        if S[i][j]!=k:
             break
        i+=1
    else:
        return 100
            
    return 5
    

#print board with coins X and O    
def printS(S):
    for i in range(3):
        print('|',end='')
        for j in range(3):
            if S[i][j]==1:
                print('X',end='')
            elif S[i][j]==2:
                print('O',end='')
            else:
                print(' ',end='')
            print('|',end='')
        print('\n',end='')

#printS(S)

#find the number of empty cells in the board
def emptyC(S):
    c=0
    for i in range(3):
        for j in range(3):
            if S[i][j]==0:
                c+=1
    return c

#generator to give successively empty board positions
def yemptyC(S):
    for i in range(3):
        for j in range(3):
            if S[i][j]==0:
                yield i,j



d={}
#value function with dynamic programming
def V(Sc,k):
    global d

    #for hasing state in dictionary key list to tuple conversion
    St=tuple(tuple(j for j in i) for i in Sc)

    if St in d:
        return d[St]

    c = emptyC(Sc)
    if c==0:
        d[St] = -1,-1
        return d[St],0
    p=1.0/c
    
    max_v=-1
    vl=[]
    #finding value function recursion for all empty cell moves
    for i,j in yemptyC(Sc):
        Sd=copy.deepcopy(Sc)
        Sd[i][j]=k
        vl.append(V(Sd,k)[1])
    
    max_a=-1,-1 
    max_val=-1
    #Bellman equation E is the reward after k move in i,j in State
    for i,j in yemptyC(Sc):
        Sd=copy.deepcopy(Sc)
        Sd[i][j]=k
        
        val=E(Sd,k)+0.8*sum([p*vl[m] for m in range(len(vl))])
        if val>max_val:
            max_val=val
            max_a=i,j
            
    d[St]=max_a,max_val
    #return the best a action place to move coin and maximum value of that state
    return max_a,max_val
    

#shuffle player 1 and 2 codes to change who opens the game
def main():
    #board in list of list with empty 0s
    S=[[0 for _ in range(3)] for _ in range(3)]
    printS(S)

    while emptyC(S)>0:
            
        #RL player marked as 2nd player with k=2    
        while True:
            i = int(input("Enter the position i:"))
            j = int(input("Enter the position j:"))
            if S[i][j]!=0:
                print("Enter different position")
            else:
                break
        S[i][j]=1
        printS(S)
        print("-"*20)
        if E(S,1)==100:
            print("won")
            break
        if emptyC(S)==0:
            break
            
            
        #RL player marked as 1st player with k=1
        (ik,yk),val=V(S,1)
        print("v(s): ",val)
        S[ik][yk]=2
        printS(S)
        print("-"*20)
        if E(S,2)==100:
            print("won")
            break
        if emptyC(S)==0:
            break
            


main()
