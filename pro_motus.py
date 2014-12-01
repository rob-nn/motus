import cProfile
import pstats
import os
import shutil
import motus

def run():
    confs = [(9,30), (10, 30), (11, 30)] 
    ann = motus.Motus(desc='Profiler', activations=20, configs = confs, out_index=3)
    ann.train(50)

if __name__ == '__main__':
    if os.path.isfile('pro_motus.prof'):
        shutil.move('pro_motus.prof', 'pro_motus.prof.old') 
        p = pstats.Stats('pro_motus.prof.old')
        p.strip_dirs().sort_stats('time').print_stats(20)

    cProfile.run('run()', 'pro_motus.prof')
    p = pstats.Stats('pro_motus.prof')
    p.strip_dirs().sort_stats('time').print_stats(20)

