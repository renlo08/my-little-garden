// List all the cards in the garden list
const gardenCards = Array.from(document.getElementsByClassName('garden-card'))
// Add Event Listener to each card
gardenCards.forEach(gardenCard => {
    gardenCard.addEventListener('click', () => {
        renderGardenDetails(gardenCard);
    });
});

function renderGardenDetails(gardenCard) {
    // extract url from data-url attribute
    const url = gardenCard.dataset.url;
    // navigate to the url
    window.location.href = url;
}