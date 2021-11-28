class Challenge2:

    def calculation_month(self, loan_term):
        month_number = int(loan_term * 12)
        return month_number

    def mortgage_calculation(self, home_price, down_payment, months, interest_rate):
        #  = M ( r(1 + r)^n ) / ( (1 + r)^n – 1 )
        m = home_price - (home_price * (down_payment / 100))
        r = (interest_rate/100) / 12
        n = months
        internal_acumulation = 1 + r
        internal_power = pow(internal_acumulation, n)
        c = m * ((r * internal_power) / (internal_power - 1))
        fee_to_cancel = c

        return float(fee_to_cancel)
