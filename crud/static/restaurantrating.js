function displayRating(rating) {
    const stars = '★'.repeat(Math.floor(rating)) + '☆'.repeat(5 - Math.floor(rating));
    return `<span class="rating">${stars} (${rating.toFixed(1)})</span>`;
}
