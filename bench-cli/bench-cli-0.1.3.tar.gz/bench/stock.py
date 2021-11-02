import requests
import json
import numpy as np
import pandas as pd
from requests import Session
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor
from datetime import date


class Stock:
    def __init__(self, token, version, ticker, period, num_periods):
        """
        Class for stock data.

        Parameters
        ----------
        token : str
            API token for IEX Cloud.
        version : str
            API version. Can be "stable" or "test".
        ticker : str
            Stock ticker or symbol. (eg. "MSFT").
        period : str
            Period intervals for financial data. Can be "annual" or "quarterly"
        num_periods : int
            The number of historical periods.

        Attributes
        ----------
        token : str
            API token for IEX Cloud.
        version : str
            API version. Can be "stable" or "test".
        ticker : str
            Stock ticker or symbol. (eg. "MSFT").
        period : str
            Period intervals for financial data. Can be "annual" or "quarterly"
        num_periods : int
            The number of historical periods.
        api_requests: tuple(str, str)
            Tuple of API endpoints for iex_company and iex_fundamentals.
        iex_company : pd.DataFrame
            DataFrame of IEX Cloud's company data for ticker.
        iex_fundamentals: pd.DataFrame
            DataFrame of IEX Cloud's fundamentals data for ticker.
        transformations : pd.DataFrame
            DataFrame of all data, including tranformations.
        company : pd.DataFrame
            DataFrame of company data.
        fundamentals : pd.DataFrame
            DataFrame of fundamental data.
        metrics : pd.DataFrame
            DataFrame of company metrics data.

        """
        self.ticker = ticker
        self.token = token
        self.version = version
        self.iex_base_url = self.iex_base_url()
        self.period = period
        self.num_periods = num_periods
        self.api_requests = self.api_requests()
        self.iex_company = self.iex_company()
        self.iex_fundamentals = self.iex_fundamentals()
        self.transformations = self.transformations()
        self.company = self.company()
        self.fundamentals = self.fundamentals()
        self.metrics = self.metrics()

    def iex_base_url(self):
        """Returns the base url for the API endpoint.

        Returns
        -------
        str
            IEX Cloud API base url.

        """
        base_url = "https://cloud.iexapis.com/"
        test_url = "https://sandbox.iexapis.com/stable"

        if self.version == "stable":
            url = base_url + "stable"
        elif self.version == "test":
            url = test_url

        return url

    def api_requests(self):
        """Concatenate API endpoint urls from Class Attributes

        Raises
        -------
        JSONDecodeError
            There was an issue with the way JSON data was formatted. Returns None.

        Returns
        -------
        tuple(str, str)
            Tuple of API endpoints for iex_company and iex_fundamentals.

        """
        session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))

        try:
            session = FuturesSession()

            company_url = (
                session.get(
                    f"{self.iex_base_url}/stock/{self.ticker}/company?token={self.token}"
                )
                .result()
                .json()
            )

            fundamentals_url = (
                session.get(
                    f"{self.iex_base_url}/time-series/fundamentals/{self.ticker}/{self.period}?last={self.num_periods}&token={self.token}"
                )
                .result()
                .json()
            )

            return company_url, fundamentals_url

        except json.JSONDecodeError:
            print(
                f"Decoding JSON for ticker {self.ticker} has failed. Canceling request for {self.ticker}"
            )

    def iex_company(self):
        """Creates and filters DataFrame with IEX company data.

        Returns
        -------
        pd.DataFrame
            DataFrame of IEX Cloud's company data for ticker.

        """
        df = pd.json_normalize(self.api_requests[0])

        df["lastUpdated"] = date.today()

        df = df[
            [
                "symbol",
                "companyName",
                "country",
                "exchange",
                "industry",
                "sector",
                "lastUpdated",
            ]
        ]

        df["industry"] = df["industry"].str.replace(",", ".")

        return df

    def iex_fundamentals(self):
        """Creates and filters DataFrame with IEX fundamentals data.

        Returns
        -------
        pd.DataFrame
            DataFrame of IEX Cloud's fundamentals data for ticker.

        """
        df = pd.json_normalize(self.api_requests[1])

        if self.period == "annual":
            df["filingYear"] = df["filingDate"].str.split("-").str[0]
            df["filingQuarter"] = np.nan
            df["periodType"] = "annual"
            df["periodKey"] = (f"{self.ticker}" + "a" + df["filingYear"]).str.lower()
        else:
            df["filingYear"] = df["filingDate"].str.split("-").str[0]
            df["filingQuarter"] = df["fiscalQuarter"].astype(str)
            df["periodType"] = "quarterly"
            df["periodKey"] = (
                f"{self.ticker}" + "q" + df["filingYear"] + df["filingQuarter"]
            ).str.lower()

        def neg_to_positive(df):

            try:
                for col in df.iteritems:
                    df[col].apply(lambda x: x.abs() if x < 0 else x)
            except TypeError:
                return df

        df = neg_to_positive(df)

        df["lastUpdated"] = date.today()

        return df

    def transformations(self):
        """Calculates and transforms the ticker's fundamentals data to calculate metrics.

        Returns
        -------
        pd.DataFrame
            DataFrame of all data, including tranformations.

        """
        # loading data
        df = self.iex_fundamentals

        # get the tax rate, make adjustments, change in NWC, and define NOPAT & free cash flow
        df["nopat"] = (df["incomeOperating"] * (1 - df["incomeTaxRate"])).astype(int)

        # LIFO to FIFO adjustment for COGS and Inventory
        def lifo_adjustment(x):
            x["lifoDelta"] = (
                (x["reservesLifo"] - x["reservesLifo"].shift(periods=-1)).fillna(0)
            ).astype(int)
            x1 = list(x["reservesLifo"])
            x2 = list(x["lifoDelta"])
            x3 = list(x["inventory"])
            x4 = list(x["salesCost"])

            def myfunc(x1, x2):
                result = [v1 + v2 if v1 > 0 else v2 for v1, v2 in zip(x1, x2)]
                return result

            def myfunc2(x1, x2):
                result = [v2 - v1 if v1 != 0 else v2 for v1, v2 in zip(x1, x2)]
                return result

            ai = myfunc(x1, x3)
            ac = myfunc2(x2, x4)

            return ai, ac

        ai, ac = lifo_adjustment(df)
        df["adjInventory"] = ai
        df["adjInventory"] = df["adjInventory"].astype(int)
        df["adjCOGS"] = ac
        df["adjCOGS"] = df["adjCOGS"].astype(int)
        df["nonCashWorkingCapital"] = (
            (df["accountsReceivable"] + df["adjInventory"])
            - (df["accountsPayable"] + df["nibclRevenueDeferred"])
        ).astype(int)
        df["nonCashWorkingCapitalDelta"] = (
            (
                df["nonCashWorkingCapital"]
                - df["nonCashWorkingCapital"].shift(periods=-1)
            ).fillna(0)
        ).astype(int)

        # Free cash flow
        df["fcf"] = (
            (
                df["nopat"]
                + df["expensesDepreciationAndAmortization"]
                - df["nonCashWorkingCapitalDelta"]
                - df["capex"]
            )
        ).astype(int)

        # margin ratios
        df["grossMargin"] = (df["profitGross"] / df["revenue"]) * 100
        df["operatingMargin"] = (df["incomeOperating"] / df["revenue"]) * 100
        df["ebitdaMargin"] = (df["ebitdaReported"] / df["revenue"]) * 100
        df["ebitMargin"] = (df["ebitReported"] / df["revenue"]) * 100
        df["fcfMargin"] = (df["fcf"] / df["revenue"].values) * 100
        df["niMargin"] = (df["incomeNet"] / df["revenue"]) * 100

        # expense metrics
        df["sgaToRev"] = (df["expensesSga"] / df["revenue"]) * 100
        df["rndToRev"] = (df["researchAndDevelopmentExpense"] / df["revenue"]) * 100
        df["sbcToRev"] = (df["expensesStockCompensation"] / df["revenue"]) * 100
        df["capexToRev"] = (df["capex"] / df["revenue"]) * 100
        df["capexToFcf"] = (df["capex"] / df["fcf"]) * 100
        df["acquisitionCapexToRev"] = (df["capexAcquisition"] / df["revenue"]) * 100
        df["maintenanceCapexToRev"] = (df["capexMaintenance"] / df["revenue"]) * 100
        df["acquisitionCapexToFcf"] = (df["capexAcquisition"] / df["fcf"]) * 100
        df["maintenanceCapexToFcf"] = (df["capexMaintenance"] / df["fcf"]) * 100

        # return ratios
        df["ROA"] = (df["incomeNet"] / df["assetsUnadjusted"]) * 100

        # define average shareholder's equity
        df["avgShareholdersEquity"] = (
            (
                df["equityShareholder"].shift(periods=-1) + df["equityShareholder"]
            ).fillna(0)
        ) * 100
        df["ROE"] = (df["incomeNet"] / df["avgShareholdersEquity"]) * 100

        # define invested capital, ROIC, ROIC, CFROIC, CFROIIC
        df["investedCapital"] = (
            (
                df["nonCashWorkingCapital"]
                + df["ppAndENet"]
                + df["assetsFixedDeferredCompensation"]
                + df["assetsFixedDeferredTax"]
                + df["assetsFixedLeasesOperating"]
                + df["assetsFixedOperatingSubsidiaryUnconsolidated"]
                + df["assetsFixedOther"]
                + df["goodwillAndIntangiblesNetOther"]
                + df["liabilitiesNonCurrentLeasesOperating"]
                + df["nibclLeasesOperating"]
            )
        ).astype(int)

        df["cashInvestedCapital"] = (
            (df["investedCapital"] + df["depreciationAndAmortizationAccumulated"])
        ).astype(int)

        df["ROIC"] = (df["nopat"] / df["investedCapital"].shift(periods=-1)) * 100
        df["ROIIC"] = (
            (df["nopat"] - df["nopat"].shift(periods=-1))
            / (
                df["investedCapital"].shift(periods=-1)
                - df["investedCapital"].shift(periods=-2)
            )
        ) * 100
        df["CROIC"] = (df["fcf"] / df["cashInvestedCapital"]) * 100
        df["CROIIC"] = (
            (df["fcf"] - df["nopat"].shift(periods=-1))
            / (
                df["cashInvestedCapital"].shift(periods=-1)
                - df["cashInvestedCapital"].shift(periods=-2)
            )
        ) * 100

        # activity ratios
        df["avgTotalAssets"] = (
            (
                (
                    df["assetsUnadjusted"].shift(periods=-1) + df["assetsUnadjusted"]
                ).fillna(0)
            )
            / 2
        ).astype(int)

        df["avgInventory"] = (
            ((df["adjInventory"].shift(periods=-1) + df["adjInventory"]).fillna(0)) / 2
        ).astype(int)

        df["avgAR"] = (
            (
                (
                    df["accountsReceivable"].shift(periods=-1)
                    + df["accountsReceivable"]
                ).fillna(0)
            )
            / 2
        ).astype(int)

        df["avgAP"] = (
            (
                (
                    df["accountsPayable"].shift(periods=-1) + df["accountsPayable"]
                ).fillna(0)
            )
            / 2
        ).astype(int)

        df["assetTurnover"] = df["revenue"] / df["avgTotalAssets"]
        df["inventoryTurnover"] = df["salesCost"] / df["avgInventory"]
        df["receivablesTurnover"] = df["revenue"] / df["avgAR"]
        df["payablesTurnover"] = df["salesCost"] / df["avgAP"]
        # -----------------------------------------------
        df["DSO"] = (1 / df["receivablesTurnover"]) * 365
        df["DIO"] = (1 / df["inventoryTurnover"]) * 365
        df["DPO"] = (1 / df["payablesTurnover"]) * 365
        df["CCC"] = df["DSO"] + df["DIO"] - df["DPO"]

        # growth
        df["revenueGrowth"] = (
            (df["revenue"] / df["revenue"].shift(periods=-1)) - 1
        ).fillna(0) * 100
        df["fcfGrowth"] = ((df["fcf"] / df["fcf"].shift(periods=-1)) - 1).fillna(
            0
        ) * 100
        df["ebitdaGrowth"] = (
            (df["ebitdaReported"] / df["ebitdaReported"].shift(periods=-1)) - 1
        ).fillna(0) * 100
        df["ebitGrowth"] = (
            (df["ebitReported"] / df["ebitReported"].shift(periods=-1)) - 1
        ).fillna(0) * 100

        # function to calculate CAGRs
        def cagrs(frame, datapoint, n):
            x = frame[datapoint].tolist()

            col = [
                round(np.real(((((x[i] / x[n + i]) ** (1 / n)) - 1) * 100)), 2)
                if x[n + i] != 0
                else 0
                for i, val in enumerate(x)
                if i < len(x) - n
            ]
            result = pd.Series(col)
            return result

        df["3yearRevenueCAGR"] = cagrs(df, "revenue", 3)
        df["5yearRevenueCAGR"] = cagrs(df, "revenue", 5)
        df["10yearRevenueCAGR"] = cagrs(df, "revenue", 10)

        df["3yearFcfCAGR"] = cagrs(df, "fcf", 3)
        df["5yearFcfCAGR"] = cagrs(df, "fcf", 5)
        df["10yearFcfCAGR"] = cagrs(df, "fcf", 10)

        df["3yearEbitdaCAGR"] = cagrs(df, "ebitdaReported", 3)
        df["5yearEbitdaCAGR"] = cagrs(df, "ebitdaReported", 5)
        df["10yearEbitdaCAGR"] = cagrs(df, "ebitdaReported", 10)

        # Rounding all floats to one decimal place
        df = df.round(2)

        return df

    def company(self):
        """Company data

        Returns
        -------
        pd.DataFrame
            DataFrame of company data.

        """
        df = self.iex_company
        return df

    def fundamentals(self):
        """Sorted fundamentals data

        Returns
        -------
        pd.DataFrame
            DataFrame of fundamentals data.

        """
        df = self.transformations

        df = df[
            [
                "periodKey",
                "periodType",
                "filingDate",
                "filingYear",
                "filingQuarter",
                "fiscalYear",
                "fiscalQuarter",
                "dataGenerationDate",
                "periodEndDate",
                "filingType",
                "accountsPayable",
                "accountsReceivable",
                "assetsCurrentCash",
                "assetsCurrentCashRestricted",
                "assetsCurrentDeferredCompensation",
                "assetsCurrentDeferredTax",
                "assetsCurrentDiscontinuedOperations",
                "assetsCurrentInvestments",
                "assetsCurrentLeasesOperating",
                "assetsCurrentLoansNet",
                "assetsCurrentOther",
                "assetsCurrentSeparateAccounts",
                "assetsCurrentUnadjusted",
                "assetsFixed",
                "assetsFixedDeferredCompensation",
                "assetsFixedDeferredTax",
                "assetsFixedDiscontinuedOperations",
                "assetsFixedLeasesOperating",
                "assetsFixedOperatingDiscontinuedOperations",
                "assetsFixedOperatingSubsidiaryUnconsolidated",
                "assetsFixedOreo",
                "assetsFixedOther",
                "assetsFixedUnconsolidated",
                "assetsUnadjusted",
                "capex",
                "capexAcquisition",
                "capexMaintenance",
                "cashFlowFinancing",
                "cashFlowInvesting",
                "cashFlowOperating",
                "cashFlowShareRepurchase",
                "cashLongTerm",
                "cashOperating",
                "cashPaidForIncomeTaxes",
                "cashPaidForInterest",
                "cashRestricted",
                "chargeAfterTax",
                "chargeAfterTaxDiscontinuedOperations",
                "chargesAfterTaxOther",
                "creditLossProvision",
                "debtFinancial",
                "debtShortTerm",
                "depreciationAndAmortizationAccumulated",
                "depreciationAndAmortizationCashFlow",
                "dividendsPreferred",
                "dividendsPreferredRedeemableMandatorily",
                "earningsRetained",
                "ebitReported",
                "ebitdaReported",
                "equityShareholder",
                "equityShareholderOther",
                "equityShareholderOtherDeferredCompensation",
                "equityShareholderOtherEquity",
                "equityShareholderOtherMezzanine",
                "expenses",
                "expensesAcquisitionMerger",
                "expensesCompensation",
                "expensesDepreciationAndAmortization",
                "expensesDerivative",
                "expensesDiscontinuedOperations",
                "expensesDiscontinuedOperationsReits",
                "expensesEnergy",
                "expensesForeignCurrency",
                "expensesInterest",
                "expensesInterestFinancials",
                "expensesInterestMinority",
                "expensesLegalRegulatoryInsurance",
                "expensesNonOperatingCompanyDefinedOther",
                "expensesNonOperatingOther",
                "expensesNonOperatingSubsidiaryUnconsolidated",
                "expensesNonRecurringOther",
                "expensesOperating",
                "expensesOperatingOther",
                "expensesOperatingSubsidiaryUnconsolidated",
                "expensesOreo",
                "expensesOreoReits",
                "expensesOtherFinancing",
                "expensesRestructuring",
                "expensesSga",
                "expensesStockCompensation",
                "expensesWriteDown",
                "ffo",
                "goodwillAmortizationCashFlow",
                "goodwillAmortizationIncomeStatement",
                "goodwillAndIntangiblesNetOther",
                "goodwillNet",
                "incomeFromOperations",
                "incomeNet",
                "incomeNetPreTax",
                "incomeOperating",
                "incomeOperatingDiscontinuedOperations",
                "incomeOperatingOther",
                "incomeOperatingSubsidiaryUnconsolidated",
                "incomeOperatingSubsidiaryUnconsolidatedAfterTax",
                "incomeTax",
                "incomeTaxCurrent",
                "incomeTaxDeferred",
                "incomeTaxRate",
                "interestMinority",
                "inventory",
                "liabilities",
                "liabilitiesCurrent",
                "liabilitiesNonCurrentAndInterestMinorityTotal",
                "liabilitiesNonCurrentDebt",
                "liabilitiesNonCurrentDeferredCompensation",
                "liabilitiesNonCurrentDeferredTax",
                "liabilitiesNonCurrentDiscontinuedOperations",
                "liabilitiesNonCurrentLeasesOperating",
                "liabilitiesNonCurrentLongTerm",
                "liabilitiesNonCurrentOperatingDiscontinuedOperations",
                "liabilitiesNonCurrentOther",
                "nibclDeferredCompensation",
                "nibclDeferredTax",
                "nibclDiscontinuedOperations",
                "nibclLeasesOperating",
                "nibclOther",
                "nibclRestructuring",
                "nibclRevenueDeferred",
                "nibclSeparateAccounts",
                "oci",
                "ppAndENet",
                "profitGross",
                "researchAndDevelopmentExpense",
                "reserves",
                "reservesInventory",
                "reservesLifo",
                "reservesLoanLoss",
                "revenue",
                "revenueCostOther",
                "revenueIncomeInterest",
                "revenueOther",
                "revenueSubsidiaryUnconsolidated",
                "salesCost",
                "sharesIssued",
                "sharesOutstandingPeDateBs",
                "sharesTreasury",
                "stockCommon",
                "stockPreferred",
                "stockPreferredEquity",
                "stockPreferredMezzanine",
                "stockTreasury",
                "wabso",
                "wabsoSplitAdjusted",
                "wadso",
                "wadsoSplitAdjusted",
                "nopat",
                "lifoDelta",
                "adjInventory",
                "adjCOGS",
                "nonCashWorkingCapital",
                "nonCashWorkingCapitalDelta",
                "fcf",
                "investedCapital",
                "cashInvestedCapital",
                "avgTotalAssets",
                "avgInventory",
                "avgAR",
                "avgAP",
            ]
        ]

        return df

    def metrics(self):
        """Sorted metrics data

        Returns
        -------
        pd.DataFrame
            DataFrame of metrics data.

        """
        df = self.transformations

        df = df[
            [
                "periodKey",
                "periodType",
                "filingDate",
                "filingYear",
                "filingQuarter",
                "fiscalYear",
                "fiscalQuarter",
                "grossMargin",
                "operatingMargin",
                "ebitdaMargin",
                "ebitMargin",
                "fcfMargin",
                "niMargin",
                "revenueGrowth",
                "fcfGrowth",
                "ebitdaGrowth",
                "ebitGrowth",
                "3yearRevenueCAGR",
                "5yearRevenueCAGR",
                "10yearRevenueCAGR",
                "3yearFcfCAGR",
                "5yearFcfCAGR",
                "10yearFcfCAGR",
                "3yearEbitdaCAGR",
                "5yearEbitdaCAGR",
                "10yearEbitdaCAGR",
                "sgaToRev",
                "rndToRev",
                "sbcToRev",
                "capexToRev",
                "capexToFcf",
                "acquisitionCapexToRev",
                "maintenanceCapexToRev",
                "acquisitionCapexToFcf",
                "maintenanceCapexToFcf",
                "ROA",
                "ROE",
                "ROIC",
                "ROIIC",
                "CROIC",
                "CROIIC",
                "assetTurnover",
                "receivablesTurnover",
                "payablesTurnover",
                "DSO",
                "DIO",
                "DPO",
                "CCC",
            ]
        ]

        return df
