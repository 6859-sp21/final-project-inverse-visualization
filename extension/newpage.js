let sharedData;
try {
    sharedData = JSON.parse(localStorage.sharedData);
    document.getElementById("image").src = sharedData.info.srcUrl;

    fetch(sharedData.info.srcUrl)
    .then(r => r.blob())
    .then((blob) => console.log(blob));

} 
catch (e) {}
delete localStorage.sharedData;
