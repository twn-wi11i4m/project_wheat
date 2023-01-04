from util import *
from data_source import *



class AgriInsurance:
    spring_price = {
        'canolapolish':16.33,
        'canolaargentine':16.33,
        'CPS':8.44,
        'HRS':8.71
        }
    number_of_crops = 0

    #initiate class with instance variables: 
    def __init__(self, farm:object, insured_acres:int, crop, field, coverage, include_hail_endorsement:bool) -> None:
        self.farm = farm    #pass in farm 
        self.insured_acres = insured_acres  #insured_acres: how many acres of crop being insured 
        self.crop = crop#crop: either 'canolapolish', 'canolaargentine', 'CPS', 'HRS'
        self.field = field #field: either "stubble" stubble, "fallow" fallow, or "irrigated" irrigated
        self.coverage = coverage #coverage: either 50, 60, 70 or 80 (percent)
        self.include_hail_endorsement = include_hail_endorsement #include_hail_endorsement: True if yes, False if no
        AgriInsurance.number_of_crops += 1
        self.base_rate_data = BaseRateData()
        self.yield_data = YieldData()
        self.premium_date = PremiumData()

    def get_base_rate(self):
        base_rate = self.base_rate_data.get_base_rate(
            township=self.farm.township,
            range=self.farm.range,
            meridian=self.farm.meridian
        )
        return base_rate
    
    #Method retrives the AFSC yield estimate for the passed in risk area and crop
    #from data in yield.csv
    def get_yield_estimate(self):
        crop_yield_estimate = self.yield_data.get_yield_estimate(
            risk_area=self.farm.risk_area,
            crop=self.crop,
            field=self.field
        )
        return crop_yield_estimate

     # method calculates per acre dollar liability 
    def get_dollars_liability(self): 
        #liability = spring insured price x coverage level x normal expected yield
        dollars_liability = round(
            self.spring_price[self.crop] * self.coverage/100 * self.get_yield_estimate(), 
            2
        )
        return dollars_liability

    # gets the total farm dollar liability 
    def get_total_liability(self): 
        total_liability = self.get_dollars_liability() * self.insured_acres 
        return total_liability

    #method gets the subsidized hail endorsement rate 
    def get_hail_endorsement_rate(self):
        base_rate = self.get_base_rate()
        #if elect for hail endorsement and coverage level is greater than 50%
        if self.include_hail_endorsement and self.coverage > 50:
            if self.crop == "canolapolish" or self.crop == "canolaargentine": 
                hail_endorsement_rate = round(.383 * 1.5 * base_rate, 2) 
            elif self.crop == "peas":
                hail_endorsement_rate = round(.383 * 1.75 * base_rate, 2)
            else: 
                hail_endorsement_rate = round(.383 * base_rate, 2) 
        else: 
            hail_endorsement_rate = 0 
        return hail_endorsement_rate

    #method gets the per acre hail endorsement premium
    def get_per_acre_hail_endorsement_premium(self):
        #hail endorsement premium = dollars liability x hail endorsement rate
        hail_endorsement_premium = round(
            self.get_dollars_liability() * self.get_hail_endorsement_rate()/100,
            2
        )
        return hail_endorsement_premium

    #method gets total farm hail endorsement premium 
    def get_total_hail_endorsement_premium(self):
        #total hail endorsement premium = hail endorsement premium x insured acres 
        total_hail_endorsement_premium = self.get_per_acre_hail_endorsement_premium() * self.insured_acres
        return total_hail_endorsement_premium

    #method retrieves the risk area crop premium as a percentage
    def get_crop_premium_percent(self): 
        percent_premium = self.premium_date.get_crop_premium_percentage(
            risk_area=self.farm.risk_area,
            crop=self.crop,
            field=self.field,
            coverage=self.coverage)
        return percent_premium

    #method retrieves the risk area crop premium as a dollar amount per acre
    def get_per_acre_crop_premium(self):
        crop_premium = round(
            self.get_crop_premium_percent()/100 * self.get_dollars_liability(),
            2
        )
        return crop_premium

    #method retrieves the total crop premium as a dollar amount for all acres insured
    def get_total_crop_premium(self): 
        total_crop_premium = self.get_per_acre_crop_premium()*self.insured_acres
        return total_crop_premium

    #method retrieves the total premium per acre (crop premium + hail endorsement premium)
    def get_total_premium_per_acre(self): 
        acre_total_premium = round(
            self.get_per_acre_crop_premium() + self.get_per_acre_hail_endorsement_premium(),
            2
        )
        return acre_total_premium

    #method retrieves the total premium paid per farm for both crop insurance and hail endorsement
    def get_total_premium(self):
        total_premium = self.get_total_premium_per_acre() * self.insured_acres
        return total_premium

    #calculate yield guarantee under specified coverage level, given expected yield
    def get_yield_guarantee(self): 
        yield_guarantee = self.get_yield_estimate() * self.coverage / 100 
        return yield_guarantee

    #calculates the total indemnity payment, method gets called by passing in final yield
    def calc_indemnity(self, y):
        guarantee = self.get_yield_guarantee() 
        if guarantee > y: 
            payment = round(
                (guarantee - y) * self.spring_price[self.crop] * self.insured_acres,
                2
            )
            print(f"Yield of {y} bu/acre is less than yield guarantee of {guarantee} bu/acre, thus insurance payment of ${payment} received" "\n")
        else: 
            payment = 0
            print(f"Yield of {y} bu/acre is higher than yield guarantee of {guarantee} bu/acre, thus no indemnity payment received" "\n")
        return payment 

    def get_insurance_information(self): 
        print(f"Insurance information for {self.insured_acres} acres of {self.crop} at {self.coverage}% coverage:")
        print(f"Farm Location: mer {self.farm.meridian}, twn {self.farm.township}, rng {self.farm.range}, RA {self.farm.risk_area}")
        if self.include_hail_endorsement:
            print("Farmer has elected for crop insurance with hail endorsement")
        else:
            print("Farmer has elected for crop insurance WITHOUT hail endorsement")
        print(f"The farmers estimated yield is: {self.get_yield_estimate()} bushels/acre, and yield guarantee is: {self.get_yield_guarantee()} bushels/acre")
        print(f"The farmers per/acre premium is: ${self.get_total_premium_per_acre()} and total premium is: ${self.get_total_premium()}" "\n")

    def get_insurance_information_str(self, for_html=False): 
        if for_html:
            s = []
            s.append(f"Insurance information for {self.insured_acres} acres of {self.crop} at {self.coverage}% coverage:")
            s.append(f"Farm Location: mer {self.farm.meridian}, twn {self.farm.township}, rng {self.farm.range}, RA {self.farm.risk_area}")
            if self.include_hail_endorsement:
                s.append("Farmer has elected for crop insurance with hail endorsement")
            else:
                s.append("Farmer has elected for crop insurance WITHOUT hail endorsement")
            s.append(f"The farmers estimated yield is: {self.get_yield_estimate()} bushels/acre, and yield guarantee is: {self.get_yield_guarantee()} bushels/acre")
            s.append(f"The farmers per/acre premium is: ${self.get_total_premium_per_acre()} and total premium is: ${self.get_total_premium()}")
            return s
        else:
            s = f"Insurance information for {self.insured_acres} acres of {self.crop} at {self.coverage}% coverage:\n"
            s += f"Farm Location: mer {self.farm.meridian}, twn {self.farm.township}, rng {self.farm.range}, RA {self.farm.risk_area}\n"
            
            if self.include_hail_endorsement:
                s += "Farmer has elected for crop insurance with hail endorsement\n"
            else:
                s += "Farmer has elected for crop insurance WITHOUT hail endorsement\n"
            s += f"The farmers estimated yield is: {self.get_yield_estimate()} bushels/acre, and yield guarantee is: {self.get_yield_guarantee()} bushels/acre\n"
            s += f"The farmers per/acre premium is: ${self.get_total_premium_per_acre()} and total premium is: ${self.get_total_premium()}\n"
            return s

    def is_premium_pay_date(self, adate) -> bool:
        """
        Assume the premium is paid at the end of month. Determine adate is the premium_pay_date

        :return bool: is need to pay premium
        """
        is_pay_premium = is_end_of_month(adate=adate)
        return is_pay_premium

    #calculates the number of crops being insured
    @classmethod
    def num_of_crops(cls):
        return cls.number_of_crops
