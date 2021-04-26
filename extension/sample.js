function deRender(info, tab) {
	console.log(info)
	localStorage.sharedData = JSON.stringify({info: info});
	chrome.tabs.create({
		url: 'chrome://newtab'
	});
}

(function() {
	var id = chrome.contextMenus.create({
		title: 'Derender this image!',
		contexts: ['image'],
		onclick: deRender
	});
})();
