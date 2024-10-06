from datetime import timedelta

from expense_tracker import Payment, MoneyValue, Currency


MY_PAYMENTS = (
    Payment(
        description="Коммунальные платежи",
        money_value=MoneyValue(amount=5000, currency=Currency.RUB),
        recurring_every=timedelta(days=30),
    ),
    Payment(
        description="Продукты",
        money_value=MoneyValue(amount=10000, currency=Currency.RUB),
        recurring_every=timedelta(days=7),
    ),
    Payment(
        description="Развлечения",
        money_value=MoneyValue(amount=2000, currency=Currency.RUB),
        recurring_every=timedelta(days=1),
    ),
    Payment(
        description="Кредит",
        money_value=MoneyValue(amount=3000, currency=Currency.RUB),
        recurring_every=None,
    ),
    Payment(
        description="Проезд",
        money_value=MoneyValue(amount=1500, currency=Currency.RUB),
        recurring_every=timedelta(days=1),
    ),
    Payment(
        description="Связь",
        money_value=MoneyValue(amount=500, currency=Currency.RUB),
        recurring_every=timedelta(days=30),
    ),
    Payment(
        description="Спортзал",
        money_value=MoneyValue(amount=3000, currency=Currency.RUB),
        recurring_every=timedelta(days=30),
    ),
)