def inputValidation(val, minVal, maxVal):
    # Validates that the input value is within the specified range [minVal, maxVal]
    try:
        if float(minVal) <= float(val) <= float(maxVal):
            return val
        else:
            print("Invalid input! Please enter a correct input!")
            return None
    except ValueError:
        # If the input is not a number, print an error message
        print("Invalid input! Please enter a correct input!")
        return None

def getInput(validProvinces):
    # Get and validate user inputs for various fields
    
    # Validate user name
    name = None
    while name is None or name.strip() == "":
        name = input("Enter your name: ").strip()
        if name == "":
            print("Invalid input! Name cannot be empty.")
            name = None

    # Validate province of residence
    province = None
    while province not in validProvinces:
        province = input(f"Enter your province of residence (one of {validProvinces}): ").strip()
        if province not in validProvinces:
            print("Invalid input! Please enter a correct province.")

    # Validate employment income
    employmentIncome = None
    while employmentIncome is None:
        employmentIncome = inputValidation(input("Enter your total income (enter 0 for none or positive number): "), 0, float('inf'))

    # Validate self-employment income
    selfEmploymentIncome = None
    while selfEmploymentIncome is None:
        selfEmploymentIncome = inputValidation(input("Enter your self-employment income (enter 0 for none or positive number): "), 0, float('inf'))

    # Validate other income
    otherIncome = None
    while otherIncome is None:
        otherIncome = inputValidation(input("Enter your other income (including EI) (enter 0 for none or positive number): "), 0, float('inf'))

    # Validate RRSP contribution
    rrspContribution = None
    while rrspContribution is None:
        rrspContribution = inputValidation(input("Enter your RRSP contribution (enter 0 for none or positive number): "), 0, float('inf'))

    # Validate capital gains and losses
    capitalGainsLosses = None
    while capitalGainsLosses is None:
        print("Note: Only capital gains are calculated, as losses require access to previous year's return.")
        capitalGainsLosses = inputValidation(input("Enter your capital gains and losses (enter 0 for none or positive number for capital gains): "), 0, float('inf'))

    # Validate eligible dividends
    eligibleDividends = None
    while eligibleDividends is None:
        eligibleDividends = inputValidation(input("Enter your eligible dividends (enter 0 for none or positive number): "), 0, float('inf'))
        
    # Validate non-eligible dividends
    nonEligibleDividends = None
    while nonEligibleDividends is None:
        nonEligibleDividends = inputValidation(input("Enter your non-eligible dividends (enter 0 for none or positive number): "), 0, float('inf'))

    # Validate income tax paid
    incomeTaxPaid = None
    while incomeTaxPaid is None:
        incomeTaxPaid = inputValidation(input("Enter your income tax paid (enter 0 for none or positive number): "), 0, float('inf'))

    # Return all validated inputs as a dictionary
    return {
        "name": name,
        "province": province,
        "employmentIncome": float(employmentIncome),
        "selfEmploymentIncome": float(selfEmploymentIncome),
        "otherIncome": float(otherIncome),
        "rrspContribution": float(rrspContribution),
        "capitalGainsLosses": float(capitalGainsLosses),
        "eligibleDividends": float(eligibleDividends),
        "nonEligibleDividends": float(nonEligibleDividends),
        "incomeTaxPaid": float(incomeTaxPaid)
    }


class TaxCalculator:
    def __init__(self, userInput):
        # Initialize the TaxCalculator with user input and calculate taxable income considering 2024 tax brackets and formulas
        self.userInput = userInput
        self.taxableIncome = self.userInput['employmentIncome'] + self.userInput['selfEmploymentIncome'] + self.userInput['otherIncome']
        
        # Calculate taxable capital gain (only positive gains are considered)
        capitalGain = max(0, self.userInput['capitalGainsLosses'])
        taxableCapitalGain = capitalGain * 0.50
        self.taxableIncome += taxableCapitalGain
    
    def federalTax(self):
        # Calculate federal tax based on taxable income and 2024 federal tax brackets
        if self.taxableIncome <= 55867:
            tax = self.taxableIncome * 0.15
        elif self.taxableIncome <= 111733:
            tax = 55867 * 0.15 + (self.taxableIncome - 55867) * 0.205
        elif self.taxableIncome <= 173205:
            tax = 55867 * 0.15 + (111733 - 55867) * 0.205 + (self.taxableIncome - 111733) * 0.26
        elif self.taxableIncome <= 246752:
            tax = 55867 * 0.15 + (111733 - 55867) * 0.205 + (173205 - 111733) * 0.26 + (self.taxableIncome - 173205) * 0.29
        else:
            tax = 55867 * 0.15 + (111733 - 55867) * 0.205 + (173205 - 111733) * 0.26 + (246752 - 173205) * 0.29 + (self.taxableIncome - 246752) * 0.33
        return tax
    
    def ontarioTax(self):
        # Calculate Ontario provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 51446:
            tax = self.taxableIncome * 0.0505
        elif self.taxableIncome <= 102894:
            tax = 51446 * 0.0505 + (self.taxableIncome - 51446) * 0.0915
        elif self.taxableIncome <= 150000:
            tax = 51446 * 0.0505 + (102894 - 51446) * 0.0915 + (self.taxableIncome - 102894) * 0.1116
        elif self.taxableIncome <= 220000:
            tax = 51446 * 0.0505 + (102894 - 51446) * 0.0915 + (150000 - 102894) * 0.1116 + (self.taxableIncome - 150000) * 0.1216
        else:
            tax = 51446 * 0.0505 + (102894 - 51446) * 0.0915 + (150000 - 102894) * 0.1116 + (220000 - 150000) * 0.1216 + (self.taxableIncome - 220000) * 0.1316
        return tax
    
    def quebecTax(self):
        # Calculate Quebec provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 51780:
            tax = self.taxableIncome * 0.14
        elif self.taxableIncome <= 103545:
            tax = 51780 * 0.14 + (self.taxableIncome - 51780) * 0.19
        elif self.taxableIncome <= 126000:
            tax = 51780 * 0.14 + (103545 - 51780) * 0.19 + (self.taxableIncome - 103545) * 0.24
        else:
            tax = 51780 * 0.14 + (103545 - 51780) * 0.19 + (126000 - 103545) * 0.24 + (self.taxableIncome - 126000) * 0.2575
        return tax
    
    def newfoundlandTax(self):
        # Calculate Newfoundland and Labrador provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 43198:
            tax = self.taxableIncome * 0.087
        elif self.taxableIncome <= 86135:
            tax = 43198 * 0.087 + (self.taxableIncome - 43198) * 0.145
        elif self.taxableIncome <= 154244:
            tax = 43198 * 0.087 + (86135 - 43198) * 0.145 + (self.taxableIncome - 86135) * 0.158
        elif self.taxableIncome <= 215343:
            tax = 43198 * 0.087 + (86135 - 43198) * 0.145 + (154244 - 86135) * 0.158 + (self.taxableIncome - 154244) * 0.173
        elif self.taxableIncome <= 269750:
            tax = 43198 * 0.087 + (86135 - 43198) * 0.145 + (154244 - 86135) * 0.158 + (215343 - 154244) * 0.173 + (self.taxableIncome - 215343) * 0.183
        elif self.taxableIncome <= 314928:
            tax = 43198 * 0.087 + (86135 - 43198) * 0.145 + (154244 - 86135) * 0.158 + (215343 - 154244) * 0.173 + (269750 - 215343) * 0.183 + (self.taxableIncome - 269750) * 0.203
        else:
            tax = 43198 * 0.087 + (86135 - 43198) * 0.145 + (154244 - 86135) * 0.158 + (215343 - 154244) * 0.173 + (269750 - 215343) * 0.183 + (314928 - 269750) * 0.203 + (self.taxableIncome - 314928) * 0.213
        return tax
    
    def peiTax(self):
        # Calculate Prince Edward Island provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 32656:
            tax = self.taxableIncome * 0.0995
        elif self.taxableIncome <= 64313:
            tax = 32656 * 0.0995 + (self.taxableIncome - 32656) * 0.138
        elif self.taxableIncome <= 105000:
            tax = 32656 * 0.0995 + (64313 - 32656) * 0.138 + (self.taxableIncome - 64313) * 0.167
        elif self.taxableIncome <= 140000:
            tax = 32656 * 0.0995 + (64313 - 32656) * 0.138 + (105000 - 64313) * 0.167 + (self.taxableIncome - 105000) * 0.167
        else:
            tax = 32656 * 0.0995 + (64313 - 32656) * 0.138 + (105000 - 64313) * 0.167 + (140000 - 105000) * 0.167 + (self.taxableIncome - 140000) * 0.1875
        return tax
    
    def novaScotiaTax(self):
        # Calculate Nova Scotia provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 29590:
            tax = self.taxableIncome * 0.0879
        elif self.taxableIncome <= 59998:
            tax = 29590 * 0.0879 + (self.taxableIncome - 29590) * 0.1495
        elif self.taxableIncome <= 93000:
            tax = 29590 * 0.0879 + (59998 - 29590) * 0.1495 + (self.taxableIncome - 59998) * 0.175
        elif self.taxableIncome <= 150000:
            tax = 29590 * 0.0879 + (59998 - 29590) * 0.1495 + (93000 - 59998) * 0.175 + (self.taxableIncome - 93000) * 0.21
        else:
            tax = 29590 * 0.0879 + (59998 - 29590) * 0.1495 + (93000 - 59998) * 0.175 + (150000 - 93000) * 0.21 + (self.taxableIncome - 150000) * 0.21
        return tax
    
    def newBrunswickTax(self):
        # Calculate New Brunswick provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 49495:
            tax = self.taxableIncome * 0.094
        elif self.taxableIncome <= 102894:
            tax = 49495 * 0.094 + (self.taxableIncome - 49495) * 0.1475
        elif self.taxableIncome <= 150000:
            tax = 49495 * 0.094 + (102894 - 49495) * 0.1475 + (self.taxableIncome - 102894) * 0.16
        elif self.taxableIncome <= 185064:
            tax = 49495 * 0.094 + (102894 - 49495) * 0.1475 + (150000 - 102894) * 0.16 + (self.taxableIncome - 150000) * 0.195
        else:
            tax = 49495 * 0.094 + (102894 - 49495) * 0.1475 + (150000 - 102894) * 0.16 + (185064 - 150000) * 0.195 + (self.taxableIncome - 185064) * 0.195
        return tax

    def manitobaTax(self):
        # Calculate Manitoba provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 47000:
            tax = self.taxableIncome * 0.108
        elif self.taxableIncome <= 100000:
            tax = 47000 * 0.108 + (self.taxableIncome - 47000) * 0.1275
        else:
            tax = 47000 * 0.108 + (100000 - 47000) * 0.1275 + (self.taxableIncome - 100000) * 0.174
        return tax
    
    def saskatchewanTax(self):
        # Calculate Saskatchewan provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 55205:
            tax = self.taxableIncome * 0.105
        elif self.taxableIncome <= 127430:
            tax = 55205 * 0.105 + (self.taxableIncome - 55205) * 0.125
        else:
            tax = 55205 * 0.105 + (127430 - 55205) * 0.125 + (self.taxableIncome - 127430) * 0.145
        return tax
    
    def albertaTax(self):
        # Calculate Alberta provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 148269:
            tax = self.taxableIncome * 0.1
        elif self.taxableIncome <= 177922:
            tax = 148269 * 0.1 + (self.taxableIncome - 148269) * 0.12
        elif self.taxableIncome <= 227230:
            tax = 148269 * 0.1 + (177922 - 148269) * 0.12 + (self.taxableIncome - 177922) * 0.13
        elif self.taxableIncome <= 355845:
            tax = 148269 * 0.1 + (177922 - 148269) * 0.12 + (227230 - 177922) * 0.13 + (self.taxableIncome - 227230) * 0.14
        else:
            tax = 148269 * 0.1 + (177922 - 148269) * 0.12 + (227230 - 177922) * 0.13 + (355845 - 227230) * 0.14 + (self.taxableIncome - 355845) * 0.15
        return tax
    
    def bcTax(self):
        # Calculate British Columbia provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 47737:
            tax = self.taxableIncome * 0.0506
        elif self.taxableIncome <= 95474:
            tax = 47737 * 0.0506 + (self.taxableIncome - 47737) * 0.077
        elif self.taxableIncome <= 116344:
            tax = 47737 * 0.0506 + (95474 - 47737) * 0.077 + (self.taxableIncome - 95474) * 0.105
        elif self.taxableIncome <= 157748:
            tax = 47737 * 0.0506 + (95474 - 47737) * 0.077 + (116344 - 95474) * 0.105 + (self.taxableIncome - 116344) * 0.1229
        elif self.taxableIncome <= 222420:
            tax = 47737 * 0.0506 + (95474 - 47737) * 0.077 + (116344 - 95474) * 0.105 + (157748 - 116344) * 0.1229 + (self.taxableIncome - 157748) * 0.147
        elif self.taxableIncome <= 253812:
            tax = 47737 * 0.0506 + (95474 - 47737) * 0.077 + (116344 - 95474) * 0.105 + (157748 - 116344) * 0.1229 + (222420 - 157748) * 0.147 + (self.taxableIncome - 222420) * 0.168
        else:
            tax = 47737 * 0.0506 + (95474 - 47737) * 0.077 + (116344 - 95474) * 0.105 + (157748 - 116344) * 0.1229 + (222420 - 157748) * 0.147 + (253812 - 222420) * 0.168 + (self.taxableIncome - 253812) * 0.205
        return tax
        
    def yukonTax(self):
        # Calculate Yukon provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 55867:
            tax = self.taxableIncome * 0.064
        elif self.taxableIncome <= 111733:
            tax = 55867 * 0.064 + (self.taxableIncome - 55867) * 0.09
        elif self.taxableIncome <= 173205:
            tax = 55867 * 0.064 + (111733 - 55867) * 0.09 + (self.taxableIncome - 111733) * 0.109
        elif self.taxableIncome <= 500000:
            tax = 55867 * 0.064 + (111733 - 55867) * 0.09 + (173205 - 111733) * 0.109 + (self.taxableIncome - 173205) * 0.128
        else:
            tax = 55867 * 0.064 + (111733 - 55867) * 0.09 + (173205 - 111733) * 0.109 + (500000 - 173205) * 0.128 + (self.taxableIncome - 500000) * 0.15
        return tax
        
    def northwestTerritoriesTax(self):
        # Calculate Northwest Territories provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 50597:
            tax = self.taxableIncome * 0.059
        elif self.taxableIncome <= 101195:
            tax = 50597 * 0.059 + (self.taxableIncome - 50597) * 0.086
        elif self.taxableIncome <= 164625:
            tax = 50597 * 0.059 + (101195 - 50597) * 0.086 + (self.taxableIncome - 101195) * 0.122
        else:
            tax = 50597 * 0.059 + (101195 - 50597) * 0.086 + (164625 - 101195) * 0.122 + (self.taxableIncome - 164625) * 0.1405
        return tax

    def nunavutTax(self):
        # Calculate Nunavut provincial tax based on taxable income and 2024 provincial tax brackets
        if self.taxableIncome <= 53268:
            tax = self.taxableIncome * 0.04
        elif self.taxableIncome <= 106537:
            tax = 53268 * 0.04 + (self.taxableIncome - 53268) * 0.07
        elif self.taxableIncome <= 173205:
            tax = 53268 * 0.04 + (106537 - 53268) * 0.07 + (self.taxableIncome - 106537) * 0.09
        else:
            tax = 53268 * 0.04 + (106537 - 53268) * 0.07 + (173205 - 106537) * 0.09 + (self.taxableIncome - 173205) * 0.115
        return tax

    def calculateCPPCredits(self):
        # Calculate CPP contribution and tax credit based on taxable income
        cppContributionRate = 0.0595
        cppMaxContribution = 3867.50
        cppOnIncome = max(self.taxableIncome - 3500, 68500)
        cppContribution = min(cppOnIncome * cppContributionRate, cppMaxContribution)
        cppTaxCredit = cppContribution * 0.15
        # 15% eligibility on CPP credits from total CPP contribution
        return cppContribution, cppTaxCredit
        
    def calculateEICredits(self):
        # Calculate EI contribution and tax credit based on taxable income
        eiContributionRate = 0.0166
        eiMaxContribution = 1049.12
        eiOnIncome = max(self.taxableIncome, 63200)
        eiContribution = min(eiOnIncome * eiContributionRate, eiMaxContribution)
        eiTaxCredit = eiContribution * 0.15
        # 15% eligibility on EI credits from total EI contribution
        return eiContribution, eiTaxCredit
        
    def calculateQuebecEICredits(self):
        # Calculate EI contribution and tax credit for Quebec based user on taxable income
        eiContributionRate = 0.0132
        eiMaxContribution = 834.24
        eiOnIncome = max(self.taxableIncome, 63200)
        eiContribution = min(eiOnIncome * eiContributionRate, eiMaxContribution)
        eiQuebecTaxCredit = eiContribution * 0.15
        # 15% eligibility on quebec EI credits from total EI contribution
        return eiContribution, eiQuebecTaxCredit
    
    def calculateRRSPCredits(self):
        # Calculate RRSP credits and apply penalties for over-contribution based on taxable income
        rrspContribution = self.userInput['rrspContribution']
        annualLimit = 31560
        overContributionLimit = 2000
        penaltyRate = 0.01
    
        if self.taxableIncome <= 51446:
            rrspCreditRate = 0.2005
        elif self.taxableIncome <= 55867:
            rrspCreditRate = 0.2415
        elif self.taxableIncome <= 90599:
            rrspCreditRate = 0.2965
        elif self.taxableIncome <= 102894:
            rrspCreditRate = 0.3148
        elif self.taxableIncome <= 106732:
            rrspCreditRate = 0.3389
        elif self.taxableIncome <= 111733:
            rrspCreditRate = 0.3719
        elif self.taxableIncome <= 150000:
            rrspCreditRate = 0.4341
        elif self.taxableIncome <= 173205:
            rrspCreditRate = 0.4497
        elif self.taxableIncome <= 220000:
            rrspCreditRate = 0.4829
        elif self.taxableIncome <= 246752:
            rrspCreditRate = 0.4985
        else:
            rrspCreditRate = 0.5353
    
        rrspCredit = rrspContribution * rrspCreditRate
    
        if rrspContribution > annualLimit:
            excessContribution = rrspContribution - annualLimit
            if excessContribution > overContributionLimit:
                penalty = (excessContribution - overContributionLimit) * penaltyRate * 12
            else:
                penalty = 0
        else:
            penalty = 0
    
        rrspCredit -= penalty
        return rrspCredit
    
    def elgAndNonElgDividendsCredits(self):
        # Calculate tax credits for eligible and non-eligible dividends based on taxable income
        eligiblaDiv = self.userInput['eligibleDividends']
        nonEligiblaDiv = self.userInput['nonEligibleDividends']
        creditEligibleDiv = (eligiblaDiv * 1.38) * 0.150198
        # 38% eligibility on eligible dividend credits from contribution
        creditNonEligibleDiv = (nonEligiblaDiv * 1.15) * 0.090301
        # 15% eligibility on non eligible dividend credits from contribution
        return creditEligibleDiv + creditNonEligibleDiv
    
    def calculateTaxOwingOrRefund(self):
        provinceTaxMethods = {
            "ON": self.ontarioTax,
            "QC": self.quebecTax,
            "NB": self.newBrunswickTax,
            "MB": self.manitobaTax,
            "SK": self.saskatchewanTax,
            "AB": self.albertaTax,
            "BC": self.bcTax,
            "YT": self.yukonTax,
            "NT": self.northwestTerritoriesTax,
            "NU": self.nunavutTax
        }
        
        provincialTax = provinceTaxMethods[self.userInput['province']]()
        
        if self.userInput['province'] == 'QC':
            eiContribution, eiCredits = self.calculateQuebecEICredits()
        else:
            eiContribution, eiCredits = self.calculateEICredits()
        
        cppContribution, cppCredits = self.calculateCPPCredits()
        rrspCredits = self.calculateRRSPCredits()
        dividendCredits = self.elgAndNonElgDividendsCredits()
        
        federalTax = self.federalTax()
        totalTax = federalTax + provincialTax
        totalCredits = cppCredits + eiCredits + rrspCredits + dividendCredits
        taxOwingOrRefund = totalTax - totalCredits - self.userInput['incomeTaxPaid']
        
        return taxOwingOrRefund, provincialTax, federalTax, cppContribution, eiContribution


def main():
    # Print the title and description of the software
    title = """
******************************************************
*                                                    *
*            Tax Return Software 2024                *
*                                                    *
******************************************************
"""
    description = """Welcome to the Tax Return Software 2024!
This software will help you calculate your federal and provincial taxes,
CPP and EI contributions, and RRSP credits. It will also determine your
total tax owing or potential refund based on the latest tax brackets and formulas.
Please follow the prompts to enter your income and other relevant details.\n"""

    print(title)
    print(description)
    
    # Define the valid provinces for the user to choose from
    validProvinces = ["ON", "QC", "NB", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
    userInput = getInput(validProvinces)  # Get user input
    
    # Initialize the TaxCalculator with the user input
    taxCalculator = TaxCalculator(userInput)
    
    # Call the method to calculate the total tax owing or refund along with the provincial tax, federal tax,
    # CPP contribution, and EI contribution. This method encapsulates all the necessary tax calculations.
    taxOwingOrRefund, provincialTax, federalTax, cppContribution, eiContribution = taxCalculator.calculateTaxOwingOrRefund()

    # Print the summary of the tax calculation
    print("\n")
    print("********************************************************************************************************************")
    print(f"Name: {userInput['name']}")
    print(f"Province: {userInput['province']}")
    print(f"Total Income: ${taxCalculator.taxableIncome:.2f}")
    print(f"Provincial Tax: ${provincialTax:.2f}")
    print(f"Federal Tax: ${federalTax:.2f}")
    print(f"CPP Contribution: ${cppContribution:.2f}")
    print(f"EI Contribution: ${eiContribution:.2f}")
    print(f"Total Tax Owing or Refund: {'Owing' if taxOwingOrRefund > 0 else 'Refund'} ${abs(taxOwingOrRefund):.2f}")
    print("********************************************************************************************************************")

main()