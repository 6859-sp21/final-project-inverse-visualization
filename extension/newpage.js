
let sharedData;
let imageDerender = {}
try {
    sharedData = JSON.parse(localStorage.sharedData);
    document.getElementById("image").src = sharedData.info.srcUrl;

    fetch(sharedData.info.srcUrl)
        .then(r => r.blob())
        .then((blob) => console.log(blob));

}
catch (e) { }

derenderImage = () => {
    fetch('http://localhost:5000/derender',
        {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'image': sharedData.info.srcUrl }),
        })
        .then(response => response.json())
        .then(data => {

            for (let i = 0; i < data.stats.length; i++) {
                stat = data.stats[i]
                imageDerender[stat.text] = stat.text
                addTooltip(stat.text, stat.x, stat.y)
            }
        });
}

submitChanges = () => {
    fetch('http://localhost:5000/changes',
        {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'changes': imageDerender }),
        })
        .then(response => response.json())
        .then(data => {

        });
}

addTooltip = (text, x, y) => {
    var imageContainer = document.getElementById("image-container");

    var input = document.createElement("input");
    input.type = "text";
    input.value = text;
    input.id = 'text-tooltip';
    input.style.width = '30px';
    input.style.height = '10px';
    input.style.left = `${x}px`;
    input.style.top = `${y}px`;

    input.addEventListener('input', (e) => {
        console.log(text, '=>', e.target.value);
        imageDerender[text] = e.target.value
        console.log(imageDerender)

    });

    imageContainer.appendChild(input);
}

document.addEventListener('DOMContentLoaded', function () {
    var button = document.getElementById('submit');
    var initial = true;
    button.addEventListener('click', function () {

        if (initial) {
            derenderImage();
            button.innerHTML = 'Submit!'
            initial = false
        }
        else {
            submitChanges()
        }
    });
});

