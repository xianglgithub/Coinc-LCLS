

import numpy as np

def EngMo(traw,xraw,yraw,t0,x0,y0,to,particle):
    
    try:
        if particle=='N1': 
            EngXY, MoX, MoY = EngMoXY_N1(traw,xraw,yraw,t0,x0,y0,to)  
            EngTof, MoTof = EngMoTof_N1(traw,xraw,yraw,t0,x0,y0,to)
            Eng = EngXY + EngTof 
        elif particle=='N2':        
            EngXY, MoX, MoY = EngMoXY_N2(traw,xraw,yraw,t0,x0,y0,to)  
            EngTof, MoTof = EngMoTof_N2(traw,xraw,yraw,t0,x0,y0,to)  
            Eng = EngXY + EngTof 
        elif particle=='N3':        
            EngXY, MoX, MoY = EngMoXY_N3(traw,xraw,yraw,t0,x0,y0,to)  
            EngTof, MoTof = EngMoTof_N3(traw,xraw,yraw,t0,x0,y0,to)  
            Eng = EngXY + EngTof 
        elif particle=='N4':        
            EngXY, MoX, MoY = EngMoXY_N4(traw,xraw,yraw,t0,x0,y0,to)  
            EngTof, MoTof = EngMoTof_N4(traw,xraw,yraw,t0,x0,y0,to)  
            Eng = EngXY + EngTof 
        elif particle=='2N1':        
            EngXY, MoX, MoY = EngMoXY_2N1(traw,xraw,yraw,t0,x0,y0,to)  
            EngTof, MoTof = EngMoTof_2N1(traw,xraw,yraw,t0,x0,y0,to)
            Eng = EngXY + EngTof 
            
                                                   
    except Exception as e:
        print ('Error when calculating Pxy_N4: {0}'.format(e))   
        EngXY = 10000
        EngTof = 10000     
        Eng = 10000
        MoX = 10000
        MoY = 10000
        MoTof = 10000                        
 #   print 'EngMo:',EngXY, EngTof, Eng, MoX, MoY, MoTof
 #   print 'raw:',traw,xraw,yraw,t0,x0,y0,to,particle
 #   print 'radius:',np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    return Eng, MoX, MoY, MoTof
        
 
def EngMoXY_N1(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    x = [radius,traw/1000.0]
    px_ratio = (xraw-x0)/radius
    py_ratio = (yraw-y0)/radius
 #   sign = np.sign(x-x0)
 #   x = np.abs(x-x0)    
    b= 1774.90995942
    rc1= 4.73559686923
    rc2= -0.0251360312745
    rc3= 3.96003855519e-06
    rc4= -5.84570981899e-08
    rc5= 1.03690654844e-09
    rtc1= -0.86427667844
    rtc2= 0.00178376370634
    rdtc1= -6.47576693404
    rdtc2= 0.163701149146
    tmc1= -166.001080119
    tmc2= 1244.57237119
    tmc3= -268.421489496
    tc1= -2592.7550567
    tc2= 996.291769456
    tc3= 12.8212380112
    tc4= -73.0448008663
    tc5= 10.4293058247
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+tc4*x[1]**4+tc5*x[1]**5)
    if E<0:
        E=10000  
    pxy = np.sqrt(2*1836*14*E/27.2)
    return E, px_ratio*pxy, py_ratio*pxy
    
def EngMoTof_N1(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    sign = -np.sign(traw-t0)    
    x = [radius,traw/1000.0]
    
    tof0= 2.8408
    b= 0.199254783351
    rc1= -12.6957903238
    rc2= -0.00453652677426
    rc3= -0.000213179354773
    rc4= 5.95799085659e-06
    rc5= -7.65590553371e-08
    rc6= 3.11679220005e-10
    rc7= 8.0002717475e-13
    rtc1= 2.18220911056
    rtc2= 0.00102296917826
    rdtc1= 18.3704723878
    rdtc2= 2.21178702261e-05
    tmc1= -931323.583995
    tmc2= 1822419.66882
    tmc3= -152.797482577
    tc1= -2.23188057731
    tc2= 930.737923973
    tc3= -12052.9223192
    tc4= 4.87405444387
    tc5= 14531.3971683
    tc6= -7077.48577773
    tc7= 938.892453372   
       
    
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rc6*x[0]**6+rc7*x[0]**7+
            rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+
            tc4*x[1]**4+tc5*x[1]**5+tc6*x[1]**6+tc7*x[1]**7)
    if E<0:
        E=10000  

    return E,sign*np.sqrt(2*1836*14*E/27.2)   
    
def EngMoXY_N2(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    x = [radius,traw/1000.0]
    px_ratio = (xraw-x0)/radius
    py_ratio = (yraw-y0)/radius
 #   sign = np.sign(x-x0)
 #   x = np.abs(x-x0)    
    
    b= 79.0971057092
    rc1= 5.23414586655
    rc2= -0.0208781198478
    rc3= 1.63928333574e-06
    rc4= 2.76351167101e-08
    rc5= 8.81948624461e-10
    rtc1= -1.34520278243
    rtc2= 0.00322919213324
    rdtc1= -5.08540542405
    rdtc2= 0.109203363334
    tmc1= 46.9017991427
    tmc2= -869.858021708
    tmc3= 711.423296983
    tc1= 373.798553429
    tc2= -371.748711732
    tc3= 114.86946874
    tc4= -5.83404751403
    tc5= -1.88214921026  
      
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+tc4*x[1]**4+tc5*x[1]**5)
    if E<0:
        E=10000  
    pxy = np.sqrt(2*1836*14*E/27.2)
    return E, px_ratio*pxy, py_ratio*pxy
    
def EngMoTof_N2(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    sign = -np.sign(traw-t0)    
    x = [radius,traw/1000.0]  
    
    tof0= 2.00875
    b= 1.53057327658
    rc1= 1.37885137933
    rc2= -0.153321889814
    rc3= -1.48448694327e-05
    rc4= 2.92651001766e-06
    rc5= -1.2396970503e-07
    rc6= 2.17087569758e-09
    rc7= -1.38065422397e-11
    rtc1= -0.391656317292
    rtc2= 0.0206188643065
    rdtc1= -1.17945960241
    rdtc2= 0.281282121847
    tmc1= -1432217.5291
    tmc2= -159.690014945
    tmc3= 2286590.06379
    tc1= -18901.2729018
    tc2= 55652.1511678
    tc3= 102055.185296
    tc4= 32742.1695997
    tc5= -26200.7962466
    tc6= -18357.993782
    tc7= 7176.09415842
      
    
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rc6*x[0]**6+rc7*x[0]**7+
            rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+
            tc4*x[1]**4+tc5*x[1]**5+tc6*x[1]**6+tc7*x[1]**7)
    if E<0:
        E=10000  

    return E,sign*np.sqrt(2*1836*14*E/27.2)       
    
def EngMoXY_N3(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    x = [radius,traw/1000.0]
    px_ratio = (xraw-x0)/radius
    py_ratio = (yraw-y0)/radius
 #   sign = np.sign(x-x0)
 #   x = np.abs(x-x0)    
    
    b= -366.735406174
    rc1= 3.53783653614
    rc2= 0.00214753020431
    rc3= 1.35815527508e-06
    rc4= 7.26670542994e-08
    rc5= 9.8957065265e-10
    rtc1= -1.11707358273
    rtc2= 0.000691242830414
    rdtc1= -2.79725510499
    rdtc2= 0.0668212103686
    tmc1= 1237.18819276
    tmc2= 93.6501294447
    tmc3= -752.693231386
    tc1= -531.532435147
    tc2= 216.888693143
    tc3= -26.4616597017
    tc4= 55.0981658444
    tc5= -20.6775874015
        
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+tc4*x[1]**4+tc5*x[1]**5)
    if E<0:
        E=10000  
    pxy = np.sqrt(2*1836*14*E/27.2)
    return E, px_ratio*pxy, py_ratio*pxy
    
def EngMoTof_N3(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    sign = -np.sign(traw-t0)    
    x = [radius,traw/1000.0] 
    
    tof0= 1.64013
    b= -10.186378546
    rc1= -1.26602491063
    rc2= 1.21917295755
    rc3= -0.00237974457539
    rc4= 0.000169708133633
    rc5= -6.17559810329e-06
    rc6= 1.09983093138e-07
    rc7= -7.59731840713e-10
    rtc1= 0.375031103607
    rtc2= -0.222248217361
    rdtc1= 0.996234752058
    rdtc2= -1.62748069965
    tmc1= 280388.721955
    tmc2= 30137.1565494
    tmc3= 331085.076246
    tc1= -564935.389169
    tc2= -236879.321657
    tc3= 46861.1794613
    tc4= 489809.301149
    tc5= -164.957023676
    tc6= -253248.472791
    tc7= 77900.5039324
    
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rc6*x[0]**6+rc7*x[0]**7+
            rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+
            tc4*x[1]**4+tc5*x[1]**5+tc6*x[1]**6+tc7*x[1]**7)
    if E<0:
        E=10000  

    return E,sign*np.sqrt(2*1836*14*E/27.2)     
    
def EngMoXY_N4(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    x = [radius,traw/1000.0]
    px_ratio = (xraw-x0)/radius
    py_ratio = (yraw-y0)/radius
 #   sign = np.sign(x-x0)
 #   x = np.abs(x-x0)    
    
    b= -216.09400834
    rc1= 3.15382510798
    rc2= 0.0154753039496
    rc3= 8.73093881899e-07
    rc4= 1.3002103833e-07
    rc5= 9.18122318635e-10
    rtc1= -1.14764874837
    rtc2= -0.0021641307284
    rdtc1= -2.16405855581
    rdtc2= 0.0552119210309
    tmc1= -572.863385146
    tmc2= 960.882591065
    tmc3= -420.917028375
    tc1= 383.16111656
    tc2= -123.322013226
    tc3= -67.7368881536
    tc4= 73.4238610471
    tc5= -19.054905383
      
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+tc4*x[1]**4+tc5*x[1]**5)
    if E<0:
        E=10000  
    pxy = np.sqrt(2*1836*14*E/27.2)
    return E, px_ratio*pxy, py_ratio*pxy
    
def EngMoTof_N4(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    sign = -np.sign(traw-t0)    
    x = [radius,traw/1000.0] 
    
    tof0= 1.4204
    b= -36.6439747028
    rc1= 270.666895575
    rc2= -1.58347904991
    rc3= -1.06624018448e-05
    rc4= 2.37715896665e-06
    rc5= -1.00232768621e-07
    rc6= 1.66886485363e-09
    rc7= -9.68899044003e-12
    rtc1= -95.7722747995
    rtc2= 0.402835970584
    rdtc1= -191.21759686
    rdtc2= 1.55415014382
    tmc1= -1688966.41465
    tmc2= -11280.8850539
    tmc3= 1378805.03014
    tc1= 282.151866662
    tc2= -9667.11848929
    tc3= 708726.823451
    tc4= 8.6936725184
    tc5= 12279.0840006
    tc6= -416361.823425
    tc7= 175736.44707
    
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rc6*x[0]**6+rc7*x[0]**7+
            rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+
            tc4*x[1]**4+tc5*x[1]**5+tc6*x[1]**6+tc7*x[1]**7)
    if E<0:
        E=10000  

    return E,sign*np.sqrt(2*1836*14*E/27.2)       
    
def EngMoXY_2N1(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    x = [radius,traw/1000.0]
    px_ratio = (xraw-x0)/radius
    py_ratio = (yraw-y0)/radius
 #   sign = np.sign(x-x0)
 #   x = np.abs(x-x0)    
    
    b= -78.4901503469
    rc1= 4.73262783819
    rc2= -0.0251452338313
    rc3= 3.97093489479e-06
    rc4= -5.8626135575e-08
    rc5= 1.03784967457e-09
    rtc1= -0.610764374471
    rtc2= 0.000892158603641
    rdtc1= -9.15217516732
    rdtc2= 0.327473886629
    tmc1= 2020.19942916
    tmc2= -701.217548507
    tmc3= 928.94098029
    tc1= -284.602350342
    tc2= -253.004474699
    tc3= 198.464049407
    tc4= -43.5685098642
    tc5= 3.16510385821
        
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+tc4*x[1]**4+tc5*x[1]**5)
    if E<0:
        E=10000  
    pxy = np.sqrt(2*1836*28*E/27.2)
    return E, px_ratio*pxy, py_ratio*pxy
    
def EngMoTof_2N1(traw,xraw,yraw,t0=0,x0=0,y0=0,to=0):
    
    radius = np.sqrt((xraw-x0)**2+(yraw-y0)**2)
    traw -= to
    sign = -np.sign(traw-t0)    
    x = [radius,traw/1000.0]  
    
    tof0= 4.01749
    b= -4.04299894741
    rc1= 0.481385274472
    rc2= 0.00028153235923
    rc3= -0.00019111106657
    rc4= 4.3878078484e-06
    rc5= -4.42358229223e-08
    rc6= 1.00146389288e-10
    rc7= 6.94453514831e-13
    rtc1= -0.101887222967
    rtc2= 0.000367693585177
    rdtc1= -0.426379182161
    rdtc2= -0.0362139187189
    tmc1= 1.31881146257
    tmc2= -1551.23935837
    tmc3= 1899063.86679
    tc1= 144.003079259
    tc2= -166.963653237
    tc3= -14325.8061489
    tc4= -730.612631986
    tc5= 4686.72371786
    tc6= -1380.70591282
    tc7= 117.955254843
    
    E = (b+rc1*x[0]+rc2*x[0]**2+rc3*x[0]**3+rc4*x[0]**4+rc5*x[0]**5+rc6*x[0]**6+rc7*x[0]**7+
            rtc1*x[0]*x[1]+rtc2*(x[0]*x[1])**2+
            rdtc1*(x[0]/x[1])+rdtc2*(x[0]/x[1])**2+tmc3*x[1]**(-3)+
            tmc2*x[1]**(-2)+tmc1*x[1]**(-1)+tc1*x[1]+tc2*x[1]**2+tc3*x[1]**3+
            tc4*x[1]**4+tc5*x[1]**5+tc6*x[1]**6+tc7*x[1]**7)
    if E<0:
        E=10000  

    return E,sign*np.sqrt(2*1836*28*E/27.2)               
    
    
    
   

        
