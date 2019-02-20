import matplotlib
import shutil
import subprocess

plt_path = "{}/mpl-data/fonts/ttf/DejaVuSans.ttf".format(matplotlib.__path__[0])
shutil.copy2('SimHei.ttf', plt_path)
# subprocess.call(['fc-cache', '-fv'])
# subprocess.call(['cp', '-r', '{}/mpl-data/matplotlibrc'.format(matplotlib.__path__[0]), 'matplotlibrc'])
