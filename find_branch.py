import numpy as np
def find_branch(frac_pos):
    branch = []
    branch_new = []
    all = []
    first_node = frac_pos[0]
    all.append(first_node)
    for j in range(np.size(frac_pos)):
        d = np.abs(first_node-frac_pos[j])
        if d==1 or d==10 or d==9 or d==11:
            branch.append(frac_pos[j])


    while branch!=[]:
        for i in range(np.size(branch)):
            for j in range(np.size(frac_pos)):
                for k in range(np.size(all)):
                    if all[k]==frac_pos[j]:
                        pass
                    else:
                        d = np.abs(branch[i]-frac_pos[j])
                        if d==1 or d==10 or d==9 or d==11:
                            branch_new.append(frac_pos[j])
            all.append(branch[i])
        branch = branch_new
        print(branch)
        branch_new = []
    return all