import numpy as np

# def EWT_LocalMaxMin_change(f, N, fm=None):
#     import numpy as np

def EWT_LocalMaxMin_change(f, N, fm=None):
    locmax = np.zeros_like(f)
    if fm is not None:
        f2 = fm
    else:
        f2 = f.copy()
    locmin = np.full_like(f2, fill_value=np.max(f2))
    for i in range(1, len(f) - 1):
        if f[i - 1] < f[i] and f[i] > f[i + 1]:
            locmax[i] = f[i]
        
        if f2[i - 1] > f2[i] and f2[i] < f2[i + 1]:
            locmin[i] = f2[i]    
    
    X = 1.1
    m = 0
    Threshold = 3.2
    Imax_dummy = len(f) * X / 30.0
    cnt = 1
    flag = True
    if N != -1:
        N = N - 1
        N2 = []
        Imax = np.argsort(locmax)[::-1]
        lmax = np.sort(locmax)[::-1]
        if locmax[Imax[0]] >= 3:
            Threshold = 3.5
        else:
            Threshold = 3.5
        
        for s in range(len(f)):
            if Imax[s] <= Imax_dummy and flag and lmax[s] > Threshold:
                
                m += 1
            elif lmax[s] > Threshold:
                N2.append(s)
                cnt += 1
            else:
                flag = False
        
        N = m + len(N2)
        if len(locmax) > N:
            Imax = np.sort(Imax[:N])
        else:
            Imax = np.sort(Imax)
            N = len(lmax)
        bound = np.zeros(N)
        for i in range(N):
            if i == 0:
                a = 1
            else:
                a = Imax[i - 1]
            lmin = np.sort(locmin[a:Imax[i]])
            ind = np.argsort(locmin[a:Imax[i]])
            if len(lmin) > 0:tmp = lmin[0]
            n = 1
            
            if n < len(lmin):
                n = 2
                while n < len(lmin) and tmp == lmin[n]:
                    n += 1
            
            if np.ceil(n / 2) < len(ind): bound[i] = a + ind[np.ceil(n / 2).astype(int)-1]
        
        Z = 2
        default = int(2 * len(f) * Z / 100.0)
        if(i+1 >= len(bound)):bound = np.append(bound, Imax[-1] + default)
        else:bound[i + 1] = Imax[-1] + default
        Y = 20
        if(i+2 >= len(bound)):bound = np.append(bound,int(len(f) * Y / 30.0))
        else: bound[i + 2] = int(len(f) * Y / 30.0)
        if bound[0] == 0 and Imax[0] == 1:
            bound = bound[1:]
        return bound
    
    else:
        bound = []
        k = 0
        for i in range(len(locmin)):
            if locmin[i] < np.max(f2):
                bound.append(i - 1)
                k += 1
        return bound
