import configuration,os,simulate, subprocess
from shutil import move
import xml.etree.ElementTree as ET

from copy import copy

def dictify(r,root=True):
    if root:
        return {r.tag : dictify(r, False)}
    d=copy(r.attrib)
    if r.text:
        d["_text"]=r.text
    for x in r.findall("./*"):
        if x.tag not in d:
            d[x.tag]=[]
        d[x.tag].append(dictify(x,False))
    return d

def parseConfigFile(sessionID):
    tree = ET.parse(configuration.SESSION_PATH+sessionID+'/'+'config.xml')
    root = tree.getroot()
    return dictify(root)['simulation']


def checkBinaryFiles(config):
    for app in config['benchmark']:
        if app['type'] == 'NAS':
            b_kernel = app['kernel']
            b_class = app['class']
            b_numprocs = app['numprocs']

            if os.path.isfile(configuration.BIN_PATH+b_kernel+'.'+b_class+'.'+b_numprocs):
                simulate.printLog('NAS kernel exists')
            else:
                simulate.printLog(configuration.BIN_PATH+b_kernel+'.'+b_class+'.'+b_numprocs+' not found. Create binary file.')
                compileBinaryFiles('NAS',b_numprocs,b_kernel,b_class)
        
        if app['type'] == 'graph500':
            if os.path.isfile(configuration.BIN_PATH+'graph500_smpi_simple'):
                simulate.printLog('graph500 binary file exists.')
            else:
                simulate.printLog(configuration.BIN_PATH+'graph500_smpi_simple'+' not found. Create binary file.')
                compileBinaryFiles('graph500')
        if app['type'] == 'himeno':
            b_class = app['class']
            b_numprocs = app['numprocs']
            b_filename = 'himeno'+'.'+b_class+'.'+b_numprocs

            if os.path.isfile(configuration.BIN_PATH+b_filename):
                simulate.printLog('Himeno benchmark file exists')
            else:
                simulate.printLog(configuration.BIN_PATH+b_filename+' not found. Create binary file.')
                compileBinaryFiles('himeno',b_numprocs,'',b_class)

def compileBinaryFiles(b_type,numprocs='1',kernel='ep',b_class='S'):
    if b_type == 'NAS':
        os.chdir(configuration.NAS_PATH)
        command = ['make',kernel,'NPROCS='+numprocs,'CLASS='+b_class]
        b_filename = kernel+'.'+b_class+'.'+numprocs
        process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stderr is not '':
            simulate.printLog('Error compiling benchmark application')
            simulate.printLog(stdout)
            simulate.printLog(stderr)

        if os.path.isfile(configuration.NAS_PATH+'bin/'+b_filename):
            move(configuration.NAS_PATH+'bin/'+b_filename,configuration.BIN_PATH+b_filename)
            simulate.printLog('Finish compiling benchmark application')

    if b_type == 'himeno':
        os.chdir(configuration.HIMENO_PATH)
        b_filename = 'himeno'+'.'+b_class+'.'+numprocs
        args = ['./set_params',b_class,numprocs]
        print 'current dir '+os.getcwd()
        print ''.join(args)
        get_param = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        simulate.printLog('[Himeno] Generate parameters.')

        command = ['smpicc','-o',b_filename,'himenoBMT_m.c']
        compiler = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        simulate.printLog('[Himeno] Compiling benchmark file.')

        if os.path.isfile(configuration.HIMENO_PATH+b_filename):
            move(configuration.HIMENO_PATH+b_filename,configuration.BIN_PATH+b_filename)
            simulate.printLog('Finish compiling benchmark application')

    if b_type == 'graph500':
        os.chdir(configuration.G500_PATH)
        b_filename = 'graph500_smpi_simple'
        command = ['make', 'graph500_mpi_simple']
        process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stderr is not '':
            simulate.printLog('Error compiling benchmark application')
            simulate.printLog(stdout)
            simulate.printLog(stderr)

        if os.path.isfile(configuration.G500_PATH+b_filename):
            move(configuration.G500_PATH+b_filename,configuration.BIN_PATH+b_filename)
            simulate.printLog('Finish compiling benchmark application')

############## TEST ##############
config = parseConfigFile('1')
checkBinaryFiles(config)