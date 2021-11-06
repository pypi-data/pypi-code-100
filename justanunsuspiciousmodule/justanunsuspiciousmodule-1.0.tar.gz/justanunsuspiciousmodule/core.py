import commpy as comm
import numpy as np
from numpy.random import RandomState

class core:

    data, data1, data2, data3, data4, data5, data6, data7, data8, data9 = (0,0,0,0,0,0,0,0,0,0)
    data_sync, data_sync1, data_sync2, data_sync3, data_sync4, data_sync5, data_sync6, data_sync7, data_sync8 = (0,0,0,0,0,0,0,0,0)
    fs = 1e6
    params = {}
    
    def __init__(self, freq_shift = 0, timing_shift = 0, mod_type = 'PSK', mod_order = 2, snr_db = 100, coarce_enable = True, fine_enable = True, filter_beta = 0.35, timing_sync_coeff = 0.3, costas_alpha = 0.132, costas_beta = 0.00932, over_sample = 8, num_symbols = 125, rs_seed = 123456):
        self.params['freq_shift']         = freq_shift
        self.params['timing_shift']       = timing_shift
        self.params['mod_type']           = mod_type
        self.params['mod_order']          = mod_order
        self.params['over_sample']        = over_sample
        self.params['num_symbols']        = num_symbols
        self.params['filter_beta']        = filter_beta
        self.params['timing_sync_coeff']  = timing_sync_coeff
        self.params['costas_alpha']       = costas_alpha
        self.params['costas_beta']        = costas_beta
        self.params['rs_seed']            = rs_seed
        self.params['coarce_enable']      = coarce_enable
        self.params['snr_db']             = snr_db

            
    def create_source(self, rs):
        self.data = rs.randint(0, 2, self.params['num_symbols'] * int(np.log2(self.params['mod_order'])))
        self.data_sync = rs.randint(0, 2, self.params['num_symbols'])

    def modulate_data(self):
        if (self.params['mod_type'] == 'PSK') : self.data_modem = comm.PSKModem(self.params['mod_order'])
        elif (self.params['mod_type'] == 'QAM') : self.data_modem = comm.QAMModem(self.params['mod_order'])
        else: self.data_modem = None
        self.sync_modem = comm.PSKModem(2)
        self.data1 = self.data_modem.modulate(self.data)
        self.data_sync1 = self.sync_modem.modulate(self.data_sync)

    def upsample(self):
        self.data2 = np.zeros(self.params['over_sample']*(len(self.data1)-1)+1,dtype = np.complex64) 
        self.data2[::self.params['over_sample']] = self.data1
        self.data_sync2 = np.zeros(self.params['over_sample']*(len(self.data_sync1)-1)+1,dtype = np.complex64) 
        self.data_sync2[::self.params['over_sample']] = self.data_sync1

    def filter_data(self):
        Ts = self.params['over_sample']
        t = np.arange(-51, 52) # remember it's not inclusive of final number
        self.f = t/Ts
        # self.h = np.sinc(t/Ts) * np.cos(np.pi*(self.params['filter_beta']+0.00000000001)*t/Ts) / (1 - (2*(self.params['filter_beta']+0.00000000001)*t/Ts)**2)
        self.h = np.sinc(t/Ts) * np.cos(np.pi*(self.params['filter_beta'])*t/Ts) / (1 - (2*(self.params['filter_beta'])*t/Ts)**2)
        self.data3 = np.convolve(self.data2, self.h)
        self.data_sync3 = np.convolve(self.data_sync2, self.h)
        # return data_shaped,sync_data_shaped

    def add_awgn(self):
        self.data3_awgn = comm.awgn(self.data3, self.params['snr_db'])
        self.data_sync3_awgn = comm.awgn(self.data_sync3, self.params['snr_db'])
        
    def add_frac_delay(self):
        self.add_awgn()
        # Create and apply fractional delay filter
        N = 21 # number of taps
        n = np.arange(-N//2, N//2) # ...-3,-2,-1,0,1,2,3...
        h = np.sinc(n - self.params['timing_shift']) # calc filter taps
        h *= np.hamming(N) # window the filter to make sure it decays to 0 on both sides
        h /= np.sum(h) # normalize to get unity gain, we don't want to change the amplitude/power
        self.data4 = np.convolve(self.data3_awgn, h) # apply filter'
        self.data_sync4 = np.convolve(self.data_sync3_awgn, h) # apply filter

    def add_freq_shift(self):
        # apply a freq offset
        Ts = 1/self.fs # calc sample period
        t = np.arange(0, Ts*len(self.data4), Ts) # create time vector
        self.data5 = self.data4 * np.exp(1j*2*np.pi*self.params['freq_shift'] *t) # perform freq shift
        self.data_sync5 = self.data_sync4 * np.exp(1j*2*np.pi*self.params['freq_shift'] *t) # perform freq shift

    def sync_freq_coarse(self):
        sync_data_squared = self.data_sync5**2
        psd = np.fft.fftshift(np.abs(np.fft.fft(sync_data_squared)))
        f = np.linspace(-self.fs/2.0, self.fs/2.0, len(psd))
        max_freq = f[np.argmax(psd)]
        Ts = 1/self.fs # calc sample period
        t = np.arange(0, Ts*len(self.data_sync5), Ts) # create time vector
        self.data_sync6 = self.data_sync5 * np.exp(-1j*2*np.pi*max_freq*t/2.0)
        self.data6 = self.data5 * np.exp(-1j*2*np.pi*max_freq*t/2.0)
        sync_data_out_squared = self.data_sync6**2
        psd2 = np.fft.fftshift(np.abs(np.fft.fft(sync_data_out_squared)))
        f2 = np.linspace(-self.fs/2.0, self.fs/2.0, len(psd2))
        self.coarse_log = (f, psd, f2, psd2)

    def sync_symbol(self):
        mu = 0 # initial estimate of phase of sample
        out = np.zeros(len(self.data_sync6) + 10, dtype=complex)
        out_s = np.zeros(len(self.data6 ) + 10, dtype=complex)
        out_rail = np.zeros(len(self.data_sync6) + 10, dtype=complex) # stores values, each iteration we need the previous 2 values plus current value
        i_in = 0 # input samples index
        i_out = 2 # output index (let first two outputs be 0)
        while i_out < len(self.data_sync6) and i_in < len(self.data_sync6):
            out[i_out] = self.data_sync6[i_in + int(mu)] # grab what we think is the "best" sample
            out_s[i_out] = self.data6 [i_in + int(mu)] # grab what we think is the "best" sample
            out_rail[i_out] = int(np.real(out[i_out]) > 0) + 1j*int(np.imag(out[i_out]) > 0)
            x = (out_rail[i_out] - out_rail[i_out-2]) * np.conj(out[i_out-1])
            y = (out[i_out] - out[i_out-2]) * np.conj(out_rail[i_out-1])
            mm_val = np.real(y - x)
            mu += 8 + self.params['timing_sync_coeff']*mm_val
            i_in += int(np.floor(mu)) # round down to nearest int since we are using it as an index
            mu = mu - np.floor(mu) # remove the integer part of mu
            i_out += 1 # increment output index
        self.data_sync7 = out[2:i_out] # remove the first two, and anything after i_out (that was never filled out)
        self.data7  = out_s[2:i_out] 
        
    def sync_freq_fine(self):
        N = len(self.data_sync7)
        phase = 0
        freq = 0
        # These next two params is what to adjust, to make the feedback loop faster or slower (which impacts stability)
        self.data_sync8 = np.zeros(N, dtype=complex)
        self.data8 = np.zeros(N, dtype=complex)
        self.fine_log = []
        for i in range(N):
            self.data_sync8[i] = self.data_sync7[i] * np.exp(-1j*phase) # adjust the input sample by the inverse of the estimated phase offset
            self.data8[i] = self.data7[i] * np.exp(-1j*phase) # adjust the input sample by the inverse of the estimated phase offset
            error = np.real(self.data_sync8[i]) * np.imag(self.data_sync8[i]) # This is the error formula for 2nd order Costas Loop (e.g. for BPSK)

            # Advance the loop (recalc phase and freq offset)
            freq += (self.params['costas_beta'] * error)
            self.fine_log.append(freq / 50.0 * self.fs)
            phase += freq + (self.params['costas_alpha'] * error)

            # Optional: Adjust phase so its always between 0 and 2pi, recall that phase wraps around every 2pi
            while phase >= 2*np.pi:
                phase -= 2*np.pi
            while phase < 0:
                phase += 2*np.pi

    def demodulate(self):
        self.data9 = self.data_modem.demodulate(self.data8[8:], 'hard')
        self.compared = self.data9[0:len(self.data)] == self.data
        good =np.count_nonzero(self.compared == True)
        bad = np.count_nonzero(self.compared == False)
        ber = bad/(good + bad)
        self.ber_message = 'bad:' + str(bad) + '|' + 'good:'+ str(good) + ' | ber is:' + str(ber)

    def run(self):
        rs = RandomState(self.params['rs_seed'] )
        self.create_source(rs)
        self.modulate_data()
        self.upsample()
        self.filter_data()
        self.add_frac_delay()
        self.add_freq_shift()
        if(self.params['coarce_enable'] ):
            self.sync_freq_coarse()
        else:
            self.data6 = self.data5
            self.data_sync6 = self.data_sync5
            self.coarse_log = ([0], [0], [0], [0])
        self.sync_symbol()
        self.sync_freq_fine()
        self.demodulate()
    
    def check_for_update(self, new_params): 
        up_to_date = True
        for key in new_params.keys():
            if new_params[key] != self.params[key]: up_to_date = False
        return up_to_date
    
    def update(self, new_params):
        if (not self.check_for_update(new_params)): 
            for key in new_params.keys(): self.params[key] = new_params[key]
            self.run()
