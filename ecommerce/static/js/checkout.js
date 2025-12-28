document.addEventListener('DOMContentLoaded', () => {
  const hideableShipping = document.querySelector('.hideable_shipping_form');
  const hideableBilling = document.querySelector('.hideable_billing_form');
  const hideableWholeBilling = document.querySelector('.hideable_whole_billing_form');

  const useDefaultShipping = document.querySelector('input[name="use_default_shipping"]');
  const useDefaultBilling = document.querySelector('input[name="use_default_billing"]');
  const sameBilling = document.querySelector('input[name="same_billing_address"]');

  const toggle = (checkbox, element) => {
    if (!checkbox || !element) {
        return;
    }

    element.style.display = checkbox.checked ? 'none' : '';
    checkbox.addEventListener('change', () => {
      element.style.display = checkbox.checked ? 'none' : '';
    });
  };

  toggle(useDefaultShipping, hideableShipping);
  toggle(useDefaultBilling, hideableBilling);
  toggle(sameBilling, hideableWholeBilling);
});
