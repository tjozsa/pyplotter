import subprocess, time, os, sys
import shutil

from os import path
from datetime import datetime

""" This module contains wrapper code around pguPlotGenerator.
    The main goal is to implement smart and error "fault tolerant"
    utility to plot multiple hundreds of terrabites of external drive.
"""

print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: " , str(sys.argv))

#we need to get certain command line parameters to do our job
#account_id: the burst numberic account id we need to use for the generation of nonce and the filename
#increment: nonce that will be aded to one filename
#filenum: the total number of files to generate
#final_target: the final path to where we will move each file when it is plotted fully

#python3 pyplotter.py 17794691632528195274 4096000 5 /media/tjozsa/External2

workingdir = os.getcwd()

account_id = sys.argv[1]
increment = int(sys.argv[2])
filenum = int(sys.argv[3])
final_target = sys.argv[4]
stagger = 8192

drives = ["/media/tjozsa/External1/",
"/media/tjozsa/External2/",
"/media/tjozsa/External3/",
"/media/tjozsa/storage1",
"/media/tjozsa/storage2",
"/media/tjozsa/storage3",]

def collect_plots():
    """Collects all the plot files on a path and returns as an array"""
    plots = []
    for d in drives:
        os.chdir(d)
        files = [f for f in os.listdir(d) if path.isfile(f)]
        for f in files:
            # print("found {} in {}".format(f,d))
            plots.append("{}{}".format(d, f))
    return plots

def next_start_nonce():
    """goes through all found plot files and finds the largest starting nonce.
    Then it calculates the next starting nonce by adding one to the sum of last_start + increment"""
    plots = collect_plots()
    laststartingnonce = 0
    for p in plots:
        exp = p.split("_")
        if int(exp[1]) >= laststartingnonce:
            laststartingnonce = int(exp[1])
    return laststartingnonce + increment + 1

def plot_files():
    """ Collects all plot files from drive list
    """
    for i in range(0,filenum):
        thisnonce = next_start_nonce()
        os.chdir(workingdir)
        cmd = "./plotavx2 -k {accontid} -x 2 -d {ppath} -s {nstart} -n {ninc} -m {stag} -t 8 -a".format(accontid=account_id, ppath=final_target, nstart=thisnonce, ninc=increment, stag=stagger)
        # cmd = "./plotavx2 -k {}account_id), "-x", "2", "-d", "{}".format(final_target), "-s", "{}".format(thisnonce), "-n", "{}".format(increment), "-m", "{}".format(stagger), "-t", "8", "-a"]
        print(cmd)
        print("[{}] starting plotting ({})".format(str(datetime.now()), str(thisnonce)))
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in iter(process.stdout.readline, b''):
            print(">>> " + str(line.rstrip()))

        process.wait()
        print(process.returncode)
        print("[{}] finished plotting ({})".format(str(datetime.now()), str(thisnonce)))
    return

plot_files()
