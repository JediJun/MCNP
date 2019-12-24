# -*- coding: UTF-8 -*-
#####################################################################
#                                                                   #
#            MCNP out file Analsis file Part 1                      #
#   Extrcate data from  MCNP output files by ex_mcnpoutput_data.py  #
#                                                                   #
#                                     by:czj 2019.12.24             #
#                https://github.com/JediJun                         #
#####################################################################


#import plot_tallydata
import numpy as np
import re
import os 
import datetime
import copy
import matplotlib.pyplot as plt
import argparse
import linecache

def main():
    parser = argparse.ArgumentParser()
    parser.description = "Extarcte output file tally data to seperated txt files, please enter two parameters: output file and tallyN "
    parser.add_argument("-f", "--file", help="this is mcnp output file", dest="out_f", type=str, default="none")
    parser.add_argument("-n", "--tallyN", help="this is ntally number", dest="tallyN", type=int, default="0")
    parser.add_argument("-a", "--extall", help="extracte all tally data", dest="extracteAll", action='store_true', default="none")
    parser.add_argument("-l", "--list", help="list tally number", dest="talist", action='store_true', default="0")
    parser.add_argument("-p", "--plot", help="plot tallyN", dest="plotn", type=int, default="0")
    args = parser.parse_args()
    if args.out_f != "none":
        outfile_name = args.out_f
        tally_number = args.tallyN
        tal_seq_list, tal_par_list, tal_cs_list = read_tal_list(outfile_name)
        if args.tallyN != 0 and args.extracteAll != True:
            data2txt(outfile_name, tally_number)
        elif args.tallyN == 0 and args.extracteAll == True:
            print(" Try to extracte all tally data from ", args.mctalfile)
            for i in tal_seq_list:
                data2txt(outfile_name,i)
            print("  Extraction done.")
        elif args.tallyN == 0 and args.extracteAll != True and args.talist == True:
            print("  Tally list: ",tal_seq_list)
        elif args.plotn != 0:
            print("  Plot tally %d " %args.plotn)
        else:
            print("  Please input tally number '-n N' or '-a'")
    else:
        print("  Please input mctal file name '-f mctalfile'")


#  read data from MCNP output file

#outfile_name = "d13_5e8.out"
#outfile_name = "2cm_colli_5cmLead1211.s5mx"
#outfile_name = "shd1211.concrete"
def get_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read()
    else:
        print('  output file \'%s\' not exsist, please check again!' %filename)
        return 0

#  read tally card list format (Fn, mode = n,p,h, cell,surf = n)
def read_tal_list(outfile_name):
    pattern = re.compile(r'(F[\d]*)(:)(\w)([\s]*)([\d]*)', re.I)
    out_f = get_file(outfile_name)
    tal_list_tmp = pattern.findall(out_f)
    #print(tal_list_tmp)
    tal_seq_list= []
    tal_par_list = []
    tal_cs_list = []
    for i in tal_list_tmp:
        j =list(copy.deepcopy(i))
        del j[1]
        del j[-2]
        j[0] = re.sub(r'F', "", j[0]) 
        tal_seq_list.append(int(j[0]))
        tal_par_list.append(j[1])
        tal_cs_list.append(int(j[2]))
    #print(tal_seq_list)
    return tal_seq_list, tal_par_list, tal_cs_list

#read_tal_list(outfile_name)


def read_1tal_tot_list(outfile_name, tally_number = 0):
    pattern_1tally = re.compile(r'(\d\w{5})(\s+)(\d+)(\s+)(nps)')
    pattern_total = re.compile(r'(\s{6}total\s{5})([-\s]\d\.\d{5}E[+-]\d{2})\s(\d\.\d{4})')
    out_f = get_file(outfile_name)
    tal_line_list = pattern_1tally.findall(out_f)
    total_list = pattern_total.findall(out_f)
    taln_line = []
    totaln_list = []
    for i in tal_line_list:
        taln_line.append(i[2])
    for j in total_list:
        j_tmp = re.sub(r" ", "", j[1])
        totaln_list.append(j_tmp) 
    list_1tally_total = [taln_line, totaln_list]
    #print(list_1tally_total)
    return list_1tally_total

#read_1tal_tot_list(outfile_name)

def read_data_line_list(outfile_name):
    pattern_energy = re.compile(r'^\s{6}energy$')
    pattern_total = re.compile(r'^(\s{6}total\s{5})([-\s]\d\.\d{5}E[+-]\d{2})\s(\d\.\d{4})$')
    with open(outfile_name, "r") as out_f:
        count = 1
        tal_data_start_line_list = []
        tal_data_end_line_list = []
        for line in out_f.readlines():
            if pattern_energy.match(line):
                tal_data_start_line_list.append(count+1)
            elif pattern_total.match(line):
                tal_data_end_line_list.append(count-1)
            count += 1
        print('------------------------------------------------------------------------\n')
        print(tal_data_start_line_list)
        print(tal_data_end_line_list)
        print("  File '%s', total lines:%d " %(outfile_name,count))
        print('------------------------------------------------------------------------\n')
        return tal_data_start_line_list, tal_data_end_line_list

#read_data_line_list(outfile_name)

def read_data2list(outfile_name, start_line,end_line):
    line_len = end_line -start_line + 1
    E_list = []
    V_list = []
    R_list = []
    data_list = []
    for k in range(start_line, end_line + 1, 1):
        data_line_str = linecache.getline(outfile_name, k)
        data_line_tmp = data_line_str.split()
        data_tmp = list(map(float, data_line_tmp))
        data_list.append(data_tmp)
        E_list.append(data_line_tmp[0])
        V_list.append(data_line_tmp[1])
        R_list.append(data_line_tmp[2])
    #data_list = (E_list, V_list, R_list)
    #print(data_list[1:10]) 
    return data_list

#read_data2list(outfile_name, 27728,27750)

def read_tallyN_data(outfile_name,tally_number):
    tal_seq_list, tal_par_list, tal_cs_list = read_tal_list(outfile_name)
    tal_data_start_line_list, tal_data_end_line_list = read_data_line_list(outfile_name)
    
    if tally_number in tal_seq_list:
        index = tal_seq_list.index(tally_number)
        start = tal_data_start_line_list[index]
        end = tal_data_end_line_list[index]
        particle = tal_par_list[index]
        cellorsuface_Number = tal_cs_list[index]
        return read_data2list(outfile_name, start, end), particle, cellorsuface_Number
    else:
        print("  Error: no tally number in tally list: ", tal_seq_list)

#read_tallyN_data(outfile_name,55)

def data2txt(outfile_name, tally_number):
    data_list, particle, cellorsuface_Number = read_tallyN_data(outfile_name, tally_number)
    time_str = datetime.datetime.now().strftime("%m-%d-%H-%M")
    data_txt_name = "F" + str(tally_number) + "_" + outfile_name +"_" + time_str  + ".txt"
    if  os.path.exists(data_txt_name):
        data_txt_name2 = data_txt_name + "2"
        print("  file %s exsit, created file %s instead." %(data_txt_name, data_txt_name2))
        data_txt_name = data_txt_name2
    with open(data_txt_name, "a+") as f:
        for i in range(len(data_list)):
            f.write(str(data_list[i][0])),     f.write('    ')
            f.write(str(data_list[i][1])),         f.write('    ')
            f.write(str(data_list[i][2])),        f.write('\n')
    print('  Tally %d (par: %s) writen to file: %s\n' %(tally_number,particle, data_txt_name))
    print('------------------------------------------------------------------------\n')

#data2txt(outfile_name, 14)

def array_info(EVR_array, outfile_name = "data", tally_number = 0 ):
    EVR = copy.deepcopy(EVR_array)
    #print(type(EVR))
    print("------------------------------------------------------------------------\n")
    print(" Tally F%d data info:" %tally_number)
    print(" file: %s" %outfile_name)
    print('   E: %.5e to %.5e' %(EVR[1,0], EVR[-1,0]))
    print('   bin number: %.2d' %(EVR.size/3))
    sum_col = EVR.sum(axis=0)
    max_col = np.amax(EVR, axis=0)
    min_col = np.amin(EVR, axis=0)
    print('   Total Vals: %.5e' %sum_col[1])
    print('     Max  Val: {:.5e}, Min  Val:{:.5e} '.format(max_col[1],min_col[1]))
    print("------------------------------------------------------------------------\n") 
    E_min = EVR[1,0]
    E_max = EVR[-1,0]
    Val_max = max_col[1] 
    Val_min = min_col[1] 
    Val_total = sum_col[1]
    return  E_min, E_min, Val_max, Val_min, Val_total


def plot_tallyN(outfile_name,tally_number):
    data_list, particle,cellorsuface_Number = read_tallyN_data(outfile_name, tally_number)
    EVR_array = np.array(data_list, dtype=np.float32)
    print(EVR_array.shape)
    print(EVR_array.ndim)
    E_min, E_max, Val_max, Val_min, Val_total = array_info(EVR_array, outfile_name, tally_number)

    E = EVR_array[:,0]
    Vals = EVR_array[:,1]
    R = EVR_array[:,2]
    Vals_nonzero_index = np.nonzero(Vals)
    Vals_nonzero = Vals[Vals_nonzero_index]
    E_nonzero = E[Vals_nonzero_index]
    fig_title = outfile_name[0:-4] + "F" + str(tally_number) + " for " + particle
    fig_legend = "F" + str(tally_number)
    
    plt.title(fig_title)
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.plot(E_nonzero,Vals_nonzero)
    plt.xlim([E_min,E_max*1.1]), plt.ylim([Val_min,Val_max*1.2])
    plt.xlabel('E (MeV)'), plt.ylabel('count')
    print(fig_legend)
    plt.legend(labels=fig_legend, loc='best', markerscale=2)
    #plt.yscale('log')
    #plt.xscale('log')
    plt.grid(True)

    plt.show()

#plot_tallyN(outfile_name,44)

if __name__ == '__main__':
    main()
