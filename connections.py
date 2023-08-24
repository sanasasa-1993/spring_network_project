def connections(X,Y):
    cx=[]
    cy=[]
    for i in range (0,X):
        for j in range(0,Y-1):
            index_i= i*Y+j
            index_j= i*Y+(j+1)
            cx.append(index_i)
            cy.append(index_j)	
    for i in range (0,X-1):
        for j in range(0,Y):
            index_i= i*Y+j
            index_j= (i+1)*Y+j
            cx.append(index_i)
            cy.append(index_j)
    for i in range(0,X-1):
        for j in range(0,Y-1):
            index_i= i*Y+j
            index_j= (i+1)*Y+(j+1)
            cx.append(index_i)
            cy.append(index_j)
    for i in range(0,X-1):
        for j in range(0,Y-1):
            index_i= (i+1)*Y+j
            index_j=i*Y+(j+1)
            cx.append(index_i)
            cy.append(index_j)	    
    return cx , cy