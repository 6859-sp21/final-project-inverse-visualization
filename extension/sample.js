function search(info, tab) {
	chrome.tabs.create({
		url: 'http://www.google.com/search?q=' + encodeURIComponent(info.selectionText)
	});
}

(function() {
	var id = chrome.contextMenus.create({
		title: 'Search google for "%s"',
		contexts: ['selection'],
		onclick: search
	});
})();