import pdb
import cmac

def basic_cmac():
    confs = []
    confs.append(cmac.SensoryCellConfig(0., 1., 50))
    confs.append(cmac.SensoryCellConfig(0., 1., 50))
    confs.append(cmac.SensoryCellConfig(0., 1., 50))
    _cmac = cmac.CMAC(confs, 4)
    _cmac.generate_tables()
    return _cmac


if __name__ == '__main__':
    pdb.run('basic_cmac()')
