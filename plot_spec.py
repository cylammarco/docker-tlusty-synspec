import argparse
import numpy as np
import os
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument(
    '--folder',
    type=str,
    required=True,
    help="Path to the folder containing the TLUSTY config file.")
parser.add_argument('--wmin',
                    type=float,
                    default=250,
                    help="Minimum wavelength (nm)")
parser.add_argument('--wmax',
                    type=float,
                    default=1250,
                    help="Maximum wavelength (nm)")

folder_path = parser.folder
wave_min = parser.wmin
wave_max = parser.wmax

fig2 = plt.figure(1, figsize=(12, 6))
fig3 = plt.figure(2, figsize=(12, 6))

ax2 = fig2.add_subplot()
ax3 = fig3.add_subplot()

for i in os.listdir(folder_path):

    if i.endswith('.9'):

        table = np.genfromtxt(i, skip_header=3, dtype='U')

        iteration = table[:, 0]
        iteration_id = table[:, 1]
        temp = table[:, 2]
        ne = table[:, 3]
        pop = table[:, 4]
        rad = table[:, 5]
        maximum = table[:, 6]
        ilev = table[:, 7]
        ifr = table[:, 8]

        temp = ['E'.join(i.split('D')) for i in temp]
        ne = ['E'.join(i.split('D')) for i in ne]
        pop = ['E'.join(i.split('D')) for i in pop]
        rad = ['E'.join(i.split('D')) for i in rad]
        maximum = ['E'.join(i.split('D')) for i in maximum]

        iteration = np.array(iteration).astype('int')
        iteration_id = np.array(iteration_id).astype('int')
        temp = np.array(temp).astype('float')
        ne = np.array(ne).astype('float')
        pop = np.array(pop).astype('float')
        rad = np.array(rad).astype('float')
        maximum = np.array(maximum).astype('float')
        ilev = np.array(ilev).astype('int')
        ifr = np.array(ifr).astype('int')

        fig1 = plt.figure(1, figsize=(20, 12))
        # top left
        ax1 = fig1.add_subplot(2, 3, 1)
        # top centre
        ax2 = fig1.add_subplot(2, 3, 2)
        # top right
        ax3 = fig1.add_subplot(2, 3, 3)
        # bottom left
        ax4 = fig1.add_subplot(2, 3, 4)
        # bottom centre
        ax5 = fig1.add_subplot(2, 3, 5)
        # bottom right
        ax6 = fig1.add_subplot(2, 3, 6)

        temp_iter = np.zeros(len(np.unique(iteration)))
        maximum_iter = np.zeros(len(np.unique(iteration)))
        for i in np.sort(np.unique(iteration)):
            mask = (iteration == i)
            ax1.plot(iteration_id[mask], temp[mask], label=str(i))
            ax2.plot(iteration_id[mask],
                     np.log10(np.abs(temp[mask])),
                     label=str(i))
            ax4.plot(iteration_id[mask], maximum[mask], label=str(i))
            ax5.plot(iteration_id[mask],
                     np.log10(np.abs(maximum[mask])),
                     label=str(i))
            temp_iter[i - 1] = abs(temp[mask][0])
            maximum_iter[i - 1] = abs(maximum[mask][0])

        ax3.plot(np.sort(np.unique(iteration)), np.log10(temp_iter))
        ax6.plot(np.sort(np.unique(iteration)), np.log10(maximum_iter))

        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()
        ax5.grid()
        ax6.grid()

        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        ax6.legend()

        ax1.set_xlabel('id')
        ax1.set_ylabel(r'$\Delta$(T)')

        ax2.set_xlabel('id')
        ax2.set_ylabel(r'log($\Delta$(T)')

        ax3.set_xlabel('iteration')
        ax3.set_ylabel(r'T$_{\mathrm{end\ point}}$')

        ax4.set_xlabel('id')
        ax4.set_ylabel(r'$\Delta$(Maximum V)')

        ax5.set_xlabel('id')
        ax5.set_ylabel(r'log($\Delta$(Maximum V)')

        ax6.set_xlabel('iteration')
        ax6.set_ylabel(r'Maximum V$_{\mathrm{end\ point}}$')

        fig1.suptitle(i.split('/')[-1])
        fig1.tight_layout()
        fig1.savefig(
            os.path.join('01_TLUSTY_convergence_',
                         i.split('/')[-1].split('.')[0], '.png'))

    if i.endswith(".13"):

        data = np.genfromtxt(i, dtype='U')

        freq = data[:, 0]
        flux = data[:, 1]

        freq = ['E'.join(f.split('D')) for f in freq]
        flux = ['E'.join(f.split('D')) for f in flux]

        freq = np.array(freq).astype('float')
        flux = np.array(flux).astype('float')

        wave = 3.0E8 / freq * 1E9

        mask = (wave > wave_min) & (wave < wave_max)
        fig2_ymax = np.nanmax(flux[mask])

        ax1.plot(wave[mask], flux[mask], label=i.split('/')[-1])

    if i.endswith('.spec'):

        spec = np.genfromtxt(i)
        wave = spec[:, 0] / 10.
        flux = spec[:, 1]

        mask = (wave > wave_min) & (wave < wave_max)
        fig3_ymax = np.nanmax(flux[mask])

        ax3.plot(wave, flux, label=i.split('/')[-1])

ax2.xlim(wave_min, wave_max)
ax2.ylim(0.0, fig2_ymax)
ax2.xlabel('Wavelength / nm')
ax2.ylabel('Flux / Arbitrary')
ax2.grid()
ax2.legend()
ax2.tight_layout()
ax2.savefig(os.path.join(folder_path, '02_TLUSTY_output.png'))

ax3.xlim(wave_min, wave_max)
ax3.ylim(0.0, fig3_ymax)
ax3.xlabel('Wavelength / nm')
ax3.ylabel('Flux / Arbitrary')
ax3.grid()
ax3.tight_layout()
ax3.savefig(os.path.join(folder_path, '03_SYNSPEC_output.png'))
