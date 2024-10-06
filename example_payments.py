from datetime import timedelta

from expense_tracker import Payment, MoneyValue, Currency


MY_PAYMENTS = (
    Payment(
        description="Utility payments",
        money_value=MoneyValue(amount=10000, currency=Currency.RUB),
        recurring_every=timedelta(days=30),
    ),
    Payment(
        description="Groceries",
        money_value=MoneyValue(amount=7000, currency=Currency.RUB),
        recurring_every=timedelta(days=7),
    ),
    Payment(
        description="Entertainment",
        money_value=MoneyValue(amount=500, currency=Currency.RUB),
        recurring_every=timedelta(days=1),
    ),
    Payment(
        description="Debt",
        money_value=MoneyValue(amount=3000, currency=Currency.RUB),
        recurring_every=timedelta(days=30),
    ),
    Payment(
        description="Public transport",
        money_value=MoneyValue(amount=100, currency=Currency.RUB),
        recurring_every=timedelta(days=1),
    ),
    Payment(
        description="Сommunication",
        money_value=MoneyValue(amount=5000, currency=Currency.RUB),
        recurring_every=timedelta(days=30),
    ),
    Payment(
        description="Gym",
        money_value=MoneyValue(amount=3000, currency=Currency.RUB),
        recurring_every=timedelta(days=30),
    ),
)
