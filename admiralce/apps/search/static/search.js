
$().ready(function () {

	$('#rank-filter').on('input',  function () {
		nRankFilter = $(this).val();
		$(".mini-profile").filter(function(){return $(this).data("rank") < nRankFilter}).hide();
		$(".mini-profile").filter(function(){return $(this).data("rank") >= nRankFilter}).show();
		if( nRankFilter > 0 )
			$("#filter-results-label").text( nRankFilter + " Stars");
		else
			$("#filter-results-label").text("All Results");

		var count = $(".mini-profile:visible").length;
		$("#results-count span").text( count );
	});
});

