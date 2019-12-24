# -*- coding: UTF-8 -*-
#####################################################################
#                                                                   #  
#            MCNP MCTL file Analsis file Part 2                     #
#    Plot tally data from  extrcated txt files by mctalextractor.py #        
#                                                                   #   
#                                     by:czj 2019.12.18             #
#####################################################################


import mctalextrcator
import numpy as np
import re
import os 
import datetime
import matplotlib.pyplot as plt
import argparse

#mctal_filename = "mctal.2cm_colli_concrete.1211.s5mx"

def main():
    parser = argparse.ArgumentParser()
    parser.description = "Plot mctal/extracted data txt files, please enter two parameters: 'mctalfile' and 'tally-N' or 'data_txt'"
    parser.add_argument("-f", "--file", help="this is mctalfile", dest="mctalfile", type=str, default="none")
    parser.add_argument("-ft", "--filetxt", help="this is mctalfile with extracted data files", dest="mctaltxt", type=str, default="none")
    parser.add_argument("-dt", "--filedata", help="this is extracted data txt", dest="datatxt", type=str, default="none")
    parser.add_argument("-n", "--tallyN", help="this is ntally number", dest="tallyN", type=int, default="0")
    parser.add_argument("-a", "--pltall", help="plot all tally data", dest="plotAll", type=str, default="none")
    args = parser.parse_args()
    print("parameter f  is :",args.mctalfile)
    print("parameter ft is :",args.mctaltxt)
    print("parameter dt is :",args.datatxt)
    print("parameter n  is :",args.tallyN)
    print("parameter a  is :",args.plotAll)
    if args.mctalfile != "none" and args.mctaltxt == "none" and args.datatxt == "none":
        mctal_filename = args.mctalfile
        tally_number = args.tallyN
        if args.tallyN != 0 and args.plotAll == "none":
            datatxt = mctaldata2tmp(mctal_filename, tally_number)
            plot_EVR_array(datatxt, tally_number)
        elif args.tallyN == 0 and args.plotAll == "none":
            print(" Try to plot all tally data from ", args.mctalfile)
            #tal_list = mctalextractor.read_tal_list(mctal_filename)
            #for tal_n in tal_list:
            #    datatxt = mctaldata2tmp(mctal_filename, tal_n)
            #    plot_EVR_array(datatxt, tal_n)
            print("Done nothing yet!")
        else:
            print("  Please input tally number '-n N' or '-a'")
    elif args.mctalfile == "none" and args.mctaltxt != "none" and args.datatxt == "none":
        print("  Please use -f parametr instead")
    elif args.mctalfile == "none" and args.mctaltxt == "none" and args.datatxt != "none":
        if args.tallyN == "none":
            plot_EVR_array(args.datatxt)
        else:
            plot_EVR_array(args.datatxt, args.tallyN)
    else:
        print("  Input parameters confused, please check it again! ")



#  Method 1: read mctalfile and pull out tally data

def logtxt(txt):
    with open('MCNP_plot.log', 'a+') as log:
        time_str = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        log_txt = time_str + '  :  ' + str(txt) 
        log.write(log_txt)
        log.write("\n")

def rmtmp(tmp_name):
    print('------------------------------------------------------------------------\n')
    if(os.path.exsists(tmp_name)):
        os.remove(tmp_name)
        print(tmp_name,", removed.")
        log_txt = tmp_name + ", removed."
        logtxt(log_txt)
    else:
        print(tmp_name,", not exsist!")
        log_txt = tmp_name + ", not sxsist."
        logtxt(log_txt)
    print('------------------------------------------------------------------------\n')

def mctaldata2tmp(mctal_filename, tally_number):
    E_Val,Val_list,ValR_list,tallyN_total = mctalextrcator.read_tallyN_data(mctal_filename, tally_number)
    tmp_name = mctal_filename + ".F" + str(tally_number) + '.tmp' 
    with open(tmp_name, "w+") as f_tmp:
        for i in range(len(E_Val)):
            f_tmp.write(str(E_Val[i])),     f_tmp.write('    ')
            f_tmp.write(str(Val_list[i])), f_tmp.write('    ')
            f_tmp.write(str(ValR_list[i])), f_tmp.write('\n')
    print('------------------------------------------------------------------------\n')
    print('  Tally %d writed to file: %s\n' %(tally_number,tmp_name))
    log_txt = "  Data write to tmp file: " + tmp_name 
    logtxt(log_txt)
    #print('------------------------------------------------------------------------\n')
    return tmp_name

#mctaldata2tmp(mctal_filename, 32)

#  Method 2: read mctal_filename , and check extracted data txt file if exsist

def read_data_txt_list(mctal_filename, tally_number):
    file_name_list= os.listdir('.')
    plot_tally_str = 'tal_F' + str(tally_number) + '_' + mctal_filename  
    data_flist = []  
    for fn in file_name_list:
        if re.search(plot_tally_str, fn):
            data_flist.append(fn)
    if len(data_flist) == 0:
        print("------------------------------------------------------------------------\n")
        print('  file %s not exsist, please check it again\n' %plot_tally_str)
        print("------------------------------------------------------------------------\n")
    elif len(data_flist) > 1:
        print("------------------------------------------------------------------------\n")
        for f in data_flist:
            print(f)
        print('  Warning: Too many extrcted data txt files')
        print("  Please specify  operation parameter '-t' or '-a'")
        print("------------------------------------------------------------------------\n")
    else:
        print("  R" %str(data_flist[0]))
    #print(file_name_list)
    #print(data_flist)
    return data_flist
#read_data_txt(mctal_filename, 32)   


#  Method 3: read data file derctaly from extracted data txt name

#txt_name ='tal_F32_mctal.2cm_colli_concrete.1211.s5mxD15_19_07.txt'

def data2array(txt_name):
    with open(txt_name, 'r') as data_txt:
        data_line_list = data_txt.readlines()   
        line_len = len(data_line_list)
        #print('line_len: %d' %line_len)
        if data_txt: 
            E_list = []
            Val_list = []
            R_list = []
            for line in data_line_list:
                line_list_str = line.split()
                line_list_float = list(map(float,line_list_str))
                #print(line_list_float)
                E_list.append(line_list_float[0])
                Val_list.append(line_list_float[1])
                R_list.append(line_list_float[2])    
            data_list = [E_list, Val_list, R_list]
            #print(E_list)
            #print(data_list[0:1])            
        else:
            print('  Error: data2array, file: %s, not exsit!' %txt_name)
    
        EVR_arrary = np.array(data_list, dtype=np.float32)
        EVR_arrary_T = EVR_arrary.T
        #print(EVR_arrary_T.shape)
        #print(EVR_arrary_T.ndim)
        #print(EVR_arrary_T[0,:])
        #print(EVR_arrary_T[:,0])
        return EVR_arrary_T

#data2array(txt_name)

def array_info(txt_name, tally_number = 0 ):
    EVR = data2array(txt_name)
    print("------------------------------------------------------------------------\n")
    print(" Tally F%d data info:" %tally_number)
    print(" file: %s" %txt_name)
    print('   E: %.5e to %.5e' %(EVR[1,0], EVR[-1,0]))
    #print('Vals: %.4e to %.4e' %(EVR[0,1], EVR[-1,1]))
    print('   bin number: %.2d' %(EVR.size))
    sum_col = EVR.sum(axis=0)
    max_col = np.amax(EVR, axis=0)
    min_col = np.amin(EVR, axis=0)
    #max_col = EVR.max()
    #print(type(max_col))
    #print(max_col)
    print('   Total Vals: %.5e' %sum_col[1])
    print('     Max  Val: {:.5e}, Min  Val:{:.5e} '.format(max_col[1],min_col[1]))
    print("------------------------------------------------------------------------\n")
    return  EVR[1,0], EVR[-1,0], max_col[1], min_col[1], sum_col[1]
#array_info(txt_name)

def plot_EVR_array(txt_name, tally_number):
    E_min, E_max, Val_max, Val_min, Val_total = array_info(txt_name, tally_number)
    EVR_arr = data2array(txt_name)
    E = EVR_arr[:,0]
    Vals = EVR_arr[:,1]
    R = EVR_arr[:,2]
    Vals_nonzero_index = np.nonzero(Vals)
    Vals_nonzero = Vals[Vals_nonzero_index]
    E_nonzero = E[Vals_nonzero_index]
    #print(Vals.shape)
    #print(Vals_nonzero[100:120])
    #print(E_nonzero[0:20])
    if tally_number != 0:
        fig_title = txt_name[0:-4] + " F" + str(tally_number)
        fig_legend = "F" + str(tally_number)
    else:
        fig_title = txt_name[0:-4]
        fig_legend = "Val"
    plt.title(fig_title)
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.plot(E_nonzero,Vals_nonzero)
    plt.xlim([E_min,E_max*1.1]), plt.ylim([Val_min,Val_max*1.2])
    plt.xlabel('E (MeV)'), plt.ylabel('count')
    print(fig_legend)
    plt.legend(labels=fig_legend, loc='best', markerscale=2)
    #plt.yscale('log')
    plt.xscale('log')
    plt.grid(True)

    plt.show()

#plot_EVR_array(txt_name, tally_number)

if __name__ == '__main__':
    main()
