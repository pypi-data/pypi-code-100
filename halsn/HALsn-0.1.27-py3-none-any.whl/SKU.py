#!/usr/bin/env python3

'''
MIT License

Copyright (c) 2021 Mikhail Hyde & Cole Crescas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from HALsn.serialSupervisor import serialSupervisor

#################################################################
#####                                                       #####
#####                    COFFEE MACHINES                    #####
#####                                                       #####
#################################################################

class CFP(serialSupervisor):
    def __init__(self, device_path='/dev/FTDI', baud=9600, timeout=0.125):

        super().__init__(device_path, baud, timeout)

        self.commands = {
            # Disables Debug Mode
            'debug_off':             '*DS0\r',
            # Enables Debug Mode
            'debug_on':              '*DS1\r',
            # Starts 6oz Classic Brew (K-Cup)
            '6_oz_classic_K':        '*LT1\r',
            # Starts 8oz Classic Brew (K-Cup)
            '8_oz_classic_K':        '*LT2\r',
            # Starts 10oz Classic Brew (K-Cup)
            '10_oz_classic_K':       '*LT3\r',
            # Starts 12oz Classic Brew (K-Cup)
            '12_oz_classic_K':       '*LT4\r',
            # Starts 6oz Over Ice Brew (K-Cup)
            '6_oz_over_ice_K':       '*LT5\r',
            # Starts 8oz Over Ice Brew (K-Cup)
            '8_oz_over_ice_K':       '*LT6\r',
            # Starts 10oz Over Ice Brew (K-Cup)
            '10_oz_over_ice_K':      '*LT7\r',
            # Starts 12oz Over Ice Brew (K-Cup)
            '12_oz_over_ice_K':      '*LT8\r',
            # Starts 6oz Rich Brew (K-Cup)
            '6_oz_rich_K':           '*LT9\r',
            # Starts 8oz Rich Brew (K-Cup)
            '8_oz_rich_K':           '*LT10\r',
            # Starts 9oz Rich Brew (K-Cup)
            '9_oz_rich_K':           '*LT11\r',
            # Starts 11oz Rich Brew (K-Cup)
            '11_oz_rich_K':          '*LT12\r',
            # Starts 8oz Classic Brew (Grounds)
            '8_oz_classic':          '*LT13\r',
            # Starts 10oz Classic Brew (Grounds)
            '10_oz_classic':         '*LT14\r',
            # Start 2oz Hot Water
            '2_oz_hot_water':        '*LT15\r',
            # Start 4oz Hot Water
            '4_oz_hot_water':        '*LT16\r',
            # Start 6oz Hot Water
            '6_oz_hot_water':        '*LT17\r',
            # Start 8oz Hot Water
            '8_oz_hot_water':        '*LT18\r',
            # Start 10oz Hot Water
            '10_oz_hot_water':       '*LT19\r',
            # Start 12oz Hot Water
            '12_oz_hot_water':       '*LT20\r',
            # Start 14oz Hot Water
            '14_oz_hot_water':       '*LT21\r',
            # Start 16oz Hot Water
            '16_oz_hot_water':       '*LT22\r',
            # Start 18oz Hot Water
            '18_oz_hot_water':       '*LT23\r',
            # Start 20oz Hot Water
            '20_oz_hot_water':       '*LT24\r',
            # Start 22oz Hot Water
            '22_oz_hot_water':       '*LT25\r',
            # Start 24oz Hot Water
            '24_oz_hot_water':       '*LT26\r',
            # Start 28oz Hot Water
            '28_oz_hot_water':       '*LT27\r',
            # Start 32oz Hot Water
            '32_oz_hot_water':       '*LT28\r',
            # Start 40oz Hot Water
            '40_oz_hot_water':       '*LT29\r',
            # Start 50oz Hot Water
            '50_oz_hot_water':       '*LT30\r',
            # Start 60oz Brew (Hot Water)
            'full_carafe_hot_water': '*LT31\r',
            # Starts 12oz Classic Brew (Grounds)
            '12_oz_classic':         '*LT32\r',
            # Starts 15oz Classic Brew (Grounds)
            '15_oz_classic':         '*LT33\r',
            # Starts 18oz Classic Brew (Grounds)
            '18_oz_classic':         '*LT34\r',
            # Starts 28oz Classic Brew (Grounds)
            '28_oz_classic':         '*LT35\r',
            # Starts 37oz Classic Brew (Grounds)
            '37_oz_classic':         '*LT37\r',
            # Starts 46oz Classic Brew (Grounds)
            '46_oz_classic':         '*LT38\r',
            # Starts 60oz Classic Brew (Grounds)
            'full_carafe_classic':   '*LT39\r',
            # Starts 8oz Over Ice Brew (Grounds)
            '8_oz_over_ice':         '*LT40\r',
            # Starts 10oz Over Ice Brew (Grounds)
            '10_oz_over_ice':        '*LT41\r',
            # Starts 12oz Over Ice Brew (Grounds)
            '12_oz_over_ice':        '*LT42\r',
            # Starts 14oz Over Ice Brew (Grounds)
            '14_oz_over_ice':        '*LT43\r',
            # Starts 18oz Over Ice Brew (Grounds)
            '18_oz_over_ice':        '*LT44\r',
            # Starts 28oz Over Ice Brew (Grounds)
            '28_oz_over_ice':        '*LT45\r',
            # Starts 37oz Over Ice Brew (Grounds)
            '37_oz_over_ice':        '*LT47\r',
            # Starts 46oz Over Ice Brew (Grounds)
            '46_oz_over_ice':        '*LT48\r',
            # Starts 55oz Over Ice Brew (Grounds)
            'full_carafe_over_ice':  '*LT49\r',
            # Starts 7oz Rich Brew (Grounds)
            '7_oz_rich':             '*LT50\r',
            # Starts 8oz Rich Brew (Grounds)
            '8_oz_rich':             '*LT51\r',
            # Starts 10oz Rich Brew (Grounds)
            '10_oz_rich':            '*LT52\r',
            # Starts 12oz Rich Brew (Grounds)
            '12_oz_rich':            '*LT53\r',
            # Starts 16oz Rich Brew (Grounds)
            '16_oz_rich':            '*LT54\r',
            # Starts 26oz Rich Brew (Grounds)
            '26_oz_rich':            '*LT55\r',
            # Starts 33oz Rich Brew (Grounds)
            '33_oz_rich':            '*LT57\r',
            # Starts 41oz Rich Brew (Grounds)
            '41_oz_rich':            '*LT58\r',
            # Starts 47oz Rich Brew (Grounds)
            '47_oz_rich':            '*LT59\r',
            # Starts 4oz Specialty (Grounds)
            '4_oz_special':          '*LT60\r',
            # Starts 4oz Specialty (K-Cup)
            '4_oz_special_K':        '*LT61\r',
            # Starts 2oz Water Boil
            '2_oz_water_boil':       '*LT62\r',
            # Starts 4oz Water Boil
            '4_oz_water_boil':       '*LT63\r',
            # Starts 6oz Water Boil
            '6_oz_water_boil':       '*LT64\r',
            # Starts 8oz Water Boil
            '8_oz_water_boil':       '*LT65\r',
            # Starts 10oz Water Boil
            '10_oz_water_boil':      '*LT66\r',
            # Starts 12oz Water Boil
            '12_oz_water_boil':      '*LT67\r',
            # Starts 14oz Water Boil
            '14_oz_water_boil':      '*LT68\r',
            # Starts 16oz Water Boil
            '16_oz_water_boil':      '*LT69\r',
            # Starts 18oz Water Boil
            '18_oz_water_boil':      '*LT70\r',
            # Starts 20oz Water Boil
            '20_oz_water_boil':      '*LT71\r',
            # Starts 22oz Water Boil
            '22_oz_water_boil':      '*LT72\r',
            # Starts 24oz Water Boil
            '24_oz_water_boil':      '*LT73\r',
            # Starts 28oz Water Boil
            '28_oz_water_boil':      '*LT74\r',
            # Starts 32oz Water Boil
            '32_oz_water_boil':      '*LT75\r',
            # Starts 40oz Water Boil
            '40_oz_water_boil':      '*LT76\r',
            # Starts 50oz Water Boil
            '50_oz_water_boil':      '*LT77\r',
            # Starts 60oz Water Boil
            '60_oz_water_boil':      '*LT78\r',
            # Starts Auto Purge Cycle
            'auto_purge':            '*LT79\r',
            # Starts Clean Cycle
            'clean_cycle':           '*LT80\r',
            # Cancel Current Brew
            'cancel_brew':           '*LC\r',
            # Turn ON Boiler
            'en_boiler':             '*KR11\r',
            # Turn OFF Boiler
            'dis_boiler':            '*KR10\r',
            # Turn ON Warm Plate
            'en_warm_panel':         '*KR21\r',
            # Turn OFF Warm Plate
            'dis_warm_panel':        '*KR20\r'
        }

        #   | CMD | MST QRY EN | STR IDX | END IDX | HEX CONV EN
        self.queries = {
            # Requests Current Debug State
            'debug_state':           ['?DS\r',  0,  3,  4, 0],
            # Requests Current Brew State
            'current_brew':          ['?LT\r',  1,  3,  4, 0],
            # Request Basket|Size|Style|Ounces|Block|Temp|Volume|Time
            'coffee_recipe_status':  ['?KC\r',  1,  3,  4, 1],
            # Requests PWM Value of Water Pump
            'water_pump_pwm':        ['?KM1\r', 1,  4,  6, 1],
            # Requests PWM Value of Air Pump
            'air_pump_pwm':          ['?KM2\r', 1,  4,  6, 1],
            # Requests Boiler Temp (C)
            'boiler_ntc':            ['?KN1\r', 1,  4,  8, 1],
            # Requests Warm Panel Temp (C)
            'warm_panel_ntc':        ['?KN2\r', 1,  4,  8, 1],
            # Requests Pump Temp (C)
            'pump_ntc':              ['?KN3\r', 1,  4,  8, 1],
            # Requests Alt Cal Temp (C)
            'alt_cal_ntc':           ['?KN4\r', 1,  4,  8, 1],
            # Requests Cal Offset Temp (C)
            'fac_cal_ntc':           ['?KN5\r', 1,  4,  8, 1],
            # Returns Boiler PWM
            'boiler_pwm':            ['?KR1\r', 1,  4,  5, 0],
            # Returns Warm Plate PWM
            'warm_panel_pwm':        ['?KR2\r', 1,  4,  5, 0],
            # Returns State of Drip Switch
            'drip_sw':               ['?SW0\r', 1,  4,  5, 0],
            # Unknown Switch
            'SW1':                   ['?SW1\r', 1,  4,  5, 0],
            # Returns state of Coffee Basket Switch
            'coffee_basket_sw':      ['?SW2\r', 1,  4,  5, 0],
            # Returns state of KCup Basket Switch
            'kcup_basket_sw':        ['?SW3\r', 1,  4,  5, 0],
            # Returns state of Water Flow Switch
            'flow_path_sw':          ['?SW4\r', 1,  4,  5, 0],
            # Returns state of Coffee Flow Switch
            'coffee_path_sw':        ['?SW5\r', 1,  4,  5, 0],
            # Requests Software Version on UI MCU
            'sw_version_ui':         ['?WZ0\r', 0,  4, 19, 0],
            # Requests Software Version on Power MCU
            'sw_version_pwr':        ['?WZ1\r', 0,  4, 19, 0]
        }

        self.testType = ''
        self.lifeTestCommand = ''
        self.errorCommand = 'cancel_brew'

    def ctrl_water_pump(self, speed):
        '''
        Takes in a speed percentage and enables the
        water pump at that percent speed. Enables
        manual activation and deactivation of
        the pump
        '''
        map_speed = str(int((speed/100) * 64))
        if len(map_speed) == 1:
            map_speed = '0' + map_speed
        self._send_msg('*KM1%s\r' % map_speed)

    def ctrl_air_pump(self, speed):
        '''
        Takes in a speed percentage and enables the
        water pump at that percent speed. Enables
        manual activation and deactivation of
        the pump
        '''
        map_speed = str(int((speed/100) * 64))
        if len(map_speed) == 1:
            map_speed = '0' + map_speed
        self._send_msg('*KM2%s\r' % map_speed)

    def check_switch_states(self):
        '''
        Simple function to check the switch state of self.CFP.
        Reads through returned strings and looks at state index
        to determine if machine configured for the test.

        ::returns:: List
        '''

        switch_qry = ['drip_sw', 'SW1', 'coffee_basket_sw', 'kcup_basket_sw', 'flow_path_sw', 'coffee_path_sw']

        switch_states = self.specific_query(switch_qry)

        print(f'Product Switch States: {switch_states}\nRefer to the\
                product map to identify switches.')
    
        return switch_states

    def return_product_functions(self):
        '''
        Returns all available functions for the CFP.
        Neglects unnecessary commands in the commands
        dictionary.

        ::returns:: Formatted String
        '''

        fnc = []

        for key in self.commands.keys():
            if self.commands[key][1:3] == 'LT':
                fnc.append(key)

        return fnc

#################################################################
#####                                                       #####
#####           AIR FRYERS - PRESSURE COOKERS               #####
#####                                                       #####
#################################################################

class SF(serialSupervisor):
    def __init__(self, device_path='/dev/FTDI', baud=9600, timeout=0.125):

        super().__init__(device_path, baud, timeout)

        self.commands = {
            # Disables Debug Mode
            'debug_off':             '*DS0\r',
            # Enables Debug Mode
            'debug_on':              '*DS1\r',
            # Disables Motor
            'disable_motor':         '*KM100\r',
            # Enable Motor 1200 RPM
            'en_motor_1200':         '*KM110\r',
            # Enable Motor 2200 RPM
            'en_motor_2200':         '*KM120\r',
            # Enable Motor 3000 RPM
            'en_motor_full':         '*KM130\r'
        }

        #   | CMD | MST QRY EN | STR IDX | END IDX | HEX CONV EN
        self.queries = {
            # Requests Current Debug State
            'debug_state':           ['?DS\r',  0,  3,  4, 0],
            # Request Motor State
            'motor_state':           ['?KM1\r', 1,  4,  6, 0],
            # Requests AF Temp (C)
            'af_ntc':                ['?KN1\r', 1,  4,  8, 1],
            # Requests Pot Temp (C)
            'pot_ntc':               ['?KN2\r', 1,  4,  8, 1],
            # Requests IR TC Temp (C)
            'ir_therm':              ['?KN3\r', 1,  4,  8, 1],
            # Requests Probe 1 Temp (C)
            'probe_1_ntc':           ['?KN4\r', 1,  4,  8, 1],
            # Requests Probe 2 Temp (C)
            'probe_2_ntc':           ['?KN5\r', 1,  4,  8, 1],
            # Returns State of Pot/Drawer switch
            'pot_sw':                ['?SW0\r', 1,  4,  5, 0],
            # Returns state of Vent/Slider switch
            'vent_sw':               ['?SW1\r', 1,  4,  5, 0],
            # PCBA Barcode Information
            'pcba_bc':               ['?WW\r',  0,  3, -2, 0],
            # QR Code Information
            'qr_code':               ['?WX\r',  0,  3, -2, 0],
            # Requests Power Software Version on MCU
            'power_sw_version':      ['?WZ\r',  0,  4, 19, 0],
            # Requests UI Software Version on MCU
            'ui_sw_version':         ['?WU\r',  0,  4, 19, 0]
        }

#################################################################
#####                                                       #####
#####                   GRILLS && OVENS                     #####
#####                                                       #####
#################################################################

class FG(serialSupervisor):
    def __init__(self, device_path='/dev/FTDI', baud=9600, timeout=0.125):
        super().__init__(device_path, baud, timeout)

        self.commands = {
            # Disables Debug Mode
            'debug_off':             '*DS0\r',
            # Enables Debug Mode
            'debug_on':              '*DS1\r'
        }

        #   | CMD | MST QRY EN | STR IDX | END IDX | HEX CONV EN
        self.queries = {
            # Requests Current Debug State
            'debug_state':           ['?DS\r',  0,  3,  4, 0],
            # Requests Top Temp (C)
            'top_ntc':               ['?KN1\r', 1,  4,  8, 1],
            # Requests Bottom Temp (C)
            'bot_ntc':               ['?KN2\r', 1,  4,  8, 1],
            # Requests Power Software Version on MCU
            'power_sw_version':      ['?WZ\r',  0,  4, 19, 0]
        }