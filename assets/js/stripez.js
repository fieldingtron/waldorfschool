//import uuid from 'uuid/v4';


const amount = 1000;
const $messageBox = document.getElementById('messageBox');
const $button = document.getElementById('buttonz');

function resetButtonText() {
  $button.innerHTML = 'Click to Buy! <strong>$10</strong>';
}

function create_UUID(){
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });
    return uuid;
}

const handler = StripeCheckout.configure({
  key: "pk_test_hmuxAR4Gp8zFUrhZbbou8wPx",
  image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
  locale: 'auto',
  closed: function () {
    resetButtonText();
  },
  token: function(token) {

    fetch("https://mysticretreats.netlify.com/.netlify/functions/stripe-charge/stripe-charge", {
      method: 'POST',
      body: JSON.stringify({
        token,
        amount,
        idempotency_key: create_UUID()
      }),
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    })
    .then(res => res.json())
    .catch(error => console.error(error))
    .then(response => {

      resetButtonText();

      let message = typeof response === 'object' && response.status === 'succeeded'
        ? 'Charge was successful!'
        : 'Charge failed.'
      $messageBox.querySelector('h2').innerHTML = message;

      console.log(response);
    });
  }
});

$button.addEventListener('click', () => {

  setTimeout(() => {
    $button.innerHTML = 'Waiting for response...';
  }, 500);

  handler.open({
    amount,
    name: 'Test Shop',
    description: 'A Fantastic New Widget'
  });
});