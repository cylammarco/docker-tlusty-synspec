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

args = parser.parse_args()

folder_path = args.folder
wave_min = args.wmin
wave_max = args.wmax

os.chdir(folder_path)

fig2 = plt.figure(2, figsize=(12, 6))
fig3 = plt.figure(3, figsize=(12, 6))

ax7 = fig2.add_subplot()
ax8 = fig3.add_subplot()

for i in os.listdir(folder_path):

    if i.endswith('.9') and not i.endswith('fort.9'):

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
        fig1.clf()
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
        for j in np.sort(np.unique(iteration)):
            mask = (iteration == j)
            ax1.plot(iteration_id[mask], temp[mask], label=str(j))
            ax2.plot(iteration_id[mask],
                     np.log10(np.abs(temp[mask])),
                     label=str(j))
            ax4.plot(iteration_id[mask], maximum[mask], label=str(j))
            ax5.plot(iteration_id[mask],
                     np.log10(np.abs(maximum[mask])),
                     label=str(j))
            temp_iter[j - 1] = abs(temp[mask][0])
            maximum_iter[j - 1] = abs(maximum[mask][0])

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

        fig1.suptitle(i)
        fig1.tight_layout()
        fig1.savefig(
            '01_TLUSTY_convergence_' +
                         i.split('.')[0] + '.png')

    if i.endswith(".13") and not i.endswith('fort.13'):

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

        ax7.plot(wave[mask], flux[mask], label=i.split('/')[-1])

    if i.endswith('.spec') and not i.endswith('fort.spec'):

        spec = np.genfromtxt(i)
        wave = spec[:, 0] / 10.
        flux = spec[:, 1]

        mask = (wave > wave_min) & (wave < wave_max)
        fig3_ymax = np.nanmax(flux[mask])

        ax8.plot(wave, flux, label=i.split('/')[-1])

ax7.set_xlim(wave_min, wave_max)
ax7.set_ylim(0.0, fig2_ymax)
ax7.set_xlabel('Wavelength / nm')
ax7.set_ylabel('Flux / Arbitrary')
ax7.grid()
ax7.legend()
fig2.tight_layout()
fig2.savefig(os.path.join(folder_path, '02_TLUSTY_output.png'))

ax8.set_xlim(wave_min, wave_max)
ax8.set_ylim(0.0, fig3_ymax)
ax8.set_xlabel('Wavelength / nm')
ax8.set_ylabel('Flux / Arbitrary')
ax8.grid()
fig3.tight_layout()
fig3.savefig(os.path.join(folder_path, '03_SYNSPEC_output.png'))
