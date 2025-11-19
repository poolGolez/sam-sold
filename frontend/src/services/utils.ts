export function formatCurrency(value: number, currency: string = "PHP", locale: string = "en-US") {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency
  }).format(value);
}