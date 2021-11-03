import os
import pickle
import random
import re

import mdtraj
import numpy as np
from scipy.spatial import distance


from simtk.openmm import unit

from .ommtk import MetadynamicSimulation
from .utils import calc_coverage, moving_average,get_minimum_path_trajectory


class SegmentMappingSim(MetadynamicSimulation):
    """
    This is a specialized version of the metaD simulation that runs a short run with a high bias,
    saves the coordinates and CV values and uses them to seed a forced sampling of the unbinding pathway
    (without previous knowledge of needed restraints. It begins a run with scan bias, and continues in .5ns
    intervals until the distance CV has reached the value of the unbound_distance variable.

    Once the distance is reached, suitable (equidistant in CV distance space) frames are chosen to represent the
    unbinding pathway and used as seeds for a sequential multiple walkers metaD run. If multiple CVs are desired
    one can use the scan_CV_list keyword to submit a list of CV_lists and each scan will use a different CV definition

    Params

    num_segs int
        number of segments along the unbinding pathway to seed
    seg_sim_time unit.Quantity
        length of simulation time to spend in each segment
    scan_bias int
        initial bias_factor for scan portion of the protocol
    scan_time unit.Quantity
        time to run the initial scan
    unbound_distance unit.quantity
        estimate of the max value of the CV. Can be determined using find_max_distance in utils

    """
    def __init__(self, num_segs_per_replica = 10, scan_bias=40,
                 scan_time = 1 * unit.nanosecond, scan_bias_freq= 1 * unit.picosecond,
                 max_scan_time=6 * unit.nanosecond, prod_bias=5, prod_bias_freq = 1 * unit.picosecond,
                 scan_bias_height=2.5 * unit.kilojoules_per_mole, prod_bias_height= 2 * unit.kilojoule_per_mole,
                 num_replicas=1, CV2_target_range = None,
                 time_per_iteration =10 * unit.nanosecond,
                 run_scans=True, run_production=True, input_scan_times=None, input_segment_coords=None,
                 max_iterations=15, max_coverage_criteria=.5, convergence_criteria=.1,
                 retain_scan_bias=True, scan_CV_list=None,
                 **kwargs):

        super().__init__(**kwargs)


        #setup init vars
        self.num_segs = num_segs_per_replica
        self.scan_bias = scan_bias
        self.scan_time = scan_time
        self.scan_CV_list = scan_CV_list
        self.scan_bias_freq = int(scan_bias_freq/self.step_length)
        self.scan_bias_height = scan_bias_height
        self.max_scan_time = max_scan_time
        self.prod_bias = prod_bias
        self.prod_bias_freq = int(prod_bias_freq/self.step_length)
        self.num_replicas = num_replicas
        self.time_per_iteration = time_per_iteration
        self.prod_bias_height = prod_bias_height
        self.run_scans_bool = run_scans
        self.run_production_bool = run_production
        self.input_scan_times = input_scan_times
        self.input_segment_coords = input_segment_coords
        #TODO come up with better handling of CV2_target range, make it automated as default
        # but still handle the 1CV case
        self.CV2_target_range = CV2_target_range
        self.max_iterations = max_iterations
        self.retain_scan_bias = retain_scan_bias
        self.max_coverage_criteria = max_coverage_criteria
        self.convergence_criteria = convergence_criteria

        #sanity checks
        if not self.run_scans_bool and self.run_production_bool:
            if self.input_segment_coords==None or self.input_scan_times==None:
                raise ValueError("""Must supply input segment coords and input scan times if not running scans 
                but running production""")

        if input_scan_times is not None:
            if not isinstance(input_scan_times, list):
                raise ValueError('input_scan_times should be a list of integers')

        if input_segment_coords is not None:
            if not isinstance(input_segment_coords,list):
                raise ValueError("""input_segment_coords should be a list of lists, 
                where the inner lists are coordinates in nm without units""")

        if scan_CV_list is not None and retain_scan_bias==True:
            print('WARNING, found list of scan CVs but bias is being retained. Be careful about how these runs are interpreted')

        if scan_CV_list is not None:
            if len(scan_CV_list)!=num_replicas:
                raise ValueError('scan_CV_list must be the same length as the number of replicas if used.')


        for cv in self.CV_list:
            if cv[0]=='Distance' and cv[4]<self.unbound_distance:
                self.unbound_distance=cv[4]
                print("""Warning, Distance CV upper bound set to less than unbound distance, replacing
                unbound_distance with max distance CV, new value is {}""".format(cv[4]))

        # if self.CV_list[0][0] not in ['Distance', 'Weighted Distances']:
        #     raise ValueError('Segment Map Sim without distance or weighted distances not yet supported')


        if self.fes_interval != self.traj_interval:
            print('WARNING: traj interval and fes interval are different, CV indices will not match trajectory frames')

    def run_scans(self):

            self._remove_custom_forces()
            self.bias_factor = self.scan_bias
            # self.bias_save_frequency = self.scan_bias_freq * 50
            self.bias_save_frequency = self.scan_bias_freq

            self.bias_frequency = self.scan_bias_freq
            self.initial_bias_height=self.scan_bias_height
            self._build_custom_forces()

            print('saving coords')
            initial_coords = self.positions

            self.scan_times = []
            self.segment_coords = []
            self.dG_traces = []
            self.coverage_traces =[]
            self.CV_traces = []
            for i in range(self.num_replicas):

                if self.retain_scan_bias==False:
                    pattern = re.compile('bias(.*)\.npy')
                    matches = [pattern.match(filename) for filename in os.listdir(self.cwd) if
                               pattern.match(filename) != None]
                    for match in matches:
                        os.remove(os.path.join(self.cwd, match.string))

                self.production_CV_list = self.CV_list
                if self.scan_CV_list is not None:
                    self.CV_list = self.scan_CV_list[i]
                    self._remove_custom_forces()
                    self._build_custom_forces()

                print('Starting scan run for replica {}'.format(i+1))

                self.simulation.context.reinitialize()
                self.simulation.context.setPositions(initial_coords)

                nsteps = int(self.scan_time / self.step_length)

                #fix the reporter intervals to make sure there are enough frames for populating replicas
                #this also ensures that the CV value matches the trajectory frame by index

                self._add_reporters(total_steps=nsteps + self.simulation.currentStep, traj_interval= .01 * unit.nanosecond)
                self._add_FESReporter(fes_interval=.01 * unit.nanosecond)

                self.metaD.step(self.simulation, nsteps)
                self.update_parmed()

                #continually run .5ns runs until distance CV exceeds unbound_distance
                with open(os.path.join(self.cwd, 'CV_values.pickle'), 'rb') as handle:
                    CVs = pickle.load(handle)

                self.CV_traces.append(CVs)

                distances = np.array(CVs)[:, 0]

                scan_clock = self.scan_time

                while all(distances < distances[0]+self.unbound_distance) and  scan_clock<self.max_scan_time:

                    print('failed to unbind, scanning for another .5 ns')
                    print('CV distance range {} to {}'.format(distances[0],np.max(distances)))
                    scan_clock += .5 * unit.nanosecond
                    nsteps = int(.5 * unit.nanosecond / self.step_length)

                    self.metaD.step(self.simulation, nsteps)

                    with open(os.path.join(self.cwd,'CV_values.pickle'), 'rb') as handle:
                        CVs = pickle.load(handle)
                    distances = np.array(CVs)[:, 0]
                else:
                    if scan_clock<self.max_scan_time:
                        self.scan_times.append(scan_clock)
                        print('ligand reached unbinding distance in {}, proceeding with forced sampling'.format(scan_clock))
                    else:
                        self.scan_times.append(scan_clock)
                        print('failed to unbind in max_scan_time, proceeding anyway')

                #get the dG_trace and load it into a master file
                with open(os.path.join(self.cwd, 'dG_trace.pickle'), 'rb') as handle:
                    self.dG_traces.append(pickle.load(handle))

                with open(os.path.join(self.cwd, 'coverage_trace.pickle'), 'rb') as handle:
                    self.coverage_traces.append(pickle.load(handle))

                print('CV1 from scan: {}'.format(distances))

                self.simulation.reporters.clear()

                #turns out the large volume guassians are pretty good at getting the positions of barriers, but not the
                #relative depth of wells. So we take the minimum path (saddle_points) as the segment coords

                with open(os.path.join(self.cwd, 'CV_values.pickle'), 'rb') as handle:
                    CV_trace = pickle.load(handle)

                fes = self.metaD.getFreeEnergy().value_in_unit(unit.kilocalorie_per_mole)

                # load trajectory, fes, and CV_values
                traj = mdtraj.load_hdf5(os.path.join(self.cwd,self.traj_out))

                #TODO come up with hueristic to pick more reliable energy cutoff and order estimate
                saddle_traj, segment_frames = get_minimum_path_trajectory(CV_trace=CV_trace,
                                                             fes=fes,
                                                             order=150,
                                                             CV_list=self.CV_list,
                                                             energy_cutoff=-5,
                                                             frames_per_minima=2,
                                                             traj=traj)

                if saddle_traj is not None:
                    # slice traj for chosen frames
                    self.segment_coords.append(saddle_traj.xyz)
                else:
                    #MFEP detection failed, take random set of frames the old way
                    distance_targets = np.linspace(np.min(distances), self.unbound_distance, self.num_segs)
                    segment_frames = []
                    chosen_CVs = []
                    for k, target in enumerate(distance_targets):
                        idx = (np.abs(distances - target)).argmin()
                        # if idx is already in the list, try 100 times to choose another with similar value
                        counter = 0
                        while idx in segment_frames and counter < 100:
                            counter += 1
                            target += random.randint(-100, 100) * .01
                            idx = (np.abs(distances - target)).argmin()
                        segment_frames.append(idx)
                        chosen_CVs.append(distances[idx])
                        print('choosing CV values {} {}'.format(idx, CVs[idx]))

                    # load trajectory and slice for chosen frames
                    traj = mdtraj.load_hdf5(os.path.join(self.cwd, self.traj_out))
                    self.segment_coords.append(traj.xyz[segment_frames])

                #now we have the coordinates we use for seeding, delete the bias file and previous objects
                pattern = re.compile('bias(.*)\.npy')
                matches = [pattern.match(filename) for filename in os.listdir(self.cwd) if pattern.match(filename)!=None]
                for match in matches:
                    os.remove(os.path.join(self.cwd, match.string))
                self.simulation.reporters.clear()

            with open(os.path.join(self.cwd,'scan_CV_traces.pickle'), 'wb') as handle:
                pickle.dump(self.CV_traces, handle)

            with open(os.path.join(self.cwd,'scan_dG_traces.pickle'), 'wb') as handle:
                pickle.dump(self.dG_traces, handle)

            with open(os.path.join(self.cwd,'scan_coverage_traces.pickle'), 'wb') as handle:
                pickle.dump(self.coverage_traces, handle)

            with open(os.path.join(self.cwd,'segment_coords.pickle'), 'wb') as handle:
                pickle.dump(self.segment_coords, handle)

            with open(os.path.join(self.cwd,'scan_times.pickle'), 'wb') as handle:
                pickle.dump(self.scan_times, handle)

    def cycle_replicas(self, segment_coords, scan_times=None):

        total_scan_time = np.sum(scan_times)

        # for i in range(self.num_production_iterations):
        num_iterations = 0
        coverage = 0
        while coverage<=self.max_coverage_criteria and num_iterations<=self.max_iterations:
            #get coverage first so that there's always one more iteration after coverage is reached
            coverage = calc_coverage(self.metaD.getFreeEnergy().value_in_unit(unit.kilocalorie_per_mole))
            print('coverage is currently {:.2f}%'.format(coverage * 100))
            #loop across all replicas
            for replica in range(self.num_replicas):
                print('starting replica {}'.format(replica+1))
                replica_seg_time= scan_times[replica]* (self.time_per_iteration / (total_scan_time * self.num_segs))
                replica_seg_steps = int(round(replica_seg_time/self.step_length))
                 #loop across the segments with chosen frames running short sims and writing to the bias
                for i,frame in enumerate(segment_coords[replica]):
                    print('replica {}: swapping in coordinates for frame {}'.format(replica+1,i+1))
                    self.simulation.context.setPositions(frame * unit.nanometers)
                    self.metaD.step(self.simulation, replica_seg_steps)
            num_iterations+=1

    def run_production(self):

        #if scans were run from this session we will have segment coords and scan times in memory but otherwise we
        #get them from input statement
        if not self.run_scans_bool:
            self.segment_coords = self.input_segment_coords
            self.scan_times = self.input_scan_times

        #if we used a scan CV we have to reset the production CV
        if self.scan_CV_list is not None:
            self.CV_list = self.production_CV_list

        # remove and rebuild the metaD wrapper force with the new metaD params
        self._remove_custom_forces()
        self.bias_factor = self.prod_bias
        self.bias_save_frequency = self.prod_bias_freq * 100
        self.bias_frequency = self.prod_bias_freq
        self.initial_bias_height = self.prod_bias_height
        self._build_custom_forces()

        #sometimes restarts show instability and lead to hangs on startup so we minimize just to be safe
        self.simulation.minimizeEnergy()

        #get total num steps for reporters
        nsteps = int(round(self.time_per_iteration / self.step_length)) * self.max_iterations
        print('nsteps for production phase',nsteps)
        self.simulation.reporters = []
        self._add_reporters(total_steps = nsteps + self.simulation.currentStep)
        self._add_FESReporter()

        self.cycle_replicas(self.segment_coords,self.scan_times)

        self.simulation.reporters.clear()

        self.update_parmed()


    def run(self):
        """
        Run the segment mapping protocol defined by input variables.

        :return: updated parmed.Structure object
        """

        if self.run_scans_bool:
            self.run_scans()

        if self.run_production_bool:
            self.run_production()
        else:
            self._write_coordinates_to_h5(os.path.join(self.cwd, self.traj_out))
            print("DID NOT RUN PRODUCTION")

        #rename the production traces for rscloud to pick up
        for i in ['dG_trace.pickle', 'coverage_trace.pickle']:
            os.rename(os.path.join(self.cwd,i), os.path.join(self.cwd,'production_{}'.format(i)))

        #check that we have at least one frame in the trajectory
        try:
            mdtraj.load_hdf5(os.path.join(self.cwd, self.traj_out))
        except:
            print('No coordinates in trajectory file')
            self._write_coordinates_to_h5(os.path.join(self.cwd, self.traj_out))

        return self.parmed_structure


class SegmentMappingSimHREMD(SegmentMappingSim):

    def __init__(self, max_production_time=60 * unit.nanosecond, min_production_time = 5 * unit.nanosecond,
                 swap_freq = 2 * unit.nanosecond, convergence_window=2 * unit.nanosecond,
                 dG_displacement_criteria = 1, min_coverage_criteria=.25,
                 **kwargs):
        self.min_production_time = min_production_time
        self.max_production_time = max_production_time
        self.swap_freq = swap_freq
        self.convergence_window = convergence_window
        self.dG_displacement_criteria = dG_displacement_criteria
        self.min_coverage_criteria = min_coverage_criteria


        super().__init__(**kwargs)

    def run_production(self):

        #if scans were run from this session we will have segment coords and scan times in memory but otherwise we
        #get them from input statement
        if not self.run_scans_bool:
            self.segment_coords = self.input_segment_coords
            self.scan_times = self.input_scan_times

        #if we used a scan CV we have to reset the production CV
        if self.scan_CV_list is not None:
            self.CV_list = self.production_CV_list

        # remove and rebuild the metaD wrapper force with the new metaD params
        self._remove_custom_forces()
        self.bias_factor = self.prod_bias
        self.bias_save_frequency = self.prod_bias_freq * 100
        self.bias_frequency = self.prod_bias_freq
        self.initial_bias_height = self.prod_bias_height
        self._build_custom_forces()

        #sometimes restarts show instability and lead to hangs on startup so we minimize just to be safe
        self.simulation.minimizeEnergy()

        #get total num steps for reporters
        nsteps = int(self.max_production_time / self.step_length)
        self.simulation.reporters = []
        self._add_reporters(total_steps = nsteps + self.simulation.currentStep)
        #once again we fix the FES Reporter freq to ensure convergence detection works
        self._add_FESReporter()

        self.cycle_replicas(self.segment_coords)

        self.simulation.reporters.clear()

        self.update_parmed()

    def cycle_replicas(self, segment_coords):

        steps_per_swap_attempt = int(self.swap_freq/self.step_length)

        #segment coords are a list of frames, each replica

        sim_time=0 * unit.nanosecond
        accepted = 0
        attempted = 0
        dG_std = 100
        dG_displacement = 100
        counter = 0
        continue_simulating=True

        while continue_simulating:

            #run the sim
            counter+=1
            self.metaD.step(self.simulation, steps_per_swap_attempt)
            sim_time += self.swap_freq
            #get current coords and energy
            state = self.simulation.context.getState(getEnergy=True,getPositions=True)
            current_positions = state.getPositions()
            current_energy = state.getPotentialEnergy()

            #load in new coordinates and get the new energy
            chosen_replica = np.random.randint(len(segment_coords))
            chosen_frame_index =  np.random.randint(len(segment_coords[chosen_replica]))
            proposed_frame = segment_coords[chosen_replica][chosen_frame_index]
            self.simulation.context.setPositions(proposed_frame * unit.nanometers)
            proposed_energy = self.simulation.context.getState(getEnergy=True).getPotentialEnergy()
            log_p_accept = proposed_energy-current_energy
            current_cv_values = self.metaD.getCollectiveVariables(self.simulation)
            if counter%10==0:
                print('chose replica',chosen_replica, ' frame ',chosen_frame_index)
                print('current cv1 distance', current_cv_values)
            #compare deltaU of swap and normalize high energy probability of acceptance by 2.5 (energy of room temp in kJ/mol)
            if log_p_accept<=0 * unit.kilojoules_per_mole \
                    or random.random() < np.exp(-(log_p_accept/2.494341741366065).value_in_unit(unit.kilojoule_per_mole)):
                accepted +=1
                attempted +=1
            else:
                attempted+=1
                self.simulation.context.setPositions(current_positions)
            print('HREMD acceptance rate {}'.format(accepted/attempted))

            if len(self.CV_list)>1:
                #calc coverage, dG_std and detect convergence
                coverage = calc_coverage(self.metaD.getFreeEnergy().value_in_unit(unit.kilocalorie_per_mole))
                print('coverage is currently {:.2f}%'.format(coverage * 100))
                with open(os.path.join(self.cwd,'dG_trace.pickle'),'rb') as handle:
                    dG_trace = pickle.load(handle)

                #get the rolling average dG displacement and variance of the production dG value trace over a limited range
                window_steps = np.max([1,int(int(self.convergence_window / self.step_length)/int(self.fes_interval/self.step_length))])
                # print('window steps, len(dG-trace)',window_steps,len(dG_trace))

                if len(dG_trace)>window_steps:
                    window_trace = dG_trace[len(dG_trace)-window_steps:]
                    dG_std = np.std(window_trace)
                    print('dG_std over the last {}: {}'.format(self.convergence_window,dG_std))
                    m_ave = moving_average(window_trace, np.max([1,int(len(window_trace)/3)]))
                    dG_displacement = np.max(m_ave) - np.min(m_ave)
                    print('dG_displacement over the last {}: {}'.format(self.convergence_window,dG_displacement))

                #convergence detected when there is significant coverage and dG std and dG rolling average displacement is low
                if coverage > self.min_coverage_criteria and \
                    sim_time > self.min_production_time and \
                    dG_std < self.convergence_criteria and \
                    dG_displacement < self.dG_displacement_criteria:
                    print("""convergence detected! Final dG {}:, coverage 
                          {}, dG_std: {}, dG_displacement: {}""".format(dG_trace[-1],coverage * 100,dG_std,dG_displacement))
                    continue_simulating= False

            #or complete when max time is hit
            if sim_time>=self.max_production_time:
                print('hit max sim time')
                continue_simulating = False

