import os
import sys
import time
import pandas as pd
import pretty_errors
import PySimpleGUI as sg

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..data.Company import FinancialStatements, IndustryAnalysis
    from ..data.Stock import ConstituentStocks, StockData
    from ..data.Bond import BondData
    from ..data.Date import GetDate
    from ..log.log import hide, show, slog, sprint
    from ..stock.Markovitz import Markovitz
except:
    from data.Company import FinancialStatements, IndustryAnalysis
    from data.Stock import ConstituentStocks, StockData
    from data.Bond import BondData
    from data.Date import GetDate
    from log.log import hide, show, slog, sprint
    from stock.Markovitz import Markovitz


class APP(object):
    '''A simple APP'''

    def __init__(self):
        sg.theme('BlueMono')

    def window_control(self, window):
        event, values = window.read()
        window.close()
        if not event:
            sys.exit()
        return values

    def path_control(self, path):
        if not path:
            raise ValueError('Please choose a folder to save the result!')

    def save(self, path, func_name, dic):
        writer = pd.ExcelWriter(f'{path}/{func_name}.xlsx')
        for name, data in dic.items():
            data.to_excel(writer, sheet_name=name)
        writer.save()
        sprint(f'Finished, saved in {path}.')
        time.sleep(10)

    def markovitz_gui(self):
        func_name = 'Markovitz Portfolio'
        layout = [
            [sg.Text('Stock List')],
            [sg.Multiline('贵州茅台\n隆基股份\n五粮液', key='stock_list')],
            [sg.Text('Start Date'), sg.Input(
                '2019-01-01', key='start_date')],
            [sg.Text('End Date'), sg.Input(
                '2020-01-01', key='end_date')],
            [sg.Text('Risk-off Rate'), sg.Input(
                '0.0185', key='no_risk_rate')],
            [sg.Text('Funds'), sg.Input(
                '10000000', key='funds')],
            [sg.FolderBrowse('Choose a folder to save data', key='path')],
            [sg.Button('Start working!')]
        ]
        window = sg.Window(func_name, layout)
        values = self.window_control(window)
        path = values['path']
        self.path_control(path)
        start_date = values['start_date']
        end_date = values['end_date']
        stock_list = values['stock_list'].rstrip().split('\n')
        no_risk_rate = float(values['no_risk_rate'])
        funds = float(values['funds'])
        mk = Markovitz(names=stock_list, start_date=start_date,
                       end_date=end_date, no_risk_rate=no_risk_rate, funds=funds)
        dic = {
            'stock data': mk.data,
            'scatter data': mk.scatter_data(number=5000),
            'font scatter data': mk.font_scatter_data(number=500),
            'optimal weight': mk.optimal_weight(),
            'buy': mk.buy(),
        }
        name = func_name+'-'+str(stock_list)+'-'+str(start_date)+'--' + \
            str(end_date)+'-'+values['no_risk_rate']+'-'+values['funds']
        self.save(path, name, dic)
        mk.drawing()

    def markovitz_work(self):
        if self.event == 'Markovitz Portfolio':
            self.window.close()
            self.markovitz_gui()

    def stock_gui(self):
        func_name = 'Stock Data'
        layout = [
            [sg.Text('Stock List')],
            [sg.Multiline('贵州茅台\n隆基股份\n五粮液', key='stock_list')],
            [sg.Text('Start Date'), sg.Input(
                '2019-01-01', key='start_date')],
            [sg.Text('End Date'), sg.Input(
                '2020-01-01', key='end_date')],
            [sg.FolderBrowse('Choose a folder to save data', key='path')],
            [sg.Button('Start working!')]
        ]
        window = sg.Window(func_name, layout)
        values = self.window_control(window)
        path = values['path']
        self.path_control(path)
        start_date = values['start_date']
        end_date = values['end_date']
        stock_list = values['stock_list'].rstrip().split('\n')
        sd = StockData(names=stock_list,
                       start_date=start_date,
                       end_date=end_date,
                       adjustflag='3')
        cs = ConstituentStocks()
        dic = {
            '股票代码和上市日期': pd.DataFrame(sd.stocks_info(), columns=['code', 'ipoDate']),
            '股票数据': sd.stocks_data(),
            '股票估值': sd.stocks_valuation(),
            '股票行业数据': cs.stock_industry(),
            '上证50': cs.sz50(),
            '沪深300': cs.hs300(),
            '中证500': cs.zz500()
        }
        name = func_name+'-'+str(stock_list)+'-' + \
            str(start_date)+'--' + str(end_date)
        self.save(path, name, dic)

    def stock_work(self):
        if self.event == 'Stock Data':
            self.window.close()
            self.stock_gui()

    def company_gui(self):
        func_name = 'Company Data'
        layout = [
            [sg.Text('Stock List')],
            [sg.Multiline('贵州茅台\n隆基股份\n五粮液', key='stock_list')],
            [sg.FolderBrowse('Choose a folder to save data', key='path')],
            [sg.Button('Start working!')]
        ]
        window = sg.Window(func_name, layout)
        values = self.window_control(window)
        path = values['path']
        self.path_control(path)
        stock_list = values['stock_list'].rstrip().split('\n')
        fs = FinancialStatements(names=stock_list)
        ia = IndustryAnalysis(names=stock_list)
        dic = {
            '财务报表摘要': fs.summary(),
            '资产负债表': fs.balance(),
            '利润表': fs.income(),
            '现金流量表': fs.cash_flow(),
            '主要财务指标': fs.main_info(),
            '盈利能力指标': fs.profit_info(),
            '偿债能力指标': fs.debt_info(),
            '成长能力指标': fs.growth_info(),
            '营运能力指标': fs.operation_info(),
            '行业资讯': ia.industry_info(),
            '成长性比较': ia.growth_info(),
            '估值比较': ia.valuation_info(),
            '杜邦分析比较': ia.dupont_info(),
            '公司规模': ia.market_size()
        }
        name = func_name+'-'+str(stock_list)
        self.save(path, name, dic)

    def company_work(self):
        if self.event == 'Company Data':
            self.window.close()
            self.company_gui()

    def bond_gui(self):
        func_name = 'Bond Data'
        layout = [
            [sg.FolderBrowse('Choose a folder to save data', key='path')],
            [sg.Button('Start working!')]
        ]
        window = sg.Window(func_name, layout)
        values = self.window_control(window)
        path = values['path']
        self.path_control(path)
        bd = BondData()
        dic = {
            '可转债': bd.convertible_bond(),
            '企业债': bd.corporate_bond(),
            '国债': bd.national_bond()
        }
        name = func_name+'-'+str(time.strftime("%Y%m%d", time.localtime()))
        self.save(path, name, dic)

    def bond_work(self):
        if self.event == 'Bond Data':
            self.window.close()
            self.bond_gui()

    def date_gui(self):
        func_name = 'Date Data'
        layout = [
            [sg.Text('Start Date'), sg.Input(
                '20190101', key='start_date')],
            [sg.Text('End Date'), sg.Input(
                str(time.strftime("%Y%m%d", time.localtime())), key='end_date')],
            [sg.FolderBrowse('Choose a folder to save data', key='path')],
            [sg.Button('Start working!')]
        ]
        window = sg.Window(func_name, layout)
        values = self.window_control(window)
        path = values['path']
        self.path_control(path)
        start_date = values['start_date']
        end_date = values['end_date']
        gd = GetDate()
        dic = {'date': gd.Date()}
        name = func_name + '-' + str(start_date)+'--' + str(end_date)
        self.save(path, name, dic)

    def date_work(self):
        if self.event == 'Date Data':
            self.window.close()
            self.date_gui()

    def work(self):

        layout = [
            [sg.Button('Markovitz Portfolio'), ],
            [sg.Button('Stock Data'), sg.Button('Company Data')],
            [sg.Button('Date Data'), sg.Button('Bond Data')],
        ]
        self.window = sg.Window('Suluoya', layout)
        self.event, self.values = self.window.read()
        while True:
            if not self.stock_work() \
                    and not self.markovitz_work() \
                    and not self.company_work() \
                    and not self.bond_work() \
                    and not self.date_work():
                sys.exit()


if __name__ == '__main__':
    app = APP()
    app.work()
'''

药明康德
比亚迪
山西汾酒
科沃斯
紫金矿业

'''