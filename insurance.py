from util import *

source_data = {
    'Hail Endorsement Rate': 1.92,
    'Spring Insured Price': 8.71,
    'Your Normal (Risk Area 4)':{
        'Fallow':{
            '50% Cover Level':{
                'Yield Guarantee': 15.9,
                'Dollars Liability': 138.72,
                'Crop Insurance Premium Per Acre': 2,
                'Hail Premium Per Acre': 0,
                'Total Premium Per Acre': 2
            },
            '60% Cover Level':{
                'Yield Guarantee': 19.1,
                'Dollars Liability': 166.46,
                'Crop Insurance Premium Per Acre': 4.39,
                'Hail Premium Per Acre': 3.2,
                'Total Premium Per Acre': 7.59
            },
            '70% Cover Level':{
                'Yield Guarantee': 22.3,
                'Dollars Liability': 194.21,
                'Crop Insurance Premium Per Acre': 7.46,
                'Hail Premium Per Acre': 3.73,
                'Total Premium Per Acre': 11.19
            },
            '80% Cover Level':{
                'Yield Guarantee': 25.5,
                'Dollars Liability': 221.95,
                'Crop Insurance Premium Per Acre': 11.9,
                'Hail Premium Per Acre': 4.26,
                'Total Premium Per Acre': 16.16
            },
        },
        'Stubble':{
            '50% Cover Level':{
                'Yield Guarantee': 12.6,
                'Dollars Liability': 109.76,
                'Crop Insurance Premium Per Acre': 2.38,
                'Hail Premium Per Acre': 0,
                'Total Premium Per Acre': 2.38
            },
            '60% Cover Level':{
                'Yield Guarantee': 15.1,
                'Dollars Liability': 131.71,
                'Crop Insurance Premium Per Acre': 4.58,
                'Hail Premium Per Acre': 2.53,
                'Total Premium Per Acre': 7.11
            },
            '70% Cover Level':{
                'Yield Guarantee': 17.6,
                'Dollars Liability': 153.66,
                'Crop Insurance Premium Per Acre': 7.31,
                'Hail Premium Per Acre': 2.95,
                'Total Premium Per Acre': 10.26
            },
            '80% Cover Level':{
                'Yield Guarantee': 20.2,
                'Dollars Liability': 175.62,
                'Crop Insurance Premium Per Acre': 11.13,
                'Hail Premium Per Acre': 3.37,
                'Total Premium Per Acre': 14.50
            },
        },
        'Irrigated':{
            '50% Cover Level':{
                'Yield Guarantee': 41.1,
                'Dollars Liability': 357.76,
                'Crop Insurance Premium Per Acre': 1.25,
                'Hail Premium Per Acre': 0,
                'Total Premium Per Acre': 1.25
            },
            '60% Cover Level':{
                'Yield Guarantee': 49.3,
                'Dollars Liability': 429.31,
                'Crop Insurance Premium Per Acre': 2.75,
                'Hail Premium Per Acre': 8.24,
                'Total Premium Per Acre': 10.99
            },
            '70% Cover Level':{
                'Yield Guarantee': 57.5,
                'Dollars Liability': 500.86,
                'Crop Insurance Premium Per Acre': 4.21,
                'Hail Premium Per Acre': 9.62,
                'Total Premium Per Acre': 13.83
            },
            '80% Cover Level':{
                'Yield Guarantee': 65.7,
                'Dollars Liability': 572.42,
                'Crop Insurance Premium Per Acre': 6.41,
                'Hail Premium Per Acre': 10.99,
                'Total Premium Per Acre': 17.4
            },
        }
    }
}

class AgriInsuranc:
    def __init__(self, expected_yield_level, cover_level:int, risk_area:int) -> None:
        self.expected_yield_level = expected_yield_level    # fallow, stubble, or irrigated
        self.cover_level = cover_level  # the % of cover level
        self.risk_area = risk_area
        self.hail_endorsement_rate = source_data['Hail Endorsement Rate']
        self.spring_insured_price = source_data['Spring Insured Price']
        
        insurance_detail = source_data[f'Your Normal (Risk Area {self.risk_area})'][self.expected_yield_level][f"{cover_level}% Cover Level"]
        self.yield_guarantee = insurance_detail['Yield Guarantee']
        self.dollars_liability = insurance_detail['Dollars Liability']
        self.crop_insurance_premium_per_acre = insurance_detail['Crop Insurance Premium Per Acre']
        self.hail_premium_per_acre = insurance_detail['Hail Premium Per Acre']
        self.total_premium_per_acre = insurance_detail['Total Premium Per Acre']

    def indemnity_payment(self, actual_yield):
        """
        calculate the indemnity payment per Acre

        :param actual_yield: The actual yield per Acre
    
        """
        payment = max((self.yield_guarantee - actual_yield) * self.spring_insured_price, 0)
        return payment
    
    @property
    def monthly_premium(self) -> float:
        """
        calculate the monthly premium per Acre
        """
        total_premium = self.total_premium_per_acre
        return total_premium

    def premium_pay_date(self, adate) -> bool:
        """
        Assume the premium paid at the end month. Determine adate is the premium_pay_date
        
        :return bool: is need to pay premium
        """
        is_pay_premium = is_end_of_month(adate)
        return is_pay_premium


