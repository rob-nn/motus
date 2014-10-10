import cProfile
import cmac
import pstats
import os
import shutil
import motus

def basic_cmac():
    confs = []
    confs.append(cmac.SensoryCellConfig(0., 1., 10))
    confs.append(cmac.SensoryCellConfig(0., 1., 10))
    confs.append(cmac.SensoryCellConfig(0., 1., 10))
    _cmac = cmac.CMAC(confs, 4)
    _cmac.generate_tables()

if __name__ == '__main__':
    if os.path.isfile('pro_motus.prof'):
        shutil.move('pro_motus.prof', 'pro_motus.prof.old') 
        p = pstats.Stats('pro_motus.prof.old')
        p.strip_dirs().sort_stats('time').print_stats(20)

    cProfile.run('motus.main()', 'pro_motus.prof')
    p = pstats.Stats('pro_motus.prof')
    p.strip_dirs().sort_stats('time').print_stats(20)

