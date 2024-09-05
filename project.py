from pyfiglet import Figlet
from numpy import log

figlet = Figlet()
figlet.setFont(font = 'banner')


# Default variables
_inf: float = 0.03             # inflation rate
_r: float = 0.08               # investment rate of return





### Guardar valores em dictionary!
_name: str = ""              # person's name
_age: int = 0                # current age
_retirement_age: int = 0     # age at which wishes to retire
_working_years: int = 0      # no. years that's still going to work 
_retirement_cf: float = 0      # annual cf adjust today's value for inflation 3% annually
_retirement_time: float = 0    # total time spent in retirement
_current_savings: float = 0    # Current savings
_req_capital: float = 0        # Starting capital needed at the beggining of retirement.
_req_lumpsum: float = 0        # Required amount to invest today to reach target
_req_annual_cf: float = 0      # Required annual investment to reach target
_req_annual_cf_w_savings: float = 0        # Including savings required annual investment to reach target


def main():
    print("\n")
    print(figlet.renderText("Welcome!"))
    menu()
    

##################################################################################
##                               MENU FUNCTIONS                                 ##
##################################################################################


############################# Auto report
def collect_data() -> None:
    '''
    A function to collect basic user data in order to do calculations later.
    '''
    print("We need some data before we initialize.".upper())
    global _name, _age, _retirement_age, _working_years, _retirement_cf, _retirement_time, _current_savings
    _name = input("\nWhat's your name? ").strip().capitalize()
    print(f"Hello {_name}. Let's start!")
    _age = int(input("What's your age? ").strip())
    _retirement_age = int(input("What's your desired retirement age? ").strip())     # age at which wishes to retire
    _retirement_time = (float(input("What's your life expectancy? ").strip())) - _retirement_age
    _working_years = (_retirement_age - _age)   # no. years that's still going to work 
    _retirement_cf = float(input("When retired, what's your desired monthly cashflow? ").strip())
    _current_savings = float(input("What's your current savings? ").strip())
    print("\n\n--------------------collected info--------------------".upper())
    print("Age:", _age)
    print("Retirement age:", _retirement_age)
    print(f"Life expectancy: {_retirement_time + _retirement_age}")
    print(f"Monthly retirement withdrawals: {_retirement_cf}")
    print("Current Savings:", _current_savings)
    ask: str = input("\nIs all this info correct? (y/n) ").strip()
    if ask == "y":
        pass
    elif ask == "n":
        collect_data() # redo collection of data
    else:
        print("Invalid option. Please try again.")


def auto_report() -> None:
    '''
    Function that will do all calculation for you.
    '''
    global _req_capital, _req_lumpsum, _req_annual_cf, _req_annual_cf_w_savings
    cf = (_retirement_cf * 12)
    r = (1+_r)/(1+_inf)-1
    n = _retirement_time
    m = 1
    # Required capital at the start of retirement
    _req_capital = cf*(1-1/(1+r)**n)/r
    
    # Required amount to invest today to reach target
    fv: float = _req_capital
    n: int = _working_years
    _req_lumpsum = fv*(1+r/m)**(-n*m)

    # Required annual investment to reach target
    _req_annual_cf = fv/(((1+r)**n-1)/r)

    # Including savings required annual investment to reach target
    svgs = _current_savings
    svgs_fv = svgs*(1+r)**n     # Calculate Future value of current savings
    rmng_fv = (fv - svgs_fv)    # subtract future value of savings from required capital at retirement beggining
    _req_annual_cf_w_savings = rmng_fv/(((1+r)**n-1)/r)


def generate_report() -> str:
    '''
    A function that diggests all the calculations into a simple way of understanding.
    '''
    report = ""
    report += "\n\n--------------------auto report--------------------\n".upper()
    report += f"Hello again {_name} this is your retirement planning report.\n"
    report += f"\nassumptions\n".upper()
    report += f"Analysed inflation rate: {_inf}\n"
    report += f"Real rate of investment return {(1+_r)/(1+_inf)-1:.3f}"
    report += "\n\n"
    report += f"At {_age} you have {_current_savings} in savings.\n"
    report += f"You expect to retire at age {_retirement_age}, {_working_years} years from now.\n"
    report += f"In order for you to withdraw monthly {_retirement_cf} in your retirement, you need {_req_capital:.2f} at the beginning of your retirement.\n"
    report += "To reach that target you have 3 options:\n\n"
    report += f"1-) Invest today {_req_lumpsum:.2f} at {_r} nominal rate of return, and let compound interest do the heavy lifting.\n"
    report += f"2-) Invest annually {_req_annual_cf:.2f} at {_r} nominal rate of return.\n"
    report += f"3-) Or invest today your current savings ({_current_savings}) and Invest annually ({_req_annual_cf_w_savings}) at {_r} nominal rate of return.\n"
    report += "\nComparison of the 3".upper()
    report += "\n"
    report += f"Option 1-) total investment is {_req_lumpsum:.2f}, you only invest one time, today.\n"
    report += f"Option 2-) total investment is {(_req_annual_cf*_working_years):.2f}, you invest annually {_working_years} times.\n"
    report += f"Option 3-) total investment is {((_req_annual_cf_w_savings*_working_years)+_current_savings):.2f}, you invest your savings today and invest annually {_working_years} times.\n"
    
    return report


############################# Manual calculations
def required_capital() -> float:
    '''
    Starting capital needed at the beggining of retirement.
    Get the present value of a series of future cashflows.

    cf = annual cashflows
    r = investment real rate of return
    n = number of years in retirement
    return Present Value of cashflows
    '''
    cf = float(input("How much cashflow you need per month in your retirement? ")) * 12
    r = (1+_r)/(1+_inf)-1
    n = float(input("How many years you expect to be retired? "))
    return cf*(1-1/(1+r)**n)/r

def required_return() -> float:
    '''
    Required return on your money to reach future value target
    Get the geometric return.

    pv = present value (current savings)
    fv = future value (monetary target)
    n = number of periods to go from pv to fv
    return geometric return
    '''
    pv = float(input("How much do you have right now? ").strip())
    fv = float(input("What's your monetary target? ").strip())
    n = float(input("How many years of investment? ").strip())
    return (fv/pv)**(1/n) -1

def required_years() -> float:
    '''
    Required years to reach a specific monetary goal.

    pv = present value
    fv = future value
    r = investment real rate of return
    return number of periods to get from pv to fv
    '''
    pv = float(input("How much do you have right now? ").strip())
    fv = float(input("What's your monetary target? ").strip())
    r = (1+_r)/(1+_inf)-1
    return (log(fv/pv)/log(1+r))

def required_annual_cf() -> float:
    '''
    Get the required annual cashflows to reach fv.

    fv = future value
    r = investment real rate of return
    n = number of periods
    svgs = current savings
    return Future Value with cash flows
    '''
    fv = float(input("What's your monetary target? ").strip())
    r = (1+_r)/(1+_inf)-1
    n = float(input("How many years of investment? ").strip())
    svgs = float(input("What's your current savings? ").strip())
    return (fv-svgs*(1+r)**n)/(((1+r)**n-1)/r)

def required_lumpsum(m=1) -> float:
    '''
    Get the present value of a future cashflow.

    fv = future value
    r = investment real rate of return
    n = number of periods
    m = annual capitalizations, default = 1
    return Present Value
    '''
    fv = float(input("What's your monetary target? ").strip())
    r = (1+_r)/(1+_inf)-1
    n = float(input("How many years of investment? ").strip())
    return fv*(1+r/m)**(-n*m)


############################# System
def change_defaults() -> None:
    print("\n\n--------------------default values--------------------".upper())
    print("Default inflation rate 0.03")
    print("Default investment rate of return 0.08")
    change = input("\nDo you wish do change any values? (y/n) ").strip()
    if change == "y":
        # store new data in the variables
        global _inf, _r
        _inf = float(input("What's your inflation rate? ").strip())
        _r = float(input("What's your investment rate of return? ").strip())
        print("\n\n-------------------- new default values--------------------".upper())
        print(f"Default inflation rate: {_inf}. ")
        print(f"Default investment rate of return: {_r}. ")
    elif change == "n":
        pass
    else:
        print("Invalid option. Please try again.")


def save_report(string) -> None:
    with open(f"{_name}_retirement_planning.txt", "w") as txt_file:
        txt_file.write(string)


def menu() -> None:
    # Infinit cycle
    while True: 
        print("\nWelcome!")
        print("'1.' Full Report.")
        print("'2.' Calculate required return from x to y in z years.")
        print("'3.' Calculate required time z for x compounds until y.")
        print("'4.' Calculate investment today to monetary target in z years.")
        print("'5'. Calculate annual investments to monetary target in z years.")
        print("'6'. Calculate required capital at the beggining of your retirement.")
        print("'7'. Reset data.")
        print("'8'. Change defaults.")
        print("'9.' Close program.")

        option = input("\nIntroduce the option to execute: ")
        if option == "1":
            collect_data()
            auto_report()
            print(generate_report())
            save = input("Do you want to save report as txt file? (y/n) ")
            if save == 'y':
                save_report(generate_report())
            else:
                pass
        elif option == "2":
            print(f"The required real rate of return is: {required_return():.2f}.")
        elif option == "3":
            print(f"The necessary number of years is: {required_years():.2f}.")
        elif option == "4":
            print(f"The necessary immediate investment value is: {required_lumpsum():.2f}.")
        elif option == "5":
            print(f"The annual investment value that you have to make is: {required_annual_cf():.2f}.")
        elif option == "6":
            print(f"The required capital at the beggining of your retirement is: {required_capital():.2f}.")
        elif option == "7":
            collect_data()
        elif option == "8":
            change_defaults()
        elif option == "9":
            print("\nThank you! Program closed.\n")
            break # quebrar o ciclo do loop
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()