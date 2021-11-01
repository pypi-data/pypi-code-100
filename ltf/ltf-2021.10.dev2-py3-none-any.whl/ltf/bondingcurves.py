import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pkg_resources
# DEFAULT_PATH = pkg_resources.resource_stream(__name__, 'data/bondingcurves_initial_values.csv')
DEFAULT_PATH = pkg_resources.resource_stream('ltf', 'data/bondingcurves_initial_values.csv')

CURRENT_SUPPLY = 16000000
ZOOM = 1
RESERVE_RATE = 0.2
RESERVE_POWER = 4

# --- Sigmoid --- #
class Sigmoid:
    """
    Sigmoid curve
    Link to default data: https://raw.githubusercontent.com/longtailfinancial/ltf_library/main/src/ltf/data/bondingcurves_initial_values.csv
    ...

    Attributes
    ----------
    data : string | pandas DataFrame
        the csv file path | dataframe contains 
        the varibales l, s, m, k, and steps
    l : number that adjusts the y-axis scale 
        default=20.8, bounds=(0, 100)
    s : number that adjusts the supply of tokens
        default=17, bounds=(1, 20)
    m : number that adjusts the slope
        default=21e6, bounds=(1, 21e6)
    k : number of tokens sold
        default=57300, bounds=(1, 1e5)
    steps : Integer 
        default=1000, bounds=(10, 10000)
    zoom : number that affects the scale of the presented view
        default=0.03, bounds=(0.01, 1)
    current_supply : number modeling the current tokens in circulation
        default=10000

    Methods
    -------
    f(x):
        Paramaterized Sigmoid Function.

    x():
        returns values for x axis scale based on m, zoom, steps.

    curve(x):
        Returns a dataframe containing the supply and price based on the X values
        supplied to f(x)

    collateral(x):
        Creates and returns the dataframe containing values that are less than the 
        current token supply

    fig_builder():
        Return a plotly fig object modeling the relationship between the supply
        and the price

    """
    
    def __init__(
        self,
        data=DEFAULT_PATH,
        current_supply=CURRENT_SUPPLY,
        zoom=ZOOM
        ):
        super(Sigmoid, self).__init__()
        if isinstance(data, pd.DataFrame):
            df_data = data
        else:
            try:
                df_data = pd.read_csv(data)
            except:
                raise ValueError('data must be a valid csv file path')
        self.l = df_data['l'][0]
        self.s = df_data['s'][0]
        self.m = df_data['m'][0]
        self.k = df_data['k'][0]
        self.steps = df_data['steps'][0]
        self.zoom = zoom
        self.current_supply = current_supply
        self.supply_upper_bound = self.m*self.zoom
        
    
    def f(self, x):
        """Sigmoid Function"""
        self.supply_upper_bound = self.m*self.zoom
        return self.k/(1+np.exp(-x*self.l/self.m+self.s))

    def x(self):
        x = np.linspace(0,self.m*self.zoom, self.steps)
        return x
    
    def curve(self, x):
        y = self.f(x)
        return pd.DataFrame(zip(x,y),columns=['supply','price'])
    
    def collateral(self, x):
        df = self.curve(x)
        return df[df['supply'] < self.current_supply]
    
    def fig_builder(self):
        """
        return a plotly fig object
        """
        # line plot
        df = self.curve(self.x())
        chart_x = df['supply']
        chart_y = df['price']
        # area plot
        df_area = self.collateral(self.x())
        area_x = df_area['supply']
        area_y = df_area['price']

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=chart_x,
                y=chart_y,
                mode='lines',
                line_color='blue',
                hovertemplate = 'Supply:%{x:.2f}<br>Price: %{y:$.2f}',
                showlegend=False,
                name='Fund')
            )
        fig.add_trace(
            go.Scatter(
                x=area_x,
                y=area_y,
                fill='tozeroy',
                mode='lines',
                line_color='blue',
                hoverinfo='skip',
                showlegend=False
                )
            )
        fig.update_layout(
            barmode='stack',
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
            )
        fig.update_xaxes(title_text='Supply')
        fig.update_yaxes(title_text='Price')
        return fig


# --- Multisigmoid --- #
class MultiSigmoid(Sigmoid):
    """
    Multi-Sigmoid curve that inherits all the methods and attributes from Sigmoid
    Link to default data: https://raw.githubusercontent.com/longtailfinancial/ltf_library/main/src/ltf/data/bondingcurves_initial_values.csv

    Attributes
    ----------

    data : string | pandas DataFrame
        the csv file path | dataframe contains 
        the varibales l, s, m, k, and steps

    l : number that adjusts the y-axis scale 
        default=20.8, bounds=(0, 100)

    s : number that adjusts the supply of tokens
        default=17, bounds=(1, 20)

    m : number that adjusts the slope
        default=21e6, bounds=(1, 21e6)

    k : number of tokens sold
        default=57300, bounds=(1, 1e5)

    NOTE: Each of the additional Sigmoid have their own respective variables appropriately 
        labeled with that curves number. (Ex: l2, s2, m2, k2)

    Methods
    -------
    f2(x): Calculates the second Sigmoid curve fundamental function

    f3(x): Calculates the third Sigmoid curve fundamental function

    f4(x): Calculates the fourth Sigmoid curve fundamental function

    f(x): Returns the sum of the original Sigmoid curve plus f2(), f3(), and f4()


    """
    
    def __init__(
        self,
        data=DEFAULT_PATH,
        current_supply=CURRENT_SUPPLY,
        zoom=ZOOM
        ):
        super(MultiSigmoid, self).__init__(data, current_supply, zoom)
        if isinstance(data, pd.DataFrame):
            df_data = data
        else:
            try:
                df_data = pd.read_csv(data)
            except:
                raise ValueError('data must be a valid csv file path')
        
        self.l = df_data['l'][0]
        self.s = df_data['s'][0]
        self.m = df_data['m'][0]
        self.k = df_data['k'][0]
        #2
        self.l2 = df_data['l'][1]
        self.s2 = df_data['s'][1]
        self.m2 = df_data['m'][1]
        self.k2 = df_data['k'][1]
        #3
        self.l3 = df_data['l'][2]
        self.s3 = df_data['s'][2]
        self.m3 = df_data['m'][2]
        self.k3 = df_data['k'][2]
        #4
        self.l4 = df_data['l'][3]
        self.s4 = df_data['s'][3]
        self.m4 = df_data['m'][3]
        self.k4 = df_data['k'][3]


    def f2(self, x):
        return self.k2/(1+np.exp(-x*self.l2/self.m2+self.s2))
    
    def f3(self, x):
        return self.k3/(1+np.exp(-x*self.l3/self.m3+self.s3))
    
    def f4(self, x):
        return self.k4/(1+np.exp(-x*self.l4/self.m4+self.s4))

    def f(self, x):
        """
        The fundamental function for this class as it calls all the other functions
        and returns the sum of their values.
        """
        return super(MultiSigmoid, self).f(x) + self.f2(x) + self.f3(x) + self.f4(x)


# --- Augumented --- #
class Augmented(MultiSigmoid):
    """
    Model the Augmented MultiSigmoid bonding Curve. 
    Link to default data:

    Attributes
    ----------

    reserve_rate: number that represents the reserve rate of the curve.
                default=0.2, bounds=(0, 1), step=0.01

    NOTE: Inherits all previous attributes.


    Methods
    -------
    curve(x):
        Calculates and returns an Augmented bonding curve data frame that shows
        the supply, price, minted  tokens, reserve, and funding of the curve as a whole

    reserves():
        Returns data frame of the collateral and includes the net gains of the curve 

    view_collateral():
        Returns a plotly fig object of the collateral against the curve

    view_reserves():
        Returns a data frame showing the sum of the reserves in regards to CAD

    """
    def __init__(
        self,
        data=DEFAULT_PATH,
        current_supply=CURRENT_SUPPLY,
        zoom=ZOOM,
        reserve_rate_input=RESERVE_RATE
        ):
        super(Augmented, self).__init__(data, current_supply, zoom)
        self.reserve_rate = reserve_rate_input
    
    def curve(self, x):
        y = self.f(x)
        curve = pd.DataFrame(zip(x,y), columns=['supply','price'])
        curve['sell_price'] = curve['price'] * self.reserve_rate
        curve['minted'] = curve['supply'].diff()
        curve['reserve'] = curve['sell_price']*curve['minted']
        curve['funding'] = curve['price']*(1-self.reserve_rate)*curve['minted']
        return curve.bfill()
    
    def reserves(self):
        x = self.x()
        reserves = self.collateral(x)
        reserves['net'] = reserves['funding'] + reserves['reserve']
        return reserves[['funding','reserve', 'net']].sum()
    
    def view_collateral(self):
        x = self.x()
        df = self.collateral(x).rename(columns={'price':'funding_price','sell_price':'reserve_price'})
        print(df.columns)
        fig = self.fig_builder()
        fig.add_trace(
            go.Scatter(x=df['supply'], y=df['reserve_price'], fill='tozeroy', mode='lines', line_color='red',hovertemplate = 'Supply:%{x:.2f}<br>Price: %{y:$.2f}', showlegend=False, name='Reserve')
            )
        fig.update_layout(hovermode="x")
        return fig

    def view_reserves(self):
        r = self.reserves().to_frame()
        r.columns = ['CAD']
        r['CAD'] = r['CAD'].apply(lambda x: "${:,.2f}".format(x))
        return r


# --- Smart --- #
class Smart(Augmented):
    """
    Model the Smart augmented MultiSigmoid bonding Curve. 

    Attributes
    ----------

    reserve_power: The power at which the curves reserve ratio is calculated
    Link to default data:

    NOTE: Inherits all previous attributes.

    Methods
    -------

    collateral(x):
        Creates and returns a data frame of the collateral against the curve and the 
        selling curve.

    curve(x):
        Same as the curve function from earlier, but missing values are now filled with 
        .bfill() from pandas 

    """
    
    def __init__(
        self,
        csv_path=DEFAULT_PATH,
        current_supply=CURRENT_SUPPLY,
        zoom=ZOOM,
        reserve_rate_input=RESERVE_RATE,
        reserve_power_input=RESERVE_POWER
        ):
        super(Smart, self).__init__(csv_path, current_supply, zoom, reserve_rate_input)
        self.reserve_power = reserve_power_input
        self.reserve_rate = 1
        
    def collateral(self, x):
        curve = self.curve(x)
        curve = curve[curve['supply'] < self.current_supply]
        reserve_rate = np.power(np.linspace(0,1,len(curve)), self.reserve_power) * self.reserve_rate
        curve['sell_price'] = curve['price'] * reserve_rate
        curve['minted'] = curve['supply'].diff()
        curve['reserve'] = curve['sell_price']*curve['minted']
        curve['funding'] = curve['price']*(1-reserve_rate)*curve['minted']
        return curve
        
    def curve(self, x):
        y = self.f(x)
        curve = pd.DataFrame(zip(x,y),columns=['supply','price'])
        return curve.bfill()


# --- Token Engineering --- #
class TokenEngineering:
    """
    Attributes
    ----------
    company: string that represents the company name
    monthly_salary: float
        default=5000, bounds=(1500, 5000), step=500
    number_employees: float
        default=7, bounds=(3, 12), step=1
    number_months: float
        default=24, bounds=(3, 24), step=1
    monthly_contract_size: float
        default=7500, bounds=(6000, 10000), step=50
    number_of_initial_contracts: float
        default=2, bounds=(1, 10), step=1
    new_contracts_per_month: float
        default=0.33, bounds=(0, 3), step=0.33
    office_expense: float
        default=7000, bounds=(3000, 7000), step=50
    """

    def __init__(self, **kwargs):
        self.company = kwargs.get('company', 'LTF')
        self.monthly_salary = kwargs.get('monthly_salary', 5000)
        self.number_employees = kwargs.get('number_employees', 7)
        self.number_months = kwargs.get('number_months', 24)
        self.monthly_contract_size = kwargs.get('monthly_contract_size', 7500)
        self.number_of_initial_contracts = kwargs.get('number_of_initial_contracts', 2)
        self.new_contracts_per_month = kwargs.get('new_contracts_per_month', 0.33)
        self.office_expense = kwargs.get('office_expense', 7000)

    def salary_costs(self):
        cummulative = [i*self.number_employees * self.monthly_salary for i in range(self.number_months)]
        return cummulative

    def office_expenses(self):
        cummulative = [
            i*self.office_expense for i in range(self.number_months)]
        return cummulative

    def costs(self):
        return [a+b for a, b in zip(self.salary_costs(), self.office_expenses())]

    def number_of_contracts(self):
        cummulative = [i*self.new_contracts_per_month + self.number_of_initial_contracts for i in range(self.number_months)]
        return cummulative

    def contract_revenue(self):
        number_of_contracts = self.number_of_contracts()
        cummulative = [i*self.monthly_contract_size*number_of_contracts[i] for i in range(self.number_months)]
        return cummulative

    def ltf_treasury(self):
        return [a-b for a, b in zip(self.contract_revenue(), self.costs())]

    def cummulative_data(self):
        data = pd.DataFrame({
            'Contract Revenue': self.contract_revenue(),
            'Number of Contracts': self.number_of_contracts(),
            'Salary Costs': self.salary_costs(),
            'Net Profit': self.ltf_treasury(),
            'Office Expenses': self.office_expenses()})
        data.index.name = 'Month'
        return data

    def results(self):
        return self.cummulative_data().iloc[[-1]]

    def results_view(self):
        return self.results().reset_index()

    def chart_view(self):
        df = self.cummulative_data()
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df.index,
                    y=df['Contract Revenue'],
                    name='Contract Revenue',
                    line=dict(color='#17BECF'),
                    hovertemplate = 'Month: %{x}<br>Value: %{y:$.2f}'
                ),
                go.Scatter(
                    x=df.index,
                    y=df['Number of Contracts'],
                    name='Number of Contracts',
                    line=dict(color='#7F7F7F'),
                    hovertemplate = 'Month: %{x}<br>Value: %{y:$.2f}'
                ),
                go.Scatter(
                    x=df.index,
                    y=df['Salary Costs'],
                    name='Salary Costs',
                    line=dict(color='#FF7F0E'),
                    hovertemplate = 'Month: %{x}<br>Value: %{y:$.2f}'
                ),
                go.Scatter(
                    x=df.index,
                    y=df['Net Profit'],
                    name='Net Profit',
                    line=dict(color='#D62728'),
                    hovertemplate = 'Month: %{x}<br>Value: %{y:$.2f}'
                ),
                go.Scatter(
                    x=df.index,
                    y=df['Office Expenses'],
                    name='Office Expenses',
                    line=dict(color='#2CA02C'),
                    hovertemplate = 'Month: %{x}<br>Value: %{y:$.2f}'
                )
            ],
            layout=go.Layout(
                title=f'{self.company} Treasury',
                xaxis=dict(
                    title='Month',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                ),
                yaxis=dict(
                    title='USD',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            )
        )
        fig.update_layout(hovermode="x")
        return fig



# --- Bonding Curve --- #
class Bonding(Smart):
    
    def batch_minted(self):
        return self.current_supply - self.collateral(self.x()).iloc[-1]['supply']
    
    def batch_available(self):
        return self.collateral(self.x()).iloc[-1]['minted'] - self.batch_minted()
    
    def current_price(self):
        return self.collateral(self.x()).iloc[-1]['price']
    
    def mint(self, CAD: float, tol=1e-6):
        self.zoom = 0.05
        current_price = self.current_price()
        requested = CAD/current_price
        batch_available = self.batch_available()
        if batch_available < tol:
            self.current_supply += tol
            return self.mint(CAD)
        
        if requested <= batch_available:
            self.current_supply += requested
            received = requested
            return received, current_price
        
        else:
            self.current_supply += batch_available
            next_received, next_price =  self.mint(current_price*(requested-batch_available))
            total_received = next_received + batch_available
            weighted_price = current_price*(batch_available/total_received) + next_price*(next_received/total_received)
            return total_received, weighted_price
        

    def view_market(self):
        df = pd.DataFrame({
            'price' : self.current_price(),
            'supply' : int(self.current_supply),
            'marketcap' : self.current_price() * self.current_supply,
        },index=['LTT'])
        df['price'] = df['price'].apply(lambda x: "${:,.2f}".format(x))
        df['marketcap'] = df['marketcap'].apply(lambda x: "${:,.0f}".format(x))
        return df.T
    