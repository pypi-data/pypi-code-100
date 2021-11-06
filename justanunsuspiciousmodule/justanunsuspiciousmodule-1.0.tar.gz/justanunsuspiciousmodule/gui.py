
import numpy as np
from matplotlib import pyplot as plt
from core import core
# %matplotlib inline
# Prevents the pop-up graphs in a separate window.
get_ipython().run_line_magic('matplotlib', 'inline')

from ipywidgets import Tab 
from ipywidgets import fixed, Layout
from ipywidgets import widgets
class GUI:
    modulation_to_param = {
    'BPSK'      : ('PSK', 2),
    'QPSK'      : ('PSK', 4),
    'PSK-16'    : ('PSK', 16),
    'PSK-32'    : ('PSK', 32),
    'PSK-64'    : ('PSK', 64),
    'PSK-128'   : ('PSK', 128),
    'PSK-256'   : ('PSK', 256),
    'PSK-512'   : ('PSK', 512),
    'QAM-4'     : ('QAM', 4),
    'QAM-16'    : ('QAM', 16),
    'QAM-64'    : ('QAM', 64),
    'QAM-128'   : ('QAM', 256),
    }
    
    def __init__(self):
        self.core = core()
        self.core.run()

    def sir_interactive_func(self, freq_shift, timing_shift, mod , filter_beta, timing_sync_coeff, costas_alpha, costas_beta, coarce_enable, snr_db,  show_filtered_psd, plot_domain = 'time', plot_type = 'Source'):
        mod_type, mod_order = self.modulation_to_param[mod]
        params = {}
        params['freq_shift']         = freq_shift
        params['timing_shift']       = timing_shift
        params['mod_type']           = mod_type
        params['mod_order']          = mod_order
        params['filter_beta']        = filter_beta
        params['timing_sync_coeff']  = timing_sync_coeff
        params['costas_alpha']       = costas_alpha
        params['costas_beta']        = costas_beta
        params['coarce_enable']      = coarce_enable
        params['snr_db']             = snr_db
        self.core.update(params)

        if (plot_domain == 'time'):
            if plot_type == 'Source':
                f, axs = plt.subplots(2,1,figsize=(30,10))
                axs[0].set_title('Сгенерированные биты')
                axs[0].plot(range( self.core.data.shape[0]), self.core.data, '-*g' )
                axs[0].grid()
                axs[1].set_title('Модулированный сигнал')
                axs[1].plot(range( self.core.data1.real.shape[0]),  self.core.data1.real,'-*g' ,  self.core.data1.imag, '-*b' )
                axs[1].legend(['I', 'Q'])
                axs[1].grid()  
            
            elif plot_type == 'Filtered':
                if(show_filtered_psd):
                    f, axs = plt.subplots(2,1,figsize=(30,10))
                    axs[0].set_title('PSD сигнала до и  после формирующего фильтра')
                    axs[0].psd(self.core.data3)
                    axs[0].psd(self.core.data1)
                    axs[0].grid()
                else:
                    f, axs = plt.subplots(2,1,figsize=(30,10))
                    axs[0].set_title('Передискретизированный сигнал')
                    axs[0].plot(range(self.core.data2.real.shape[0]), self.core.data2.real, '-*g' )
                    axs[0].grid()
                axs[1].set_title('Сигнал после формирующего фильтра')
                axs[1].plot(range(self.core.data3.real.shape[0]), self.core.data3.real, '-*g' )
                axs[1].plot(np.arange(self.core.data1.real.shape[0])*self.core.params['over_sample']+51, self.core.data1.real, '*b' )   
                axs[1].legend(['Сигнал на выходе фильтра', 'Исходные отсчеты (с добавленной задержкой фильтров)'])
                axs[1].grid()  

            elif plot_type == 'Imparameters':
                f, axs = plt.subplots(2,1,figsize=(30,10))
                axs[0].set_title('Сигнал с фракционной задержкой') 
                axs[0].plot(np.arange(self.core.data3.real.shape[0])+11, self.core.data3.real, '-*r' )  
                axs[0].plot(range(self.core.data4.real.shape[0]), self.core.data4.real, '-*g' )
                axs[0].legend(['I сигнал до сдвига', 'I после сдвига'])
                axs[0].grid()
                axs[1].set_title('Сигнал со сдвигом по частоте') 
                axs[1].plot(range(self.core.data5.real.shape[0]), self.core.data5.real, '-*g', self.core.data5.imag, '-*b' )
                axs[1].legend(['I', 'Q'])
                axs[1].grid()  

            elif plot_type == 'Coarce_Timing':
                f1, psd1, f2, psd2 = self.core.coarse_log
                max_freq1 = f1[np.argmax(psd1)]
                max_freq2 = f2[np.argmax(psd2)]
                f, axs = plt.subplots(2,1,figsize=(30,10))
                axs[0].set_title('Отклонение частоты при грубой синхронизации')
                axs[0].grid()   
                axs[0].plot(f1, psd1)
                axs[0].plot(f2, psd2)
                arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
                axs[0].annotate(np.around(max_freq1,5), xy=(np.around(max_freq1, 5), psd1[np.argmax(psd1)]*0.95))
                axs[0].annotate(np.around(max_freq2,5), xy=(np.around(max_freq2, 5), psd2[np.argmax(psd2)]))

                axs[1].set_title('Отсчеты сигнала после тактовой синхронизации (реальная часть)') 
                axs[1].plot(np.arange(self.core.data3.real.shape[0])+12, self.core.data3.real[0:], '-*g' )
                a = np.arange(self.core.data7.real.shape[0]) *self.core.params['over_sample']
                axs[1].plot(a, self.core.data7.real[0:], 'or' )
                axs[1].plot(np.arange(self.core.data2.real[self.core.data2.real != 0].shape[0])*self.core.params['over_sample']+64, self.core.data2.real[self.core.data2.real != 0], 'bx' )
                axs[1].legend(['Исходные отсчеты (пересемплированные))', 'Выбранные отсчеты ', 'Отсчеты до пересемплирования'])
                axs[1].grid()

            elif plot_type == 'Fine':
                f, axs = plt.subplots(2,1,figsize=(30,10))
                axs[0].set_title('Отсчеты сигнала после петли Костаса') 
                axs[0].plot(np.arange(self.core.data3.real.shape[0])+12, self.core.data3.real[0:], '-*g' )
                a = np.arange(self.core.data8.real.shape[0]) * self.core.params['over_sample']
                axs[0].plot(a, self.core.data8.real[0:], 'or' )
                axs[0].plot(np.arange(self.core.data2.real[self.core.data2.real != 0].shape[0])*self.core.params['over_sample']+64, self.core.data2.real[self.core.data2.real != 0], 'bx' )
                
                axs[0].grid()
                axs[0].legend(['Исходные отсчеты (пересемплированные))', 'Выбранные отсчеты ', 'Отсчеты до пересемплирования'])
                
                axs[1].set_title('Значение ошибки в петле Костаса') 
                axs[1].plot(self.core.fine_log, '-*g' )
                axs[1].grid()

            elif plot_type == 'Demodulated':
                f, axs = plt.subplots(2,1,figsize=(30,10), sharex=True)
                axs[0].set_title('Исходеные  биты') 
                axs[0].plot(np.arange(len(self.core.data)), self.core.data, '-*r' )           
                axs[0].grid()

                axs[1].set_title('Демодулированные биты') 
                axs[1].plot(np.arange(len(self.core.data)), self.core.data9[0:len(self.core.data)], '-*g' )
                axs[1].grid()
                self.ber.value = self.core.ber_message
        else:
            if plot_type == 'Source':
                f, axs = plt.subplots(1,1,figsize=(30,10))
                axs.set_title('Сигнальное созвездие модулирвоанного сигнала')
                axs.plot(self.core.data1.real, self.core.data1.imag, '*')
                axs.grid()
                axs.axis('equal')
            
            elif plot_type == 'Filtered':
                f, axs = plt.subplots(1,2,figsize=(30,10))
                axs[0].set_title('Сигнальное созвездие передискретизированного сигнала')
                axs[0].plot(self.core.data2.real, self.core.data2.imag, '*' )
                axs[0].grid()
                axs[1].set_title('Сигнальное созвездие сигнала после формирующего фильтра')
                axs[1].plot(self.core.data3.real, self.core.data3.imag, '*' )
                axs[1].grid()  
                axs[0].axis('equal')
                axs[1].axis('equal')

            elif plot_type == 'Imparameters':
                f, axs = plt.subplots(1,2,figsize=(30,10))
                axs[0].set_title('Сигнальное созвездие сигнала с фракционной задержкой') 
                axs[0].plot(self.core.data4.real, self.core.data4.imag, '*' )
                axs[0].grid()
                axs[1].set_title('Сигнальное созвездие сигнала со сдвигом по частоте') 
                axs[1].plot(self.core.data5.real, self.core.data5.imag, '*' )
                axs[1].grid()
                axs[0].axis('equal')
                axs[1].axis('equal')  

            elif plot_type == 'Coarce_Timing':
                f1, psd1, f2, psd2 = self.core.coarse_log
                max_freq1 = f1[np.argmax(psd1)]
                max_freq2 = f2[np.argmax(psd2)]
                f, axs = plt.subplots(1,2,figsize=(30,10))
                axs[0].set_title('Сигнальное созвездие сигнала после грубой синхронизации по частоте')
                axs[0].plot(self.core.data6.real[50:-50], self.core.data6.imag[50:-50], '*' )
                axs[0].grid()
                axs[0].axis('equal')
                axs[1].axis('equal')

                axs[1].set_title('Сигнальное созвездие сигнала после тактовой синхронизации') 
                axs[1].plot(self.core.data7.real[50:-50], self.core.data7.imag[50:-50], '*' )
                axs[1].grid()
                axs[1].axis('equal') 

            elif plot_type == 'Fine':
                f, axs = plt.subplots(1,2,figsize=(30,10))
                axs[0].set_title('Сигнальное созвездие сигнала после петли Костаса')
                axs[0].plot(self.core.data8.real[50:-50], self.core.data8.imag[50:-50], '*' )
                axs[0].grid()
                axs[0].axis('equal')
                          
                axs[1].set_title('Значение ошибки в петле Костаса') 
                axs[1].plot(self.core.fine_log, '-*g' )
                axs[1].grid()

    def show(self):
        self.rfa_button = widgets.Button(description='Запустить анимацию изменения сдвига частоты', layout =  widgets.Layout(width='auto'))
        self.rta_button = widgets.Button(description='Запустить анимацию изменения временного сдвига', layout =  widgets.Layout(width='auto'))
        self.coarce_checkbox = widgets.Checkbox(False, description='Выполнять грубую синхронизацию по частоте', layout =  widgets.Layout(width='auto'))
        self.show_filtered_psd_checkbox = widgets.Checkbox(False, description='Показывать PSD до и после фильтрации', layout =  widgets.Layout(width='auto'))

        self.filter_beta_slider = widgets.FloatSlider(min=0,max=0.8,step=0.001, description="Коэффициент beta фильтра", layout = Layout(width='95%'), style = {'description_width': 'initial'})
        self.timing_sync_coeff_slider = widgets.FloatSlider(min=0,max=1,step=0.01, description="Множитель тактовой синхронизации", layout = Layout(width='95%'), style = {'description_width': 'initial'})
        self.costas_alpha_slider = widgets.FloatSlider(min=0,max=1,step=0.001, description="Коэффициент alpha в петле Костаса", layout = Layout(width='95%'), style = {'description_width': 'initial'})
        self.costas_beta_slider = widgets.FloatSlider(min=0,max=1,step=0.001, description="Коэффициент beta в петле Костаса", layout = Layout(width='95%'), style = {'description_width': 'initial'})
        self.dnr_db_slider = widgets.FloatSlider(min=0,max=100,step=1, value=100, description="SNR в дБ", layout = Layout(width='95%'), style = {'description_width': 'initial'})

        self.freq_shift_slider = widgets.FloatSlider(min=0,max=13000,step=1, description="Сдвиг по чатоте", layout = Layout(width='95%'), style = {'description_width': 'initial'})
        self.timing_shift_slider = widgets.FloatSlider(min=0,max=9.9,step=0.1, description="Сдвиг по времени", layout = Layout(width='95%'), style = {'description_width': 'initial'})
        self.plot_domain_list = widgets.Dropdown(options=['time', 'constellations'],description='Вид отображения', style = {'description_width': 'initial'})
        self.mod_list = widgets.Dropdown(options=self.modulation_to_param.keys(),description='Тип модуляции', style = {'description_width': 'initial'})

        self.ber = widgets.Text(layout={'border': '1px solid black'})
        self.base_map = { 'freq_shift': self.freq_shift_slider, 'timing_shift': self.timing_shift_slider, 'plot_domain':self.plot_domain_list, 'mod': self.mod_list, 
                     'filter_beta' : self.filter_beta_slider, 'timing_sync_coeff': self.timing_sync_coeff_slider, 'costas_alpha' : self.costas_alpha_slider, 
                     'costas_beta' : self.costas_beta_slider, 'coarce_enable':self.coarce_checkbox, 'show_filtered_psd': self.show_filtered_psd_checkbox, 'snr_db':self.dnr_db_slider,
                     'plot_type': fixed('Source')  }

        source_ui = widgets.HBox([self.mod_list, self.plot_domain_list]) 
        source_out = widgets.interactive_output(self.sir_interactive_func, {**self.base_map, 'plot_type': fixed('Source')} )
        source = widgets.VBox(children=[source_ui, source_out])

        # modulated_ui = widgets.HBox([self.mod_list, self.plot_domain_list])
        # modulated_out = widgets.interactive_output(self.sir_interactive_func, {**self.base_map, 'plot_type': fixed('Modulated')} )
        # modulated = widgets.VBox(children=[modulated_ui, modulated_out])

        filtered_ui = widgets.VBox([self.filter_beta_slider, widgets.HBox([self.mod_list, self.plot_domain_list, self.show_filtered_psd_checkbox])])
        filtered_out = widgets.interactive_output(self.sir_interactive_func, {**self.base_map, 'plot_type': fixed('Filtered')} )
        filtered  = widgets.VBox(children=[filtered_ui, filtered_out])

        imparameters_ui = widgets.VBox([self.freq_shift_slider, self.timing_shift_slider, self.dnr_db_slider, widgets.HBox([self.mod_list, self.plot_domain_list, self.rfa_button, self.rta_button])])
        imparameters_out = widgets.interactive_output(self.sir_interactive_func, {**self.base_map, 'plot_type': fixed('Imparameters')} )
        imparameters = widgets.VBox(children=[imparameters_ui, imparameters_out])


        coarce_timing_ui = widgets.VBox([self.freq_shift_slider,self.timing_shift_slider,self.dnr_db_slider, self.timing_sync_coeff_slider, widgets.HBox([self.mod_list, self.plot_domain_list, self.coarce_checkbox]) ])
        coarce_timing_out = widgets.interactive_output(self.sir_interactive_func, {**self.base_map, 'plot_type': fixed('Coarce_Timing')})
        coarce_timing = widgets.VBox(children=[coarce_timing_ui, coarce_timing_out])

        fine_ui = widgets.VBox([self.freq_shift_slider, self.timing_shift_slider, self.dnr_db_slider, self.costas_alpha_slider, self.costas_beta_slider, widgets.HBox([self.mod_list, self.plot_domain_list])])
        fine_out = widgets.interactive_output(self.sir_interactive_func, {**self.base_map, 'plot_type': fixed('Fine')})
        fine = widgets.VBox(children=[fine_ui, fine_out])  

        demodulated_ui = widgets.VBox([self.freq_shift_slider, self.timing_shift_slider, self.dnr_db_slider, self.costas_alpha_slider, self.costas_beta_slider, widgets.HBox([self.mod_list, self.plot_domain_list,  self.ber])])
        # demodulated_ui = widgets.VBox([self.freq_shift_slider, self.timing_shift_slider, self.dnr_db_slider, self.costas_alpha_slider, self.costas_beta_slider, widgets.HBox([self.mod_list, self.plot_domain_list])])
        demodulated_out = widgets.interactive_output(self.sir_interactive_func, {**self.base_map, 'plot_type': fixed('Demodulated')})
        demodulated =  widgets.VBox(children=[demodulated_ui, demodulated_out,])  

        self.rfa_button.on_click(self.run_freq_animation)
        self.rta_button.on_click(self.run_timing_animation)

        sub_tab=[source,  filtered,imparameters,coarce_timing,fine,demodulated ]
        self.tab = Tab(sub_tab)
        self.tab.set_title(0,"Source/Modulated")
        self.tab.set_title(1,"Upsampled/Filtered")
        self.tab.set_title(2,"Imparameters")
        self.tab.set_title(3,"Coarce/Timing")
        self.tab.set_title(4,"Fine")
        self.tab.set_title(5,"Demodulated")
        display(self.tab)

    def run_freq_animation(self, a, steps = 10, sep_size = 10):
        for i in range(steps):
            self.freq_shift_slider.value += sep_size

    def run_timing_animation(self, a, steps = 10, sep_size = 0.1):
        for i in range(steps):
            self.timing_shift_slider.value += sep_size