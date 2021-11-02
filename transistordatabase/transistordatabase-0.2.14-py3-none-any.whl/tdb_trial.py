from databaseClasses import *

#transistorlist = print_TDB()



def whatever():

    #transistor_loaded = load({'name': 'CREE_C3M0120100J'})
    transistor_loaded = load({'name': 'Fuji_2MBI400U2B-060'})

    x = np.logspace(-3, 0, 1000)
    y = 0 * x
    transistor_loaded.calc_thermal_params('switch')
    print(transistor_loaded.switch.thermal_foster.r_th_vector)
    print(transistor_loaded.switch.thermal_foster.c_th_vector)

    for count,val in enumerate(transistor_loaded.switch.thermal_foster.r_th_vector):
        r = transistor_loaded.switch.thermal_foster.r_th_vector[count]
        c = transistor_loaded.switch.thermal_foster.c_th_vector[count]
        tau = r * c

        y += r * (1 - np.exp(-x/tau))


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.loglog(transistor_loaded.switch.thermal_foster.graph_t_rthjc[0], transistor_loaded.switch.thermal_foster.graph_t_rthjc[1])
    ax.loglog(x,y)
    ax.set_xlabel('Time : $t$ [sec]')
    ax.set_ylabel('Thermal impedance: $Z_{th(j-c)}$ [K/W ]')
    ax.grid()
    plt.show()

def neu():
    update_from_fileexchange()

if __name__ == '__main__':
    neu()
    t1 = load({'name': 'Fuji_2MBI200XAA065-50'})
    print(t1.r_g_on_recommended)