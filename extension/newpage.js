
let sharedData;
try {
    sharedData = JSON.parse(localStorage.sharedData);
    document.getElementById("image").src = sharedData.info.srcUrl;

    fetch(sharedData.info.srcUrl)
    .then(r => r.blob())
    .then((blob) => console.log(blob));

} 
catch (e) {}
derenderImage = () => {
    fetch('http://localhost:5000/derender')
        .then(response => response.json())
        .then(data => {
            
            for( let i = 0 ; i < data.stats.length ; i ++){
                stat = data.stats[i]
                addTooltip(stat.text, stat.x, stat.y)
            }
        });
}

addTooltip = (text, x, y) => {
    var imageContainer = document.getElementById("image-container");

    var div = document.createElement("div");
    div.id = 'text-tooltip';
    div.style.width = '30px'; 
    div.style.height = '30px';
    div.style.left = `${x}px`;
    div.style.top = `${y}px`; 
    console.log(div.style) 

    var node = document.createTextNode(text);
    div.appendChild(node);

    console.log(div)
    imageContainer.appendChild(div);
}

document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('submit');
    // onClick's logic below:
    button.addEventListener('click', function() {
        // call the api
        derenderImage();
        // display results

    });
});

