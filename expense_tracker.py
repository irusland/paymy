import abc
from datetime import timedelta, datetime
from decimal import Decimal
from enum import Enum
from typing import Iterable

import humanize
from pydantic import BaseModel

from currency_converter import CurrencyConverter
import plotly.express as px
import matplotlib.pyplot as plt


class Currency(Enum):
    RUB = "₽"
    USD = "$"
    EUR = "€"
    TENGE = "₸"


class MoneyValue(BaseModel):
    amount: Decimal
    currency: Currency

    def __str__(self):
        return f"{self.currency.value}{float(self.amount):,.2f}"


class Charge(BaseModel):
    description: str
    money_value: MoneyValue

    def __str__(self):
        return f"{self.money_value} ({self.description})"


class Payment(Charge):
    recurring_every: timedelta | None = None


class Subscription(Payment):
    pass


class PaymentTracker:
    def __init__(self):
        self._payments = []

    def add_payments(self, payments: Iterable[Payment]):
        self._payments.extend(payments)

    def add_payment(self, payment: Payment):
        self._payments.append(payment)

    def get_payments(self) -> list[Payment]:
        return self._payments


class ICurrencyConverter(abc.ABC):
    @abc.abstractmethod
    def convert(
        self, amount: Decimal, from_currency: Currency, to_currency: Currency
    ) -> Decimal:
        pass

    def convert_money(self, money: MoneyValue, to_currency: Currency) -> MoneyValue:
        return MoneyValue(
            amount=self.convert(money.amount, money.currency, to_currency),
            currency=to_currency,
        )


class StaticCurrencyConverter(ICurrencyConverter):
    def __init__(self):
        usd_to_rub = Decimal("92")
        rub_to_usd = Decimal("1") / usd_to_rub
        eur_to_rub = Decimal("102")
        rub_to_eur = Decimal("1") / eur_to_rub

        self._rate = {
            (Currency.USD, Currency.RUB): usd_to_rub,
            (Currency.RUB, Currency.USD): rub_to_usd,
            (Currency.EUR, Currency.RUB): eur_to_rub,
            (Currency.RUB, Currency.EUR): rub_to_eur,
            (Currency.USD, Currency.EUR): usd_to_rub * rub_to_eur,
        }

    def convert(
        self, amount: Decimal, from_currency: Currency, to_currency: Currency
    ) -> Decimal:
        if from_currency == to_currency:
            return amount
        return amount * self._rate[(from_currency, to_currency)]


class UpdatableCurrencyConverter(ICurrencyConverter):
    def __init__(self):
        self._currency_converter = CurrencyConverter("eurofxref.csv")
        self._date = datetime(2024, 10, 4)

    def convert(
        self, amount: Decimal, from_currency: Currency, to_currency: Currency
    ) -> Decimal:
        return Decimal(
            self._currency_converter.convert(
                float(amount), from_currency.name, to_currency.name, date=self._date
            )
        )


class ExpenseSummary:
    def __init__(
        self, payment_tracker: PaymentTracker, currency_converter: ICurrencyConverter
    ):
        self.payment_tracker = payment_tracker
        self.currency_converter = currency_converter

    def total(self, period: timedelta, currency: Currency) -> MoneyValue:
        result = 0
        for payment in self.payment_tracker.get_payments():
            times = 1
            if payment.recurring_every:
                times = Decimal(period / payment.recurring_every)
            result += (
                self.currency_converter.convert(
                    payment.money_value.amount, payment.money_value.currency, currency
                )
                * times
            )
        return MoneyValue(amount=result, currency=currency)

    def charges(self, period: timedelta, currency: Currency) -> list[Charge]:
        result = []
        for payment in self.payment_tracker.get_payments():
            times = 1
            if payment.recurring_every:
                times = Decimal(period / payment.recurring_every)
            result.append(
                Charge(
                    description=payment.description,
                    money_value=MoneyValue(
                        amount=self.currency_converter.convert(
                            payment.money_value.amount,
                            payment.money_value.currency,
                            currency,
                        )
                        * times,
                        currency=currency,
                    ),
                )
            )
        return result


class ExpensePlotter:
    def pie(self, charges: list[Charge], period: timedelta):
        expenses = [float(charge.money_value.amount) for charge in charges]

        plt.pie(
            expenses, labels=list(map(str, charges)), autopct="%1.1f%%", startangle=140
        )

        plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(f"Expenses over {humanize.naturaldelta(period)}")
        plt.show()

    def interractive_barplot(
        self, charges: list[Charge], currency: Currency, period: timedelta
    ):
        labels = [charge.description for charge in charges]
        expenses = [charge.money_value.amount for charge in charges]

        fig = px.bar(
            x=labels,
            y=expenses,
            text=list(map(str, charges)),
            labels={"x": "Categories", "y": f"Charges ({currency.value})"},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            title=f"Charges over {humanize.naturaldelta(period)}",
            yaxis_tickprefix=currency.value,
        )
        fig.show()
