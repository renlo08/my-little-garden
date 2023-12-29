window.onload = function () {
    // Get all elements that have class 'garden-card'
    let cards = document.getElementsByClassName('garden-card');

    // Loop through the returned HTMLCollection
    for (let i = 0; i < cards.length; i++) {
        // Bind the click event to each card
        cards[i].addEventListener('click', function () {
            let id = this.id.split('-').pop(); // get the last part of the id, i.e., corresponding to the pk
            window.location.href = `/gardens/detail/${id}`;
        });
    }
};