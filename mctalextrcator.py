##################################################################
#                                                                #
#           MCNP MCTL file Analsis file Part 1                   #
#    Extracte tally data from MCTAL file to seperate txt files   #
#                                                                #   
#                                     by:czj 2019.12.18          #
##################################################################
#                                                                #  
#         |--- two line Info  |                                  #
#         |                   |                                  #
#         |--- ntally line    |                                  #
#         |                   |                                  #
# read -> |--- tally list     |--> read E/Vals ---> save to txt  #
#         |                   |                                  #
#         |--- bin list       |                                  #
#         |                   |                                  #
#         |--- et\vals line   |                                  #
#                                                                #
##################################################################
#                                                                #
#  Function list:                                                #
#               get_mcfile(mc_f)                                 #
#               mctal_info(mc_f)                                 #
#               read_ntal(mc_f)                                  #
#               read_tal_list(mc_f)                              #
#               read_et_bin_list(mc_f)                           #
#               keyword_linenum_list(mc_f, keyword)              #
#               read_tallyN_data(mc_f, tally_number)             #
#               read_E_data(mc_f, tally_number)                  #
#               read_Val_data(mc_f, tally_number)                #
#               save_tallyN_data2txt(mc_f, tally_number)         #
#               check_extrc_number(mc_f, tally_number)           #
#               log_txt(txt)                                     #
#                                                                #
##################################################################
import linecache
import re 
import os
import numpy as np
import datetime
import sys
import argparse

#  Start to parse mctal file:
#  read input line 


def main():
    parser = argparse.ArgumentParser()
    parser.description = "Extarcte MCTAL tally data to seperated txt files, please enter two parameters: mctalfile and tally-N"
    parser.add_argument("-f", "--file", help="this is mctalfile", dest="mctalfile", type=str, default="none")
    parser.add_argument("-n", "--tallyN", help="this is ntally number", dest="tallyN", type=int, default="0")
    parser.add_argument("-a", "--extall", help="extracte all tally data", dest="extracteAll", sction='store_true', default="none")
    parser.add_argument("-l", "--list", help="list tally number", dest="talist", action='store_true', default="none")
    args = parser.parse_args()
    print("parameter f is :",args.mctalfile)
    print("parameter n is :",args.tallyN)
    print("parameter a is :",args.extracteAll)
    if args.mctalfile != "none":
        mctal_filename = args.mctalfile
        tally_number = args.tallyN
        if args.tallyN != 0 and args.extracteAll != True:
            #tally_card_rule = (1,2,4,5,6,7,8)
            #input_tal_str = []
            #input_tal_str.extend(str(args.tallyN))
            #print(input_tal_str)
            #if int(input_tal_str[-1]) not in tally_card_rule:
            #    print("    Error: No such F%d tally card in MCNP Fn(1,2,4,5,6,7,8)" %args.tallyN)
            #    print("    Please check is again!")
            #    sys.exit()
            mctal_info(mctal_filename)
            check_extrc_number(mctal_filename, tally_number)
        elif args.tallyN == 0 and args.extracteAll == True:
            print(" Try to extracte all tally data from ", args.mctalfile)
            mctal_info(mctal_filename)
            check_extrc_number(mctal_filename, tally_number)
        elif args.tallyN == 0 and args.extracteAll != True and args.talist == True:
            tal_list = read_tal_list(mctal_filename)
            print("  Tally list: ",tal_list)
        else:
            print("  Please input tally number '-n N' or '-a'")
    else:
        print("  Please input mctal file name '-f mctalfile'")


            
        

#open and check file

def get_mcfile(mctal_filename):
    if os.path.exists(mctal_filename):
        with open(mctal_filename, 'r') as mcfile:
            return mcfile.read()
    else:
        #print('MCTAL file \'%s\' not exsist, please check again!' %mctal_filename)
        return 0

#  print and first two lines and basic info on mctal file
def mctal_info(mctal_filename):
    if get_mcfile(mctal_filename) == 0:
        print('MCTAL file \'%s\' not exsist, please check again!' %mctal_filename)
        return
    #  print first two lines
    print('Mctal Info:')
    print('======================================================================\n')
    print(linecache.getline(mctal_filename,1))
    print(linecache.getline(mctal_filename,2))
    print('======================================================================\n')
    #  count file lines 
    buffer_file_list = linecache.getlines(mctal_filename)
    #print(type(buffer_file_list))
    file_lines = len(buffer_file_list)
    #  count file lens
    with open(mctal_filename, 'r') as mcfile:
        file_lens = len(mcfile.read())
    #  count file size
    file_path = '.\\' + mctal_filename
    file_size = os.path.getsize(file_path)
    print(' mctal file: %s, Lens: %d, Lines: %d, Size: %d kB \n' 
                           %(mctal_filename, file_lens, file_lines, file_size/1024))
    tal_list = read_tal_list(mctal_filename)
    print(' tally list: %s' %tal_list)
    print('---------------------------------------------------------------------\n')


#  read ntally number
def read_ntal(mctal_filename):
    ntal_pattern = re.compile(r'ntal\s\s\s\s\s\d+')
    mcfile = get_mcfile(mctal_filename)
    ntal = ntal_pattern.findall(mcfile)
    if ntal:
        ntal_result_str = "".join(ntal)
        #print(ntal_result_str)
        ntal_result_list = ntal_result_str.split()
        #print(ntal_result_list)
        if len(ntal_result_list) == 2:
            ntally = int(ntal_result_list[1])
            #print('ntally = %d' %ntally)
            #print('------------------------------------------------------------------------')
            return ntally
        else:
            print('Error!')
            print('ntal line:\n%s' %ntal_result_list)
    else:
        print('No ntal line, exit parsing process.')



def read_tal_list(mctal_file):
    tal_line = linecache.getline(mctal_file,4)
    if tal_line:
        tal_str = ''.join(tal_line)
        tal_list = tal_str.split()
        tal_list = list(map(int, tal_list))
        #print('Test: tally list: %s' %tal_list)
        #print('------------------------------------------------------------------------')
        return tal_list
    else:
        print('Read tal line failed')


def read_et_bin_list(mctal_filename):
    mctl = get_mcfile(mctal_filename)
    et_pattern = re.compile(r'et\s+\d+')
    ets = et_pattern.findall(mctl)
    #print(ets)
    ets_list = []
    for i in range(len(ets)):    
        str_tmp = ''.join(ets[i])
        str_num = re.sub(r'\w+\s+',"",str_tmp)
        ets_list.append(str_num)
    ets_list = list(map(int, ets_list))
    #print('Test: et bin list = %s' %ets_list)
    #print('------------------------------------------------------------------------')
    return ets_list


def keyword_linenum_list(mctal_filename, keyword):
    #et_pattern = re.compile(r'et\s+\d+')
    #et_line_list= []
    if get_mcfile(mctal_filename) == 0:
        return
    line_list = []
    pattern = re.compile(keyword)
    count = 0
    with open(mctal_filename) as mcfile:
        for line in mcfile:
            count += 1
            match = re.match(pattern, line)
            if match:
                line_list.append(count)
    #print(" Test: %s line_list = %s" %(keyword, line_list))
    #print('------------------------------------------------------------------------')
    return line_list


def read_tallyN_data(mctal_filename, tally_number):
    tal_list = read_tal_list(mctal_filename)
    et_line_list = keyword_linenum_list(mctal_filename, 'et')
    vals_line_list = keyword_linenum_list(mctal_filename, 'vals')
    et_bin_list = read_et_bin_list(mctal_filename) 
    if tally_number in tal_list:
        tal_index = tal_list.index(tally_number)
        E_start_line = et_line_list[tal_index] + 1
        E_end_line = vals_line_list[tal_index] - 2

        Val_start_line = vals_line_list[tal_index] + 1
        if et_bin_list[tal_index] <= 4:
            lines = 1
        elif (et_bin_list[tal_index] > 4) and (et_bin_list[tal_index] *2 % 8) == 0:
            lines = et_bin_list[tal_index] // 4
        else:
            lines = et_bin_list[tal_index] //4 + 1
        Val_end_line = vals_line_list[tal_index] +  lines 
        
        E_Val = read_E_data(mctal_filename, E_start_line, E_end_line )
        Val_list,ValR_list = read_Val_data(mctal_filename, Val_start_line, Val_end_line)
        Val_total = Val_list.pop(-1)
        Val_total_R = ValR_list.pop(-1)
        tallyN_total = []
        tallyN_total.append(Val_total)
        tallyN_total.append(Val_total_R)
        #print(Val_list[0:10])
        #print(ValR_list[0:10])
        #print('  Val total: %e  R: %f' %(Val_total, Val_total_R))
        #print('  Get bins: [E, Val, R] : [%d, %d, %d]\n' %(len(E_Val), len(Val_list), len(ValR_list)))
        #print('------------------------------------------------------------------------\n')
        if len(E_Val) != len(Val_list):
            print('  Error: Ebin != Vbin , parser error! ')
            return
        else:
            return E_Val, Val_list, ValR_list, tallyN_total
    else:
        print('  No tally number %d in mtal file.' %tally_number)


def read_E_data(mctal_file, start_line, end_line):
    E_data_list = []
    read_time = end_line - start_line + 1 
    for k in range(read_time):
        read_line = start_line +k
        data_line_str = linecache.getline(mctal_file, read_line)
        data_line_list = data_line_str.split()
        data_line_list = list(map(float,data_line_list))
        E_data_list.extend(data_line_list)
    return E_data_list

def read_Val_data(mctal_file, start_line, end_line):    
    data_list_Val = []
    data_list_R = []
    read_time = end_line - start_line + 1
    for k in range(read_time):
        read_line = start_line + k 
        data_line_str = linecache.getline(mctal_file, read_line)
        data_line_list = data_line_str.split()
        data_line_Val = data_line_list[::2]
        data_line_R = data_line_list[1::2]
        data_line_Val = list(map(float,data_line_Val))
        data_line_R = list(map(float,data_line_R))
        data_list_Val.extend(data_line_Val)
        data_list_R.extend(data_line_R)
    #print(len(data_list_R), len(data_list_Val))    
    return data_list_Val, data_list_R


def save_tallyN_data2txt(mctal_filename, tally_number): 
    E_Val,Val_list,ValR_list,tallyN_total = read_tallyN_data(mctal_filename, tally_number)
    #EVR_list = [E_Val, Val_list, ValR_list]
    #tally_data_array = np.asarray(EVR_list)
    #print(tally_data_array.shape)
    time_str = datetime.datetime.now().strftime('D%d_%H_%M')
    tallyNfile = 'tal_F' + str(tally_number) + '_' + mctal_filename + time_str + '.txt'    
    with open(tallyNfile, 'w') as f:
        for i in range(len(E_Val)):
            f.write(str(E_Val[i])),     f.write('    ')
            f.write(str(Val_list[i])), f.write('    ')
            f.write(str(ValR_list[i])), f.write('\n')
    print('  Tally %d writed to file: %s\n' %(tally_number,tallyNfile))
    logtxt(tallyNfile)
    print('------------------------------------------------------------------------\n')

def check_extrc_number(mctal_filename, Findex):
    if get_mcfile(mctal_filename) == 0:
        return   
    if (str(Findex)).isdigit():
        save_tallyN_data2txt(mctal_filename, Findex)
    elif Findex == 'a':
        for i in read_tal_list(mctal_filename):
            save_tallyN_data2txt(mctal_filename,i)
        print("  All tally card data extrcted to txt files\n")
    else:
        print("  Error: invalid parameters '%s'" %str(Findex))

def logtxt(txt):
    with open('MCNP_extract.log', 'a+') as log:
        time_str = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        log_txt = time_str + '  :  ' + str(txt) 
        log.write(log_txt)
        log.write("\n")


#******************************************************
#            Testing zoom
#******************************************************
#  must define mctal_filename
#mctal_filename = "mctal.2cm_colli_concrete.1211.s5mx"

#mctal_info(mctal_filename)
#check_extrc_number(mctal_filename, 32)

#******************************************************

if __name__ == '__main__':
    main()

