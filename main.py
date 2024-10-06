from datetime import timedelta

from expense_tracker import (
    PaymentTracker,
    UpdatableCurrencyConverter,
    ExpenseSummary,
    Currency,
    ExpensePlotter,
)

try:
    from my_payments import MY_PAYMENTS
except ImportError:
    from example_payments import MY_PAYMENTS


if __name__ == "__main__":
    tracker = PaymentTracker()
    currency_converter = UpdatableCurrencyConverter()
    summary = ExpenseSummary(tracker, currency_converter)
    plotter = ExpensePlotter()

    tracker.add_payments(MY_PAYMENTS)

    period = timedelta(days=365)
    currency = Currency.RUB

    sorted_charges = sorted(
        summary.charges(period, currency),
        key=lambda x: x.money_value.amount,
        reverse=True,
    )
    for charge in sorted_charges:
        print(charge)
    print(summary.total(period, currency))
    plotter.pie(sorted_charges, period)
    plotter.interractive_barplot(sorted_charges, currency, period)
