"""
基于私募基金估值表的截面持仓风格归因模块
"""
import pandas as pd
import hbshare as hbs
from hbshare.rm_associated.util.config import style_name, industry_name
import datetime
from sqlalchemy import create_engine
from hbshare.rm_associated.config import engine_params
from hbshare.rm_associated.util.config import factor_map_dict
import plotly
import plotly.graph_objs as go


def plot_render(plot_dic, width=1200, height=800, **kwargs):
    kwargs['output_type'] = 'div'
    plot_str = plotly.offline.plot(plot_dic, **kwargs)
    print('%%angular <div style="height: %ipx; width: %spx"> %s </div>' % (height, width, plot_str))


class HoldingAnalysor:
    def __init__(self, fund_name, trade_date, benchmark_id):
        self.fund_name = fund_name
        self.trade_date = trade_date
        self.benchmark_id = benchmark_id
        self._load_data()

    def _load_shift_date(self):
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=100)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date, self.trade_date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isMonthEnd'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    def _load_portfolio_weight_series(self):
        sql_script = "SELECT * FROM private_fund_holding where fund_name = '{}' and trade_date = {}".format(
            self.fund_name, self.trade_date)
        engine = create_engine(engine_params)
        holding_df = pd.read_sql(sql_script, engine)
        holding_df['trade_date'] = holding_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))

        return holding_df.set_index('ticker')['weight'] / 100.

    def _load_benchmark_weight_series(self, date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and SecuCode = '{}'".format(
            self.benchmark_id)
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code = index_info.set_index('SECUCODE').loc[self.benchmark_id, 'INNERCODE']

        sql_script = "SELECT (select a.SecuCode from hsjy_gp.SecuMain a where a.InnerCode = b.InnerCode and " \
                     "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                     "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        weight_df = data.rename(
            columns={"SECUCODE": "consTickerSymbol", "ENDDATE": "effDate", "WEIGHT": "weight"})

        return weight_df.set_index('consTickerSymbol')['weight'] / 100.

    @staticmethod
    def _load_style_exposure(date):
        sql_script = "SELECT * FROM st_ashare.r_st_barra_style_factor where TRADE_DATE = '{}'".format(date)
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        exposure_df = pd.DataFrame(res['data']).set_index('ticker')
        ind_names = [x.lower() for x in industry_name['sw'].values()]
        exposure_df = exposure_df[style_name + ind_names]

        return exposure_df

    def _load_data(self):
        shift_date = self._load_shift_date()
        portfolio_weight_series = self._load_portfolio_weight_series()
        benchmark_weight_series = self._load_benchmark_weight_series(shift_date)
        style_exposure_df = self._load_style_exposure(shift_date)

        self.data_param = {
            "portfolio_weight_series": portfolio_weight_series,
            "benchmark_weight_series": benchmark_weight_series,
            "style_exposure_df": style_exposure_df
        }

    @staticmethod
    def plotly_style_bar(df, title_text, figsize=(1200, 800), legend_x=0.30):
        fig_width, fig_height = figsize
        cols = df.columns.tolist()
        color_list = ['rgb(49, 130, 189)', 'rgb(204, 204, 204)', 'rgb(216, 0, 18)']
        data = []
        for i in range(len(cols)):
            col = cols[i]
            trace = go.Bar(
                x=df.index.tolist(),
                y=df[col],
                name=col,
                marker=dict(color=color_list[i])
            )
            data.append(trace)

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=True),
            xaxis=dict(showgrid=True),
            legend=dict(orientation="h", x=legend_x),
            template='plotly_white'
        )

        # fig = go.Figure(data=data, layout=layout)

        return data, layout

    @staticmethod
    def plotly_bar(df, title_text, figsize=(1200, 800)):
        fig_width, fig_height = figsize
        cols = df.columns.tolist()
        color_list = ['rgb(49, 130, 189)', 'rgb(204, 204, 204)']
        data = []
        for i in range(len(cols)):
            col = cols[i]
            trace = go.Bar(
                x=df.index.tolist(),
                y=df[col],
                name=col,
                marker=dict(color=color_list[i])
            )
            data.append(trace)

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=True),
            xaxis=dict(showgrid=True),
            legend=dict(orientation="h", x=0.38),
            template='plotly_white'
        )

        # fig = go.Figure(data=data, layout=layout)

        return data, layout

    @staticmethod
    def plotly_pie(df, title_text, figsize=(800, 600)):
        fig_width, fig_height = figsize
        labels = df.index.tolist()
        values = df.values.round(3).tolist()
        data = [go.Pie(labels=labels, values=values, hoverinfo="label+percent",
                       texttemplate="%{label}: %{percent}")]
        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height
        )

        # fig = go.Figure(data=data, layout=layout)

        return data, layout

    def get_construct_result(self, isPlot=True):
        portfolio_weight_series = self.data_param.get('portfolio_weight_series')
        benchmark_weight_series = self.data_param.get('benchmark_weight_series')
        style_exposure_df = self.data_param.get('style_exposure_df')

        # 板块分布
        weight_df = portfolio_weight_series.reset_index()
        weight_df.loc[weight_df['ticker'].str.startswith('0'), 'sector'] = '深市'
        weight_df.loc[weight_df['ticker'].str.startswith('60'), 'sector'] = '沪市'
        weight_df.loc[weight_df['ticker'].str.startswith('30'), 'sector'] = '创业板'
        weight_df.loc[weight_df['ticker'].str.startswith('688'), 'sector'] = '科创板'
        sector_distribution = weight_df.groupby('sector')['weight'].sum()

        # 风格及行业分布
        idx = portfolio_weight_series.index.union(benchmark_weight_series.index).intersection(
            style_exposure_df.index)

        portfolio_weight_series = portfolio_weight_series.reindex(idx).fillna(0.)
        benchmark_weight_series = benchmark_weight_series.reindex(idx).fillna(0.)
        style_exposure_df = style_exposure_df.reindex(idx).astype(float)
        portfolio_expo = style_exposure_df.T.dot(portfolio_weight_series)
        benchmark_expo = style_exposure_df.T.dot(benchmark_weight_series)
        style_expo = pd.concat([portfolio_expo.to_frame('port'), benchmark_expo.to_frame('bm')], axis=1)
        style_expo['active'] = style_expo['port'] - style_expo['bm']

        reverse_ind = dict([(value.lower(), key) for (key, value) in industry_name['sw'].items()])
        benchmark_id_map = {"000300": "沪深300", "000905": "中证500", "000852": "中证1000"}

        # 风格
        style_df = style_expo[['port', 'bm', 'active']].rename(
            columns={"port": self.fund_name, "bm": benchmark_id_map[self.benchmark_id], "active": "主动暴露"}).loc[
            style_name]
        style_df.index = style_df.index.map(factor_map_dict)
        if isPlot:
            data, layout = self.plotly_style_bar(style_df, "横截面持仓风格暴露")
            plot_render({"data": data, "layout": layout})
        # 行业
        ind_df = style_expo[['port', 'bm', 'active']].rename(
            columns={"port": self.fund_name, "bm": benchmark_id_map[self.benchmark_id], "active": "主动暴露"}).iloc[10:]
        ind_df.index = [reverse_ind[x] for x in ind_df.index]
        if isPlot:
            data, layout = self.plotly_style_bar(ind_df, "横截面持仓行业暴露", figsize=(1500, 700), legend_x=0.35)
            plot_render({"data": data, "layout": layout}, width=1500, height=700)
        # 板块分布
        sector_distribution.loc['非权益资产'] = 1 - sector_distribution.sum()
        if isPlot:
            data, layout = self.plotly_pie(sector_distribution, "持仓板块分布", figsize=(800, 600))
            plot_render({"data": data, "layout": layout}, width=800, height=600)

        results = {"style_df": style_df, "ind_df": ind_df, "sector_distribution": sector_distribution}

        return results


if __name__ == '__main__':
    date_list = ['20201231', '20210131', '20210228']
    tmp = HoldingAnalysor("启林城上进取1号", "20210131", "000852").get_construct_result(isPlot=False)
    print(tmp['style_df'])