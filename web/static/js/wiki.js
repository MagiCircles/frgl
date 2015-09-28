
function linkRendererTitle(link, title) {
    return '<a href="http://fr.gl/wiki/' + link + '" class="internal-wiki-link">' + title + '</a>';
}

function linkRenderer(link) {
    linkRendererTitle(link, link);
}

$(document).ready(function() {
    var wikiPageName = $('#wiki-title').text();
    var wikiPageUrl = githubwiki.getGithubName(wikiPageName);

    githubwiki.setMarkedOptions({
	internalLink: linkRenderer,
	internalLinkTitle: linkRendererTitle
    });

    githubwiki.setWiki('SchoolIdolTomodachi', 'frgl');
    githubwiki.get(wikiPageUrl + '.md', function(data) {
	$('#wiki-content').html(data);
    });

    $('.edit-link').attr('href', 'https://github.com/SchoolIdolTomodachi/frgl/wiki/' + wikiPageUrl + '/_edit');
});
