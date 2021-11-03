if __name__ == '__main__':
    import _pickle as pickle

    import sys
    import os
    from ommtk import MDSimulation
    from parmed import unit
    import parmed

    if len(sys.argv[1:]) != 4:
        print("Usage: python md-launch-equil.py parmed sim_time_in_ns traj_frequency_in_ns output_file_prefix")
        exit(1)
    else:
        old_parmed, run_time, save_freq, output_file_prefix = sys.argv[1:]
        save_freq = int(save_freq)

        try:
            with open(old_parmed, 'rb') as handle:
                state = pickle.load(handle)
        except:
            raise

        parmed_structure = parmed.structure.Structure()
        parmed_structure.__setstate__(state)

    mdsim = MDSimulation(parmed_structure=old_parmed,
                        wrap_all_chains=True,
                        progress_out=sys.stdout, progress_interval=.5 * unit.nanosecond, cwd=os.getcwd(),
                        hmr=True, traj_interval=save_freq * unit.nanosecond, traj_out=output_file_prefix+'_traj.h5'
                        )
    new_parmed = mdsim.run(run_time * unit.nanoseconds)

    with open(output_file_prefix+'.parmed', 'wb') as handle:
        pickle.dump(new_parmed.__getstate__(), handle)
