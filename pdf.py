#!/usr/bin/python3.10

'''
    Calculation: Plane Distribution Function (PDF).
    Description: Determines the PDF over XY plane when given a xsf file.
                Everything is in Angstrom.
    Written by: Ignacio J. Chevallier-Boutell.
    Dated: August, 2021.
'''

import argparse
from core.coreHP import *
from time import time

def main():
    start = time()

    dxy = args.dxy
    Hmin = args.Hcut[0]
    Hmax = args.Hcut[1]
    at = args.at

    frames_count = 0
    frames_start = args.frames[0]
    if frames_start != 0:
        frames_start -= 1

    print(f'Running PDF for {at} atoms.')

    frames_total, Lx, Ly, Lz, nAtTot, nAt, xyz_all = userfile_mono(args.input_file, at)

    nBinX, nBinY, Lx, Ly, PDF = hist_init_pdf(Lx, Ly, dxy)

    rows = nAtTot + 2

    frames_end = args.frames[1]
    if frames_end == -1:
        frames_end = frames_total

    nAtSlab = 0

    for frame in range(frames_start, frames_end):
        xyz = xyz_all.iloc[(frame * rows + 2) : ((frame + 1) * rows), :]
        xyz = xyz[(xyz['idAt'] == at) & (Hmin <= xyz['rz']) & (xyz['rz'] < Hmax)].to_numpy()
        nAt = len(xyz)
        sample_pdf(Lx, Ly, xyz, dxy, PDF, nAt)
        frames_count += 1
        nAtSlab += nAt

    output_file = args.output_file
    if output_file == None:
        output_file = f'PDF_{at}_z-{Hmin:.2f}-{Hmax:.2f}'

    normalize_pdf(dxy, nBinX, nBinY, frames_count, PDF, output_file)

    print(f'Job done in {(time() - start):.3f} seconds!')
    print(f'Output file: {output_file}.csv')
    print(f'There are {nAtSlab/frames_count:.2f} {at} atoms on average within this slab.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', help = "Path to the xsf input file.")

    parser.add_argument('at', help = "Atom to be analyzed.")

    parser.add_argument('dxy', type = float, help = "Increment to be considered \
                        along x and y axis.")

    parser.add_argument('Hcut', type = float, nargs = 2, default = [0, -1],
                        help = "Minimum and maximum heights to be considered.")

    parser.add_argument('-f', '--frames', nargs = 2, default = [0, -1], type = int,
                        help = "Choose starting and ending frames to compute.")

    parser.add_argument('-o', '--output_file', help = "Path to the output file. \
                        If not given, the default name will be used.")

    args = parser.parse_args()

    main()
