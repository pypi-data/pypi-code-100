#!/usr/bin/env python3

import zcross
import argparse
import re
import sys
import matplotlib.pyplot as plt
import os
from pathlib import Path
from cycler import cycler
from pint import UnitRegistry



def main():
    ureg = UnitRegistry()

    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--bullet', default=None, help='Filter by bullet')
    parser.add_argument('-t', '--target', default=None, help='Filter by target')
    parser.add_argument('-c', '--collision', default=None, help='Filter by collision type')
    parser.add_argument('-e', '--exact',     action='store_true', help='Show only exact match')
    parser.add_argument(      '--velocity',  action='store_true', help='Show bullet velocity instead of energy')
    parser.add_argument('-v', '--verbose',   action='store_true', help='Does nothing, for compatibility')
    parser.add_argument('--title',     help='Title of the plot')
    parser.add_argument('--legend',     default='ids', choices=['ids', 'types', 'none'], help='Format of the legend to show')
    

    parser.add_argument('-o', '--output', default=None, help='Save plot to PNG')

    parser.add_argument('table', nargs='*')
    args = parser.parse_args()

    filter_bullet = args.bullet
    filter_target = args.target
    filter_collission = args.collision
    filter_exact = args.exact

    atoms = {}
      
        
    def calculate_mass(bullet):
        
        if len(atoms) == 0:
            import csv  
            
            csvPath = Path(__file__).parent.parent / 'share' / 'zcross'
            
            for filename in ('periodic.csv', 'isotopes.csv'):
                with open(csvPath / filename) as f:
                    
                    reader = csv.reader(f)
                    
                    header = next(reader, None)  # take the header
                    
                    keySymbol = header.index('Symbol')
                    keyMass   = header.index('Atomic Weight')
                    
                    for line in reader:
                        atoms[line[keySymbol]] = float(line[keyMass]) * ureg.u
                   
        if isinstance(bullet, Electron):
            return ureg.electron_mass
        elif isinstance(bullet, Molecule):
            if len(bullet.value) > 2:
                raise ValueError('Unable to calculate the mass for complex moecule: ' + bullet.value)
            return atoms[bullet]
        else:
            raise ValueError('Unable to calculate the mass for the object: ' + str(bullet))
            
        
        
        
        
    unit_energy   = ureg('eV')
    unit_velocity = ureg('cm/us')
    unit_area     = ureg('m^2')


    r = re.compile(r'^([\w\-\*]*)(?:\/([\w\-\*\(\)]+)(?:\/([\d\*\-\,]+))?)?$')

    filters = args.table

    if len(filters) == 0:
        filters.append('*')


    zs = []


    ms = [ r.match(filter) for filter in filters if filter != '']

    if any([m.group(1) == '*' for m in ms]):
        zs = zcross.load_all()
    else:
        for name in [m.group(1) for m in ms]:
            zs.append(zcross.load_by_name(name))
            
    processes = {}
    labels = {}

    for z in zs:
        database = z.database
        for group in database.groups.group:
            for process in group.processes.process:
                
                accept = False
                
                for m in ms:
                    acceptFilter = True
                    acceptFilter &= not (m.group(1) is not None and m.group(1) != '*' and m.group(1).lower() != database.id.lower())
                    acceptFilter &= not (m.group(2) is not None and m.group(2) != '*' and m.group(2).lower() != group.id.lower())
                    
                    if acceptFilter and m.group(3)  is not None and m.group(3) != '*':
                        
                        acceptToken = False
                        for token in m.group(3).split(','):
                            if '-' in token:
                                id_min,id_max = [int(v) if v != '' else None for v in token.split('-')]
                                acceptToken |=  (id_min is None or process.id >= id_min) and (id_max is None or process.id <= id_max)
                            else:
                                acceptToken |=  int(token) == process.id
                        acceptFilter &= acceptToken
                    
                    if acceptFilter:
                        accept = True
                        break
                
                if accept:
                    
                    if filter_bullet is not None:
                        if filter_bullet == 'e' and isinstance(process.reactants.orderedContent()[0].value, zcross.Electron):
                            pass
                        elif filter_exact and filter_bullet != 'e' and isinstance(process.reactants.orderedContent()[0].value, zcross.Molecule) and filter_target == str(process.reactants.orderedContent()[0].value):
                           pass
                        else:
                            continue
                            
                    if filter_target is not None:
                        if filter_target == 'e' and isinstance(process.reactants[1].value, zcross.Electron):
                            pass
                        elif not filter_exact and filter_target != 'e' and isinstance(process.reactants.orderedContent()[1].value, zcross.Molecule) and filter_target == process.reactants.orderedContent()[1].value.orderedContent()[0].value:
                            pass
                        elif     filter_exact and filter_target != 'e' and isinstance(process.reactants.orderedContent()[1].value, zcross.Molecule) and filter_target == str(process.reactants.orderedContent()[1].value):
                           pass
                        else:
                            continue
                            
                    if filter_collission is not None:
                        if filter_collission in ('total', 'elastic', 'inelastic', 'superelastic'):
                            if process.collisionType == filter_collission:
                                pass
                            else:
                                continue
                        elif filter_collission in ('excitation'):
                            if process.collisionType == 'inelastic' and process.inelasticType in ('excitation_ele', 'excitation_vib', 'excitation_rot'):
                                pass
                            else:
                                continue
                        elif filter_collission in ('excitation_ele', 'excitation_vib', 'excitation_rot', 'ionization', 'attachment', 'neutral'):
                            if process.collisionType == 'inelastic' and process.inelasticType == filter_collission:
                                pass
                            else:
                                continue
                        
                    
                    if process.data_x.units.lower() == 'hartee':
                        process_unit_energy   = ureg('Eh')
                    else:
                        process_unit_energy = ureg(process.data_x.units)
                    
                    if process.data_y.units == 'm2':
                        process_unit_area   = ureg('m^2')  
                    elif process.data_y.lower() == 'bohr2':
                        process_unit_area   = ureg('(hbar / (1./137. * m_e * c))^2')  # TODO: Replace with ureg('a0^2') when pint 0.10 will be released on pypi
                    else:
                        process_unit_area   = ureg(process.data_y.units)
                    
                    areas    = [ area   * process_unit_area   for area   in process.data_y.value() ]
                    
                    key = '{}/{}/{}'.format(database.id, group.id, process.id)
                    if not args.velocity:
                        energies = [ energy * process_unit_energy for energy in process.data_x.value() ]
                        processes[key] = (energies, areas)
                        
                    else:
                        bullet_mass = calculate_mass(process.reactants[0])
                        velocities = [ (2. * energy * process_unit_energy / bullet_mass) ** 0.5 for energy in process.energy ]
                        processes[key] = (velocities, areas)
                    
                    if args.legend == 'ids':
                        labels[key] = key 
                    elif args.legend == 'types':
                        labels[key] = process.get_simple_type()
                    else:
                        labels[key] = None
                    
    fig, ax1 = plt.subplots(dpi=150)

    #fig.set_figheight(15)
    #fig.set_figwidth(30)
    fig.set_figwidth(2 * fig.get_figheight())
    plt.title('Cross-sections tables' if args.title is None else args.title)
    
    
    ax1.set_axisbelow(True)
    ax1.grid(True, which='both', axis='both', color='#e0e0e0', linestyle='-', linewidth=1)
    ax1.minorticks_on()

    if not args.velocity:
        ax1.set_xlabel('Energy [{.units:~P}]'.format(unit_energy))
    else:
        ax1.set_xlabel('Velocity [{.units:~P}]'.format(unit_velocity))

    ax1.set_ylabel('Cross Section [{.units:~P}]'.format(unit_area))

    ax1.set_xscale('log')
    ax1.set_yscale('log')
        
        
    #mypalette=Spectral11[0:len(processes)]

    i = 0

    def get_ids(x):
         ids = x[0].split('/')
         ids[2] = int(ids[2])
         return ids


    ax1.set_prop_cycle(cycler(color=plt.get_cmap('tab20b').colors))


    for key, value in sorted(processes.items(), key=get_ids):
        
        if not args.velocity:
            x = [v.to(unit_energy).magnitude   for v in value[0]]
        else:
            x = [v.to(unit_velocity).magnitude for v in value[0]]
            
        y = [v.to(unit_area).magnitude  if v != 0. else None for v in value[1]]
        
    
        #x, y = zip(*[v for v in zip(x,y) if v[1] != 0])
        ax1.plot(x, y, label=labels[key] ) #, markersize=4., marker='.'
        #ax1.scatter(x, y, label=label, s = 10)
           
        
        i+=1
        
    if args.legend != 'none':
        ax1.legend( ncol=len(processes)//25+1, fontsize='xx-small', bbox_to_anchor=(1.02, 1), loc='upper left')  
    
    fig.tight_layout()

    if args.output is None: 
        plt.show()
    else:  
        print("Saving {}".format(args.output))
        plt.savefig(args.output)


if __name__ == "__main__":
    main()

