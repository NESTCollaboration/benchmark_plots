from pylab import *             # includes numpy
import scipy.io
from scipy.optimize import minimize # for fitting
from scipy.interpolate import NearestNDInterpolator
from numpy.random import normal
import json
from copy import deepcopy

def load_ER_data():
    with open('ER_yields_data.dat','r') as f:
        d=json.load(f)
    return(d)

def load_ER_data_array():
    with open('ER_yields_data.dat','r') as f:
        d=json.load(f)
    
    for dname in d.keys():
        for fname in d[dname]['data'].keys():
            d[dname]['data'][fname]['field']=array(d[dname]['data'][fname]['field'])
            d[dname]['data'][fname]['energy']=array(d[dname]['data'][fname]['energy'])
            d[dname]['data'][fname]['energy_pm']=array(d[dname]['data'][fname]['energy_pm'])
            d[dname]['data'][fname]['QY']=array(d[dname]['data'][fname]['QY'])
            d[dname]['data'][fname]['QY_pm_sys']=array(d[dname]['data'][fname]['QY_pm_sys'])
            d[dname]['data'][fname]['QY_pm_stat']=array(d[dname]['data'][fname]['QY_pm_stat'])
            
        
    return(d)

def lighten_color(color, amount=1):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    ret=colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])
    ret=list(ret)
    for ii,r in enumerate(ret):
        if r<0:
            ret[ii]=0
        if r>1:
            ret[ii]=1
    return tuple(ret)

def plot_dataset_field(ax,d,dname,fname,c=1):
    field=array(d[dname]['data'][fname]['field'])
    E=array(d[dname]['data'][fname]['energy'])
    E_pm=array(d[dname]['data'][fname]['energy_pm'])
    QY=array(d[dname]['data'][fname]['QY'])
    QY_pm_sys=array(d[dname]['data'][fname]['QY_pm_sys'])
    QY_pm_stat=array(d[dname]['data'][fname]['QY_pm_stat'])


    ax.errorbar(E,QY,yerr=QY_pm_sys+QY_pm_sys,xerr=array(E_pm),
             fmt=d[dname]['mstyle'],
             color=lighten_color(d[dname]['mcolor'],c),
             markersize=d[dname]['msize'],
             label=d[dname]['label']+' ({:d} V/cm)'.format(int(field))
            )

    return()




def plot_field_range(ax,d,field_low,field_high,interp_field=-1):
    for dname in d.keys():
        if (dname=='PIXeY_37Ar')&(interp_field>0):
            QY,QY_pm=interp_PIXeY(interp_field)
            errorbar(0.27,QY,yerr=QY_pm,
                 fmt=d[dname]['mstyle'],
                 color=lighten_color(d[dname]['mcolor'],0.5),
                 markersize=d[dname]['msize'],
                 label=d[dname]['label']+' interp ({:d} V/cm)'.format(int(interp_field))
                )
        elif (dname=='Doke_976')&(interp_field>0):
            QY,QY_pm=interp_Doke(interp_field)
            errorbar(976,QY,yerr=QY_pm,
                 fmt=d[dname]['mstyle'],
                 color=lighten_color(d[dname]['mcolor'],0.5),
                 markersize=d[dname]['msize'],
                 label=d[dname]['label']+' interp ({:d} V/cm)'.format(int(interp_field))
                )
        else:
            c=1
            for fname in d[dname]['data'].keys():
                field=array(d[dname]['data'][fname]['field'])
                if (field<=field_high)&(field>=field_low):
                    plot_dataset_field(ax,d,dname,fname,c)
                    c+=0.5
                    if c>1.5:
                        c=0.5
            
        
        
    return()

def add_flucts(d):
    ### Returns a new dict with thesame structure as the data dict, but with fluctuations added.
    df=deepcopy(d) # copys data dict
    
    for dname in df.keys():#loop over datasets
        for fname in df[dname]['data'].keys():#loop over fields
            ## Start with the field.
            N=normal() #draw from standard normal distribution
            # Fluctuate field according to uncertainty. Reflect the value at 0.
            df[dname]['data'][fname]['field']=abs(df[dname]['data'][fname]['field']+
                                                  N*df[dname]['data'][fname]['field_pm'])

            ## Move on to energy
            N=normal() # draw from standard normal distribution
            tmp=array(df[dname]['data'][fname]['energy']) #make energy into array
            # check if energy has asymmetric errors
            if shape(df[dname]['data'][fname]['energy_pm'])==(len(df[dname]['data'][fname]['energy']),):
                # add symmetric fluctuations
                tmp+=N*array(df[dname]['data'][fname]['energy_pm'])
            elif shape(df[dname]['data'][fname]['energy_pm'])==(2,len(df[dname]['data'][fname]['energy'])):
                # add asymmetric fluctuations
                if N<0:
                    tmp+=N*array(df[dname]['data'][fname]['energy_pm'][0])
                else:
                    tmp+=N*array(df[dname]['data'][fname]['energy_pm'][1])
            else:
                print('bad error shape')
            tmp[tmp<0]=-tmp[tmp<0] # reflect negative energy around 0
            df[dname]['data'][fname]['energy']=tmp.tolist() # relistify
            
            ## Systematic fluctuations
            N=normal()# draw from standard normal distribution
            tmp=array(df[dname]['data'][fname]['QY']) # arrayify
            # check if QY has asymmetric errors
            if shape(df[dname]['data'][fname]['QY_pm_sys'])==(len(df[dname]['data'][fname]['QY']),):
                # add symmetric fluctuations
                tmp+=N*array(df[dname]['data'][fname]['QY_pm_sys'])
            elif shape(df[dname]['data'][fname]['QY_pm_sys'])==(2,len(df[dname]['data'][fname]['QY'])):
                # add asymmetric fluctuations
                if N<0:
                    tmp+=N*array(df[dname]['data'][fname]['QY_pm_sys'][0])
                else:
                    tmp+=N*array(df[dname]['data'][fname]['QY_pm_sys'][1])
            else:
                print('bad error shape')
            tmp[tmp<0]=-tmp[tmp<0] # reflect negative QY around 0
            
            ## Statistical fluctuations
            # Using existing QY array
            N=normal(size=len(df[dname]['data'][fname]['QY'])) # Draw array of normal random variables
            # check if QY has asymmetric errors
            if shape(df[dname]['data'][fname]['QY_pm_stat'])==(len(df[dname]['data'][fname]['QY']),):
                # Add symmetric fluctuations
                df[dname]['data'][fname]['QY']=(array(df[dname]['data'][fname]['QY'])+
                                            normal()*array(df[dname]['data'][fname]['QY_pm_stat'])).tolist()
            elif shape(df[dname]['data'][fname]['QY_pm_stat'])==(2,len(df[dname]['data'][fname]['QY'])):
                # Add asymmetric fluctuations
                tmp[N<0]+=(N*array(df[dname]['data'][fname]['QY_pm_stat'][0]))[N<0]
                tmp[N>=0]+=(N*array(df[dname]['data'][fname]['QY_pm_stat'][1]))[N>=0]
            else:
                print('bad error shape')
            tmp[tmp<0]=-tmp[tmp<0] #reflect negative QY around 0


            df[dname]['data'][fname]['QY']=tmp.tolist() #relistify QY

    return(df)

def single_chi2(d,model,dname,fname):
    field=array(d[dname]['data'][fname]['field'])
    E=array(d[dname]['data'][fname]['energy'])
    E_pm=array(d[dname]['data'][fname]['energy_pm'])
    QY=array(d[dname]['data'][fname]['QY'])
    QY_pm_sys=array(d[dname]['data'][fname]['QY_pm_sys'])
    QY_pm_stat=array(d[dname]['data'][fname]['QY_pm_stat'])


    ## Calculate total uncertainty
    QY_p=zeros_like(QY)
    QY_m=zeros_like(QY)
    # check if energy has asymmetric errors
    if shape(E_pm)==(len(E),):
        # Calculate QY uncertainty due to symmetric energy errors
        QY_p=sqrt(QY_p**2+((model(E-E_pm,field)-model(E+E_pm,field))/2)**2)
        QY_m=sqrt(QY_m**2+((model(E-E_pm,field)-model(E+E_pm,field))/2)**2)
    elif shape(E_pm)==(2,len(E)):
        # Calculate QY uncertainty due to asymmetric energy errors. 
        dQY=model(E+E_pm[1],field)-model(E,field)
        QY_p[dQY>=0]=sqrt(QY_p[dQY>=0]**2+dQY[dQY>=0]**2)
        QY_m[dQY<0]=sqrt(QY_m[dQY<0]**2+dQY[dQY<0]**2)

        dQY=model(E-E_pm[0],field)-model(E,field)
        QY_p[dQY>=0]=sqrt(QY_p[dQY>=0]**2+dQY[dQY>=0]**2)
        QY_m[dQY<0]=sqrt(QY_m[dQY<0]**2+dQY[dQY<0]**2)
    else:
        print('bad error shape')
        return(-1)


    # check if QY has asymmetric systematic errors
    if shape(QY_pm_sys)==(len(QY),):
        # Calculate QY uncertainty due to symmetric systematic errors
        QY_p=sqrt(QY_p**2+QY_pm_sys**2)
        QY_m=sqrt(QY_m**2+QY_pm_sys**2)
    elif shape(QY_pm_sys)==(2,len(QY)):
        # Calculate QY uncertainty due to asymmetric systematic errors
        QY_p=sqrt(QY_p**2+QY_pm_sys[1]**2)
        QY_m=sqrt(QY_m**2+QY_pm_sys[0]**2)
    else:
        print('bad error shape')
        return(-1)

    # check if QY has asymmetric statistical errors
    if shape(QY_pm_stat)==(len(QY),):
        # Calculate QY uncertainty due to symmetric statistical errors
        QY_p=sqrt(QY_p**2+QY_pm_stat**2)
        QY_m=sqrt(QY_m**2+QY_pm_stat**2)
    elif shape(QY_pm_stat)==(2,len(QY)):
        # Calculate QY uncertainty due to asymmetric statistical errors
        QY_p=sqrt(QY_p**2+QY_pm_stat[1]**2)
        QY_m=sqrt(QY_m**2+QY_pm_stat[0]**2)
    else:
        print('bad error shape')
        return(-1)

    dQY=QY-model(E,field)
    chi2=dQY**2/QY_p**2
    chi2[dQY<0]=dQY[dQY<0]**2/QY_p[dQY<0]**2
    return(chi2)


# def min_func(p,d,NEST_QY,field_low=-1,field_high=999999999.,
#              skip_sets=['neriX_Compton: 190_Vcm','neriX_Compton: 480_Vcm'],
#              interp_field=-1
#             ):
#     model=lambda x,y:NEST_QY(x,y,*p)
#     chi2_all=array([])
#     for dname in d.keys():
#         if (dname=='PIXeY_37Ar')&(interp_field>0):
#             QY,QY_pm=interp_PIXeY(interp_field)
#             chi2_all=append(chi2_all,(model(0.27,interp_field)-QY)**2/QY_pm**2)
#         elif (dname=='Doke_976')&(interp_field>0):
#             QY,QY_pm=interp_Doke(interp_field)
#             chi2_all=append(chi2_all,(model(976.,interp_field)-QY)**2/QY_pm**2)
#         else:
#             for fname in d[dname]['data'].keys():
#                 field=d[dname]['data'][fname]['field']
#                 if ((field>=field_low)&(field<=field_high)&
#                     (not (dname+': '+fname) in skip_sets)):
#                     chi2=single_chi2(d,model,dname,fname)
#                     chi2_all=append(chi2_all,chi2/len(chi2))

#     return(sum(chi2_all)/len(chi2_all))   


def min_func(p,d,NEST_QY,field_low=-1,field_high=999999999.,
             skip_sets=['neriX_Compton: 190_Vcm','neriX_Compton: 480_Vcm'],
             interp_field=-1
            ):
    model=lambda x,y:NEST_QY(x,y,*p)
    chi2_all=array([])
    weight_sum=0
    num_sets=0
    for dname in d.keys():
        if (dname=='PIXeY_37Ar')&(interp_field>0):
            QY,QY_pm=interp_PIXeY(interp_field)
            chi2_all=append(chi2_all,(model(0.27,interp_field)-QY)**2/QY_pm**2)
        elif (dname=='Doke_976')&(interp_field>0):
            QY,QY_pm=interp_Doke(interp_field)
            chi2_all=append(chi2_all,(model(976.,interp_field)-QY)**2/QY_pm**2)
        else:
            for fname in d[dname]['data'].keys():
                field=d[dname]['data'][fname]['field']
                if ((field>=field_low)&(field<=field_high)&
                    (not (dname+': '+fname) in skip_sets)):
#                     print((dname+': '+fname))
                    weight=d[dname]['data'][fname]['fitting_weight']
                    chi2=single_chi2(d,model,dname,fname)*weight
                    chi2_all=append(chi2_all,chi2/len(chi2))
                    num_sets+=1
                    weight_sum+=weight

    return(sum(chi2_all)/len(chi2_all))   

def interp_PIXeY(field):
    QY=log10(field)*2.24+70.83
    return(QY,(6.**2+(QY-76.82)**2)**0.5)

def interp_Doke(field):
    a,b,c,d= 63.21119076, 37.35157016,  2.04762949,  3.63625523
    QY=a-(b/(1+(log10(field+1)/c)**d))
    QY_pm=QY*0.08

    return(QY,QY_pm)




def NESTv2_QY(energy,dfield,
            plow0,
            plow1,
            plow2,
            plow3,
            pmed1,
            pmed2,
            pmed3,
            pmed4,
            QyLvlhighE,
            pDB1,
            pDB2,
            pDB3,
            pDB4,
            m3,
            m4,
            m9,
           ):
    density=2.87
    Wq_eV=1.9896 + (20.8 - 1.9896) / (1. + pow(density / 4.0434, 1.4407));
    
#     QyLvllowE = 1e3/Wq_eV+plow1*(1.-1./(1.+pow(dfield/plow2,plow3)));
    QyLvllowE = plow0+plow1*(1.-1./(1.+pow(dfield/plow2,plow3)));
    
    QyLvlmedE =pmed1-pmed1/(1.+pow(dfield/(pmed2*exp(density/pmed3)),pmed4));
    
    DokeBirks = pDB1+(pDB2-pDB1)/(1.+pow(dfield/pDB3,pDB4));
    
    LET_power = -2.;

    Qy = (QyLvlmedE+(QyLvllowE-QyLvlmedE)/pow(1.+m3*pow(energy,m4),m9)+
          QyLvlhighE/(1.+DokeBirks*pow(energy,LET_power)))
    
    return(Qy)

def NESTv2_parms():
    return([
        73,#plow0
        6.5,#plow1
        47.408,#plow2
        1.9851,#plow3
        32.988,#pmed1
        0.026715,#pmed2
        0.33926,#pmed3
        0.6705,#pmed4
        28.,#QyLvlhighE
        1652.264,#pDB1
        1.415935e10,#pDB2
        0.02673144,#pDB3
        1.564691,#pDB4
        1.304,#m3
        2.1393,#m4
        0.35535,#m9
        ])



           
           


