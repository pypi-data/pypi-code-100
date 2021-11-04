from matplotlib.pyplot import *
from numpy import *

def Lorentz(x,fr,Q):
    return 1 / (1 + ( 2*Q*(x/fr-1))**2)
def merging(x,y,merge):
    out_x, out_y = [], []
    for i in range(len(x) - merge + 1):
        out_x.append(mean(x[i:i+merge]))
        out_y.append(sum( y[i:i+merge]))
    return array(out_x), array(out_y)

class Glimit:
    def __init__(self):
        self.h      = 6.626e-34 # J/k
        self.h_bar  = 4.135e-15/(2*pi) # ev
        self.k      = 1.38e-23 # J
        self.rho    = 0.45e15   # axion density (GeV/cc)
        self.big_A  = 78e6  #   78Mev
        self.C      = 3e8    # The Speed of light
        self.alpha  = 1/137  # fine structure const
        self.mu     = 4*pi * 1e-7 
        self.e      = 1.6e-19
        self.he     = self.h/self.e
        self.cm     = 0.6527    # one hour (s)

        self.s          = 0      # S₁₁
        self.T          = .3     # physical + noise (k) 
        self.f          = 5e9    # 5Ghz Frequency (10⁹ Hz)
        self.B          = 8      # Magnetic (T)
        self.V          = 120*pi*621e-9 #48338e-9 # Volume (L)
        self.Q          = 25000 # Q factor 
        self.delta_v    = 1000   # 5kHz
        self.delta_w    = 1000   # 5kHz
        self.cooling    = 0
        self.SNR        = 5
        self.beta       = 1
        self.total_time = 86400 * 7
        self.Scanwin    = 2e6
        self.Scanran    = 2e6
        self.Scanshi    = 2e6
        
        self.ksvz_g_gamma = -0.97
        self.dfsz_g_gamma = 0.36
        self.calculate()

    def calculate(self):
        
        self.w         = 2*pi*(self.f)
        self.ma        = self.h_bar * self.w
        self.t         = self.total_time / self.Scanran * self.Scanshi - self.cooling

        assert self.t  > 0,"No time for cooling down"

        self.g_KSVZ    = 0.97 * self.ma * self.alpha /(pi * self.big_A * self.big_A)
        self.Na        = self.delta_v * self.t
        self.Ns        = self.Scanwin/self.Scanshi
        self.sigma     = self.k * self.T * self.delta_w/sqrt(self.Ns * self.Na) 
        
        self.shift =  ((self.h_bar*self.C)**3)*self.rho / (self.ma**2)  * (1/self.mu) * (self.B**2) * \
        self.V * self.w* self.cm * self.Q *self.beta / (1+self.beta)
        
    def cal_single_point(self):
        self.w     = 2*pi*(self.f)
        self.ma    = self.h_bar   * self.w
        self.Na    = self.delta_v * self.t
        self.Ns    = 1
        self.sigma = self.k * self.T * self.delta_w/sqrt(self.Na) 
        self.shift =  ((self.h_bar*self.C)**3)*self.rho / (self.ma**2)  * (1/self.mu) * (self.B**2) * \
        self.V * self.w* self.cm * self.Q *self.beta / (1+self.beta)

    def g_a_gamma(self):
        return sqrt( self.SNR*self.sigma/self.shift) * 1e9
    
    def g_gamma(self):
        return  (pi * self.big_A * self.big_A) * self.g_a_gamma() / self.ma / self.alpha   * 1e-9    
    
    # convert G_a_gamma_gamma to G_gamma
    def to_g_gamma(self,x):
        return (pi * self.big_A * self.big_A) * x / self.ma / self.alpha   * 1e-9

    def to_g_a_gamma(self,x):
        return  x / (pi * self.big_A * self.big_A) * self.ma * self.alpha  * 1e9


    def ksvz_g_a_gamma(self):
        return 0.97 * self.ma * self.alpha /(pi * self.big_A * self.big_A)  * 1e9
        
    def information(self):
        self.calculate()
        print("|","="*18,"Parameter","="*14)
        print(f"| f = {self.f:10.3e} (Frequency [Hz])")
        print(f"| B = {self.B:10.3f} (Magnetic[T])")
        print(f"| V = {self.V:10.3e} (Cavity Volume [L])")
        print(f"| Q = {self.Q:10.3f} (Q factor)")
        print(f"| T = {self.T:10.3f} (Noise temp [k])")
        print(f"| t = {self.t:10.3f} (Integration time [s])")
        print("|","="*18,f"OUR (SNR = {self.SNR:d})","="*10)
        print(f"| g_a_gamma = {self.g_a_gamma() } GeV^-1")
        print(f"| g_gamma   = {self.g_gamma()}")
        print("|","="*18,f"KSVZ (SNR = {self.SNR:d})","="*9)
        print("|",f"ksvz_g_a_gamma = {self.ksvz_g_a_gamma()} GeV^-1")
        print("|",f"ksvz_g_gamma   = {self.ksvz_g_gamma}")
        print("|","="*43)
        print()

    # Find the  scan range and integration time with given target limit
    def find_limit(self,target,show_ = True):
        
        if (show_):
            print("|","="*14,"Parameter","="*18)
            print(f"| f = {self.f:10.3e} (Frequency [Hz])")
            print(f"| B = {self.B:10.3f} (Magnetic[T])")
            print(f"| V = {self.V:10.3e} (Cavity Volume [L])")
            print(f"| Q = {self.Q:10.3f} (Q factor)")
            print(f"| T = {self.T:10.3f} (Noise temp [k])")
            print("|","="*43)
            print("\n")
            print("[*] Total time : ",self.total_time)
            print("[*] Seaching limit :",target ,"times KSVZ limit")

        def start_exp(scan_shfit):
            spectrum    = zeros(int((scan_range + scan_windos)//grid_unit))
            weight      = zeros(int((scan_range + scan_windos)//grid_unit))
            sigma       = zeros(int((scan_range + scan_windos)//grid_unit))
            shift_index = int(scan_shfit/grid_unit)
            start_index = 0
            
            f_now = f_start
            noise        = random.normal(0,1,windo_index)
            while f_now <= f_end:
                noise        = np.zeros(windo_index) + 1#0.2
                scan_f       = linspace(f_now - scan_windos/2, f_now + scan_windos/2, windo_index)

                sigma_this   = 1 + 0 * scan_f

                noise        = noise      / Lorentz(scan_f, f_now, self.Q)
                sigma_this   = sigma_this / Lorentz(scan_f, f_now , self.Q)

                w   = 1 / sigma_this**2

                # w   = Lorentz(scan_f, f_now, self.Q) / sigma_this**2
                
                sig = sigma_this**2 * (w)**2
                
                spectrum[start_index:start_index+windo_index] = spectrum[start_index:start_index+windo_index] + noise*w
                weight[  start_index:start_index+windo_index]   = weight[start_index:start_index+windo_index] + w
                sigma[   start_index:start_index+windo_index]    = sigma[start_index:start_index+windo_index] + sig
                
                f_now       += scan_shfit
                start_index += shift_index

            outpur = [linspace(f_start, f_end, int((scan_range + scan_windos)//grid_unit)),
              np.divide(spectrum, weight, out=np.zeros_like(spectrum)+1, where=sqrt(sigma)!=0),
             np.divide(sqrt(sigma),weight, out=np.zeros_like(spectrum)+1, where=sqrt(sigma)!=0)]
    
            return outpur

        grid_unit   = 1e3
        f_start     = self.f - 200e3*100
        f_end       = self.f + 200e3*100
        scan_windos = self.Scanwin
        windo_index = int(scan_windos/grid_unit)
        scan_range  = f_end - f_start
        start_index = int((scan_windos/2) / grid_unit)
        end_index   = start_index + int(scan_range / grid_unit)

        x,spec, sigm = start_exp(self.f / self.Q / 2)
        # print(spec,sigm)

        _, spec = merging(x,spec,5)
        x, sigm = merging(x,sigm**2,5)
        # sigm    = sigm * 5 

        self.delta_w = 1000 
        y = np.divide(spec, sqrt(sigm), out=np.zeros_like(spec), where=sqrt(sigm)!=0)
        self.t = 600*60
        self.cal_single_point()

        with np.errstate(divide='ignore'):
            g_a_gamma = sqrt(self.sigma*sqrt(sigm)*5/self.shift) * 1e9

        g_gamma = self.to_g_gamma(g_a_gamma)

        #  (pi * self.big_A * self.big_A) * g_a_gamma / self.ma / self.alpha   * 1e-9
        # print(min(g_gamma/0.97))

        new_t = self.t * ( min(g_gamma/0.97) / target)  **4
        if (show_):
            print(f"[*] Founded Answer :")
            print(f"\t Integration : {(new_t/60):7.2f} [minutes] to reach {target} times KSVZ limit")
            print(f"\t Cold down   : {self.cooling:7.2f} [seconds]")
            print(f"\t Total time  : {self.total_time/3600:7.2f} [hours]")
            print(f"\t Step size   : {self.f / self.Q / 2*1e-3:7.2f} [kHz]")
            print(f"\t Move rod    : {self.total_time / (new_t + self.cooling):7.2f} [steps] (should be a convert to a integer)")
            print(f"\t Total scan  : {self.total_time / (new_t + self.cooling) * self.f / self.Q / 2*1e-6:7.2f} [MHz]")
        
        
        self.Scanshi = self.f / self.Q / 2
        self.Scanran = self.total_time / (new_t + self.cooling) * self.f / self.Q / 2
        self.t = new_t

        assert new_t < self.total_time ,"Integration time is larger then total time"


        f_start     = self.f - self.f / self.Q / 2*(self.total_time / (new_t + self.cooling)//2)
        f_end       = self.f + self.f / self.Q / 2*(self.total_time / (new_t + self.cooling)//2)
        scan_range  = f_end - f_start
        start_index = int((scan_windos/2) / grid_unit)
        end_index   = start_index + int(scan_range / grid_unit)
        x,spec, sigm = start_exp(self.f / self.Q / 2)
        _, spec = merging(x,spec,5)
        x, sigm = merging(x,sigm**2,5)
        # sigm    = sigm * 5 
        y = np.divide(spec, sqrt(sigm), out=np.zeros_like(spec), where=sqrt(sigm)!=0)

        self.cal_single_point()
        with np.errstate(divide='ignore'):
            g_a_gamma = sqrt(self.sigma*sqrt(sigm)*5/self.shift) * 1e9
        g_gamma = (pi * self.big_A * self.big_A) * g_a_gamma / self.ma / self.alpha   * 1e-9

        output_answer = {
        "Integration[s]"  : new_t ,
        "step size[kHz]"  : self.f / self.Q / 2*1e-3 ,
        "Move rod"        : self.total_time / (new_t + self.cooling) ,
        "Total scan[MHz]" : self.total_time / (new_t + self.cooling) * self.f / self.Q / 2*1e-6,
        "g_a_gamma"       : g_a_gamma,
        "g_gamma"         : g_gamma
        }


        if (show_):
            figure()
            max_ratio = min(g_gamma/0.97)
            title(f"Best value : {max_ratio:.3f} ")
            plot(x*1e-9,g_gamma/0.97,label="This experiment")

            plot(x*1e-9,abs(self.ksvz_g_gamma +x*0)/0.97,"b--",label="KSVZ")
            plot(x*1e-9,abs(self.dfsz_g_gamma +x*0)/0.97,"r--",label="DFSZ")
            upper = 4
            down  = abs(self.dfsz_g_gamma +x*0)/abs(self.ksvz_g_gamma) / 4
            fill_between(x*1e-9,upper,down,color="yellow",label="model region")

            xlabel(f"Freq [GHz]")
            ylabel(r"$\frac{G_\gamma}{G_{KSVZ}}$",size=20)
            xlim(min(x*1e-9),max(x*1e-9))
            tight_layout()
            grid()
            gcf().autofmt_xdate()
            legend()
            tight_layout()
            show()
        return output_answer

    def find_span(self,show_=True):
        if (show_):
            print("|","="*14,"Parameter","="*18)
            print(f"| f = {self.f:10.3e} (Frequency [Hz])")
            print(f"| B = {self.B:10.3f} (Magnetic[T])")
            print(f"| V = {self.V:10.3e} (Cavity Volume [L])")
            print(f"| Q = {self.Q:10.3f} (Q factor)")
            print(f"| T = {self.T:10.3f} (Noise temp [k])")
            print("|","="*43)
            print("\n")
            print(f"[*] Total time  : {self.total_time/3600/24:7.2f} [Days]")
            print(f"[*] Integration : {self.t/60:7.2f} [minutes]")
            print(f"[*] Step size   : {self.Scanshi/1e3:7.2f} [KHz]")
            print(f"[*] Cold down   : {self.cooling/60:7.2f} [minutes]")
            print(f"[*] Move rod    : {self.total_time/(self.t+self.cooling):7.2f} [steps] (should be a convert to a integer)")
            print(f"[*] Total scan  : {self.total_time/(self.t+self.cooling) * self.Scanshi * 1e-6:7.2f} [MHz]")

        def start_exp(scan_shfit):
            spectrum    = zeros(int((scan_range + scan_windos)//grid_unit))
            weight      = zeros(int((scan_range + scan_windos)//grid_unit))
            sigma       = zeros(int((scan_range + scan_windos)//grid_unit))
            shift_index = int(scan_shfit/grid_unit)
            start_index = 0
            
            f_now = f_start
            noise        = random.normal(0,1,windo_index)
            while f_now <= f_end:
                noise        = np.zeros(windo_index) + 0.2
                scan_f       = linspace(f_now - scan_windos/2, f_now + scan_windos/2, windo_index)
                
                sigma_this   = 1 + 0 * scan_f

                noise        = noise      / Lorentz(scan_f, f_now, self.Q)
                sigma_this   = sigma_this / Lorentz(scan_f, f_now , self.Q)

                w   = 1 / sigma_this**2
                sig = sigma_this**2 * (w)**2
                
                spectrum[start_index:start_index+windo_index] = spectrum[start_index:start_index+windo_index] + noise*w
                weight[  start_index:start_index+windo_index]   = weight[start_index:start_index+windo_index] + w
                sigma[   start_index:start_index+windo_index]    = sigma[start_index:start_index+windo_index] + sig
                
                f_now       += scan_shfit
                start_index += shift_index

            outpur = [linspace(f_start, f_end, int((scan_range + scan_windos)//grid_unit)),
              np.divide(spectrum, weight, out=np.zeros_like(spectrum)+1, where=sqrt(sigma)!=0),
             np.divide(sqrt(sigma),weight, out=np.zeros_like(spectrum)+1, where=sqrt(sigma)!=0)]
    
            return outpur


        self.Scanran = self.total_time/(self.t+self.cooling) * self.Scanshi 

        grid_unit   = 1e3
        f_start     = self.f - self.Scanran / 2
        f_end       = self.f + self.Scanran / 2
        scan_windos = self.Scanwin
        windo_index = int(scan_windos/grid_unit)
        scan_range  = f_end - f_start
        start_index = int((scan_windos/2) / grid_unit)
        end_index   = start_index + int(scan_range / grid_unit)

        x,spec, sigm = start_exp(self.Scanshi)
        _, spec = merging(x,spec,5)
        x, sigm = merging(x,sigm**2,5)
        y = np.divide(spec, sqrt(sigm), out=np.zeros_like(spec), where=sqrt(sigm)!=0)

        self.cal_single_point()
        with np.errstate(divide='ignore'):
            g_a_gamma = sqrt(self.sigma*sqrt(sigm)*5/self.shift) * 1e9
        g_gamma = (pi * self.big_A * self.big_A) * g_a_gamma / self.ma / self.alpha   * 1e-9

        output_answer = {
            "Integration[s]"  : self.t ,
            "step size[kHz]"  : self.Scanshi*1e-3 ,
            "Move rod"        : self.total_time / (self.t + self.cooling) ,
            "Total scan[MHz]" : self.Scanran*1e-6,
            "g_a_gamma"       : g_a_gamma,
            "g_gamma"         : g_gamma
        }

        if (show_):
            figure()
            max_ratio = min(g_gamma/0.97)
            title(f"Best value : {max_ratio:.3f} ")
            plot(x*1e-9,g_gamma/0.97,label="This experiment")

            plot(x*1e-9,abs(self.ksvz_g_gamma +x*0)/0.97,"b--",label="KSVZ")
            plot(x*1e-9,abs(self.dfsz_g_gamma +x*0)/0.97,"r--",label="DFSZ")
            upper = 4
            down  = abs(self.dfsz_g_gamma +x*0)/abs(self.ksvz_g_gamma) / 4
            fill_between(x*1e-9,upper,down,color="yellow",label="model region")

            xlabel(f"Freq [GHz]")
            ylabel(r"$\frac{G_\gamma}{G_{KSVZ}}$",size=20)
            xlim(min(x*1e-9),max(x*1e-9))
            tight_layout()
            grid()
            gcf().autofmt_xdate()
            legend()
            tight_layout()
            show()
        return output_answer

    def limit_freq_par(self,args,show_=True):
        if ("freq" not in args):
            raise ValueError("no freq found in args")

        freq = args["freq"]

        if ("Q" in args):
            if (len(args["Q"]) != len(args["freq"])):
                raise ValueError(f"Q len { len(args['Q'])} is not same as freq {len(args['freq'])}")
            get_Q = lambda x:np.interp(x, freq, args["Q"])
            if (show_):
                figure()
                title(r"$Q_L$")
                plot(freq*1e-9, args["Q"])
                xlabel("freq [GHz]")
                grid()
        else:
            get_Q = lambda x:self.Q

        if ("beta" in args):
            if (len(args["beta"]) != len(args["freq"])):
                raise ValueError(f"beta len { len(args['beta'])} is not same as freq {len(args['freq'])}")
            get_b = lambda x:np.interp(x, freq, args["beta"])
            if (show_):
                figure()
                title(r"$\beta$")
                plot(freq*1e-9, args["beta"])
                xlabel("freq [GHz]")
                grid()
        else:
            get_b = lambda x:self.beta

        if ("T" in args):
            if (len(args["T"]) != len(args["freq"])):
                raise ValueError(f"T len { len(args['T'])} is not same as freq {len(args['freq'])}")
            get_T = lambda x:np.interp(x, freq, args["T"] )
            if (show_):
                figure()
                title(r"$Adding noise$")
                plot(freq*1e-9, args["T"])
                xlabel("freq [GHz]")
                grid()
        else:
            get_T = lambda x:self.T

        grid_unit   = 1e3
        f_start     = freq[0]
        f_end       = freq[-1]
        scan_windos = 2e6
        windo_index = int(scan_windos/grid_unit)
        scan_range  = f_end - f_start
        start_index = int((scan_windos/2) / grid_unit)
        end_index   = start_index + int(scan_range      / grid_unit)
        def start_exp(scan_shfit):
            spectrum    = zeros(int((scan_range + scan_windos)//grid_unit))
            weight      = zeros(int((scan_range + scan_windos)//grid_unit))
            sigma       = zeros(int((scan_range + scan_windos)//grid_unit))
            shift_index = int(scan_shfit/grid_unit)
            start_index = 0
            
            f_now = f_start
            noise        = random.normal(0,1,windo_index)
            while f_now <= f_end:
                noise        = np.zeros(windo_index) +1
                scan_f       = linspace(f_now - scan_windos/2, f_now + scan_windos/2, windo_index)
                sigma_this   = 1 + 0 * scan_f

                noise        = noise      / Lorentz(scan_f, f_now, self.Q)
                sigma_this   = sigma_this / Lorentz(scan_f, f_now , self.Q)

                w   = 1 / sigma_this**2
                sig = sigma_this**2 * (w)**2
                
                spectrum[start_index:start_index+windo_index] = spectrum[start_index:start_index+windo_index] + noise*w
                weight[  start_index:start_index+windo_index]   = weight[start_index:start_index+windo_index] + w
                sigma[   start_index:start_index+windo_index]    = sigma[start_index:start_index+windo_index] + sig
                
                f_now       += scan_shfit
                start_index += shift_index
            outpur = [linspace(f_start, f_end, int((scan_range + scan_windos)//grid_unit)),
              np.divide(spectrum, weight, out=np.zeros_like(spectrum)+1, where=sqrt(sigma)!=0),
             np.divide(sqrt(sigma),weight, out=np.zeros_like(spectrum)+1, where=sqrt(sigma)!=0)]
    
            return outpur


        x,spec, sigm = start_exp(g.Scanshi)
        _, spec = merging(x,spec,5)
        x, sigm = merging(x,sigm**2,5)
        y = np.divide(spec, sqrt(sigm), out=np.zeros_like(spec), where=sqrt(sigm)!=0)

        this_shift = []
        this_sigma = []
        for each_x in x:
            self.Q    = get_Q(each_x)
            self.T    = get_t(each_x)
            self.beta = get_b(each_x)
            self.cal_single_point()
            this_shift.append(g.shift)
            this_sigma.append(g.sigma)
            
        this_shift = array(this_shift)
        this_sigma = array(this_sigma)
        g_a_gamma = sqrt(this_sigma*sqrt(sigm)*5/this_shift) * 1e9
        g_gamma = self.to_g_gamma(g_a_gamma)

        figure(figsize=(8,6))
        max_ratio = min(g_gamma/0.97)
        title(f"Best value : {max_ratio:.3f} ")
        plot(x*1e-9,g_gamma/0.97,label="This experiment")

        plot(x*1e-9,abs(g.ksvz_g_gamma +x*0)/0.97,"b--",label="KSVZ")
        plot(x*1e-9,abs(g.dfsz_g_gamma +x*0)/0.97,"r--",label="DFSZ")
        upper = 4
        down  = abs(g.dfsz_g_gamma +x*0)/abs(g.ksvz_g_gamma) / 4
        fill_between(x*1e-9,upper,down,color="yellow",label="model region")

        xlabel(f"Freq [GHz]")
        ylabel(r"$\frac{G_\gamma}{G_{KSVZ}}$",size=20)
        xlim(min(x*1e-9),max(x*1e-9))
        tight_layout()
        grid()
        gcf().autofmt_xdate()
        legend()

if __name__ == "__main__":
    g = Glimit()
    g.B    = 7.8
    g.Q    = 20000
    g.T    = 2
    g.total_time = 14 * 24 * 3600
    g.SNR  = 5
    g.f    = 5e9
    g.beta = 2
    g.cooling = 5 * 60
    g.delta_w = 1000
    g.delta_v = 1000
    # g.information()
    # print(g.to_g_gamma(1.3e-13))

    print(min(g.find_limit(10,1)["g_a_gamma"]))

    g.t   = 32*60
    g.Scanshi = 115e3
    print(g.find_span(1))

    # g.limit_freq_par({"freq":[1],"Q":[1,2]})