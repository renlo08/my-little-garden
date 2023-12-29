const redirectToURL = function () {
    // Get the URL from the data attribute and redirect
    let url = this.getAttribute('data-url');
    window.location.href = url;
};

const bindEventsToCards = function (cards) {
    // Loop through the returned HTMLCollection
    for (let i = 0; i < cards.length; i++) {
        // Bind the click event to each card
        cards[i].addEventListener('click', redirectToURL);
    }
};

window.onload = function () {
    // Get all elements that have class 'garden-card'
    let cards = document.getElementsByClassName('garden-card');
    bindEventsToCards(cards);
};