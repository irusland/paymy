from datetime import timedelta

from expense_tracker import (
    PaymentTracker,
    UpdatableCurrencyConverter,
    ExpenseSummary,
    Currency,
)
from my_payments import MY_PAYMENTS


if __name__ == "__main__":
    tracker = PaymentTracker()
    currency_converter = UpdatableCurrencyConverter()
    summary = ExpenseSummary(tracker, currency_converter)

    tracker.add_payments(MY_PAYMENTS)

    period = timedelta(days=365)
    currency = Currency.USD
    for charge in sorted(
        summary.charges(period, currency),
        key=lambda x: x.money_value.amount,
        reverse=True,
    ):
        print(charge)

    print(summary.total(period, currency))
