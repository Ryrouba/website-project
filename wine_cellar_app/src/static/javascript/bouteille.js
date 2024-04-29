var bottles = {{ bottles | tojson }};
var currentBottleIndex = 0;

function showNextBottle() {
    if (currentBottleIndex < bottles.length) {
        var currentBottle = bottles[currentBottleIndex];
        displayBottle(currentBottle);
        currentBottleIndex++;
    } else {
        alert("Vous avez atteint la dernière bouteille.");
    }
}

function showPreviousBottle() {
    if (currentBottleIndex > 0) {
        currentBottleIndex--;
        var currentBottle = bottles[currentBottleIndex];
        displayBottle(currentBottle);
    } else {
        alert("Vous êtes déjà à la première bouteille.");
    }
}

function displayBottle(bottle) {
    var bottleHtml = `
        <div class="bottle-container">
            <h2>${bottle[3]}</h2> <!-- Nom de la bouteille -->
            <p><strong>Vignoble :</strong> ${bottle[2]}</p> <!-- Nom du vignoble -->
            <p><strong>Type :</strong> ${bottle[4]}</p> <!-- Type de vin -->
            <p><strong>Année :</strong> ${bottle[5]}</p> <!-- Année -->
            <p><strong>Région :</strong> ${bottle[6]}</p> <!-- Région -->
            <p><strong>Commentaires :</strong> ${bottle[7]}</p> <!-- Commentaires -->
            <p><strong>Note personnelle :</strong> ${bottle[8]}</p> <!-- Note personnelle -->
            <p><strong>Note communautaire :</strong> ${bottle[9]}</p> <!-- Note communautaire -->
            <p><strong>Prix :</strong> ${bottle[11]}</p> <!-- Prix -->
            <img src="${bottle[10]}" alt="Image de la bouteille" class="bottle-image">
        </div>
    `;
    document.getElementById("bottleDisplay").innerHTML = bottleHtml;
}

// Afficher la première bouteille au chargement de la page
if (bottles.length > 0) {
    displayBottle(bottles[0]);
    currentBottleIndex = 1;
}
