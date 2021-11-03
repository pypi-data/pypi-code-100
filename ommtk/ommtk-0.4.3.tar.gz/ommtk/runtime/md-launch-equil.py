if __name__ == '__main__':
    import _pickle as pickle

    import sys
    import os
    from ommtk import GentleHeatSimulation
    import parmed

    if len(sys.argv[1:]) != 2:
        print("Usage: python -m ommtk md-launch-equil.py parmed sim_time_in_ns output_file_prefix")
        exit(1)
    else:
        old_parmed, equil_time, output_file_prefix = sys.argv[1:]

        try:
            with open(old_parmed, 'rb') as handle:
                state = pickle.load(handle)
        except:
            raise

        parmed_structure = parmed.structure.Structure()
        parmed_structure.__setstate__(state)

    heat = GentleHeatSimulation(parmed_structure=sys.argv[1],
                                wrap_all_chains=True,
                                progress_out=sys.stdout,cwd=os.getcwd(),
                                hmr=True
                                )
    heat.minimize()
    new_parmed = heat.run()

    with open(output_file_prefix+'.parmed', 'wb') as handle:
        pickle.dump(new_parmed.__getstate__(), handle)
