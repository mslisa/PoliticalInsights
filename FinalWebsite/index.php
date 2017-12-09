
<!--
	Built from the template called Binary by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
-->

<?php

$google_api_key = "AIzaSyAMNlvrMsN-mlVz3_u2bPoaWNG_XhzAs-Y";
$propublica_api_key = "ODFvfKwCNwTHCbQQf4a3fmCkdW0qU0GnKKpHCe8q";

if(empty($pp_senator_dict)){
    $party_dict = array();
    $chamber_dict = array();
    $name_dict = array();
    $context = stream_context_create(array(
    'http' => array(
        'method' => 'GET',
        'header' => "X-API-Key: " . $propublica_api_key
    )
    ));
    $pp_senator_dict = json_decode(file_get_contents("https://api.propublica.org/congress/v1/115/senate/members.json", false, $context), true)['results'][0]['members'];
    
    foreach($pp_senator_dict as $s){
        $temp_id = $s['id'];
        $temp_party = $s['party'];
        $temp_name = $s['last_name'];
        $party_dict[$temp_id] = $temp_party;
        $chamber_dict[$temp_id] = 'senate';
        $name_dict[$temp_id] = $temp_name;
    }
}

if(empty($pp_rep_dict)){
    $context = stream_context_create(array(
    'http' => array(
        'method' => 'GET',
        'header' => "X-API-Key: " . $propublica_api_key
    )
    ));
    $pp_rep_dict = json_decode(file_get_contents("https://api.propublica.org/congress/v1/115/house/members.json", false, $context), true)['results'][0]['members'];
    
    foreach($pp_rep_dict as $r){
        $temp_id = $r['id'];
        $temp_party = $r['party'];
        $temp_name = $r['last_name'];
        $party_dict[$temp_id] = $temp_party;
        $chamber_dict[$temp_id] = 'house';
        $name_dict[$temp_id] = $temp_name;
    }
}
if(empty($id_lookup)){
    $id_lookup = array();
    $arr = array($pp_senator_dict, $pp_rep_dict);
    foreach($arr as $chamber){
        foreach($chamber as $p){
            $member_id = $p{'id'};
            $t = $p['twitter_account'];
            $f = $p['facebook_account'];
            $y = $p['youtube_account'];
            $u = $p['url'];
            if($t != NULL){
                $id_lookup[$t] = $member_id;
            }
            if($f != NULL){
                $id_lookup[$f] = $member_id;
            }
            if($y != NULL){
                $id_lookup[$y] = $member_id;
            }
            if($u != NULL){
                $id_lookup[$u] = $member_id;
            }
        }
    }
}

function id_lookup($g_object, $lookup){
    $urls = $g_object['urls'];
    $channels = $g_object['channels'];
    foreach($urls as $url){
        if(isset($lookup[$url])){
            $id = $lookup[$url];
        }
        if(isset($lookup[$url.'/'])){
            $id = $lookup[$url.'/'];
        }
    }
    foreach($channels as $channel){
        $temp_id = $channel['id'];
        if(isset($lookup[$temp_id])){
            $id = $lookup[$temp_id];
        }
    }
    return $id;
}

if(!empty($_GET['address'])){
    $api_url = "https://www.googleapis.com/civicinfo/v2/representatives?key=" . $google_api_key . "&address=" . urlencode($_GET['address']);
    
    $api_json = file_get_contents($api_url);
    $google_array = json_decode($api_json, true);
    
    $g_senator1 = $google_array['officials'][2];
    $g_senator2 = $google_array['officials'][3];
    $g_rep = $google_array['officials'][4];
    
    $g_reps_array = array($g_senator1, $g_senator2, $g_rep);
    
    $s1_id = id_lookup($g_senator1, $id_lookup);
    $s2_id = id_lookup($g_senator2, $id_lookup);
    $r_id = id_lookup($g_rep, $id_lookup);
    
    $focus_id = $s1_id;
}
    
if(!empty($_GET['focus_id'])){
    $focus_id = $_GET['focus_id'];
}

$focus_chamber = $chamber_dict[$focus_id];
$focus_party = $party_dict[$focus_id];
$focus_name = $name_dict[$focus_id];
$focus_prefix = 'Senator';
if($focus_chamber == 'house'){$focus_prefix = 'Representative';}

?>

<html>
    
	<head>
		<title>Political Insights</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="assets/css/main.css" />
        <script src="http://d3js.org/d3.v3.min.js"></script>
	</head>

<!-- This would be better off in a css file, but I got stuck trying to figure out where to put it so that it would work -->    
    <style>
    .axis path,
    .axis line {
      fill: none;
      stroke: #000;
      shape-rendering: crispEdges;
    }

    .dot {
      stroke: #000;
    }

    .tooltip {
      position: absolute;
      width: 200px;
      pointer-events: none;
      background: darkgray;
      color: white;
    }
    </style>
    
	<body class="page_bg">

		<!-- Header -->
			<header id="header">
				<a href="index.php" class="logo"><strong>Be Informed</strong> with  Political Insights</a>
				<nav>
					<a href="#menu">Menu</a>
				</nav>
			</header>

		<!-- Nav -->
			<nav id="menu">
				<ul class="links">
					<li><a href="index.php">Home</a></li>
					<li><a href="methodology/index.html">Behind the Curtain</a></li>
					<!-- <li><a href="elements.html">Elements</a></li> -->
				</ul>
			</nav>

        <?php if(empty($g_reps_array)){ ?>
		<!-- Banner if address still needed -->
			<section id="banner">
				<div class="inner">
					<h1>Welcome to Political Insights.</h1>
                    <h2>Please enter your full street address below to begin.</h2>
                    <h3>ex: 1313 Disneyland Dr, Anaheim, CA 92802</h3>
                    
                    <form action="">
                        <input name="address" type="text">
                    </form>
                    <br>
                    <br>
                    <p>Note: we do not store your address! It is sent to Google to look up who your representatives are.</p>
                </div>
            </section>
        <?php } ?>
        <?php if(!empty($g_reps_array)){ ?>
		<!-- Banner if address already given -->
			<section id="banner">
				<div class="inner">
					<h1>Welcome to Political Insights.</h1>
                    <h2>Your representatives are:</h2>
                    <br>
                    
                </div>
                
                <style>
                    .photo{width:175px; font-size:80%; text-align:center; vertical-align:top; display:inline-block;}
                </style>

                <div class="container">
                    <div class="photo">
                        <img src='https://github.com/unitedstates/images/blob/gh-pages/congress/225x275/<?php echo $s1_id; ?>.jpg?raw=true' width="75%"/>
                        Senator <?php echo $g_reps_array[0]['name'];?>
                    </div>
                    <div class="photo">
                        <img src='https://github.com/unitedstates/images/blob/gh-pages/congress/225x275/<?php echo $s2_id; ?>.jpg?raw=true' width="75%"/>
                        Senator <?php echo $g_reps_array[1]['name'];?>
                    </div>
                    <div class="photo">
                        <img src='https://github.com/unitedstates/images/blob/gh-pages/congress/225x275/<?php echo $r_id; ?>.jpg?raw=true' width="75%"/>
                        Representative <?php echo $g_reps_array[2]['name'];?>
                    </div>
                    <br><br>
                    <p>Scroll down to see your representatives' legislative effectiveness, if they garner bipartisan support, their campaign funding sources, [PLACEHOLDER etc etc etc].</p>
                    <!-- test -->
                </div>
                
			</section>
            
        <?php } ?>
            
                

		<!-- One -->
        
        <!-- Hide everything if there's no address and no rep array populated -->
        <?php if(!empty($g_reps_array)){ ?>
        <a id="vis1"></a>        
            <article id="one" class="post style1">
				<div class="image effectiveness" id="effectiveness"></div>
				<script>
                    var margin1 = {top: 40, right: 20, bottom: 40, left: 40},
                        width1 = 600 - margin1.left - margin1.right,
                        height1 = 600 - margin1.top - margin1.bottom,
                        current_id = "<? echo $focus_id;?>", current_party = "<? echo $focus_party;?>", current_chamber="<? echo $focus_chamber;?>",
                        current_congress = 115;

                    /* 
                     * value accessor - returns the value to encode for a given data object.
                     * scale - maps value to a visual display encoding, such as a pixel position.
                     * map function - maps from data value to display value
                     * axis - sets up axis
                     */ 

                    // setup x 
                    var xValue1 = function(d) { return d.sponsor_rank;}, // data -> value
                        xScale1 = d3.scale.linear().range([width1, 0]), // value -> display
                        xMap1 = function(d) { return xScale1(xValue1(d));}, // data -> display
                        xAxis1 = d3.svg.axis().scale(xScale1).orient("bottom");

                    // setup y
                    var yValue1 = function(d) { return d.cosponsor_rank;}, // data -> value
                        yScale1 = d3.scale.linear().range([0, height1]), // value -> display
                        yMap1 = function(d) { return yScale1(yValue1(d));}, // data -> display
                        yAxis1 = d3.svg.axis().scale(yScale1).orient("left");
                    
                    var sponsorCount = function(d) { return d.sponsor_count;},
                        cosponsorCount = function(d) { return d.cosponsor_count;};
                    
                    var rScale1 = d3.scale.linear().range([2, 5]);
                        
                        

                    // add the graph canvas to the body of the webpage
                    var svg1 = d3.select("#effectiveness").append("svg")
                        .attr("width", width1 + margin1.left + margin1.right)
                        .attr("height", height1 + margin1.top + margin1.bottom)
                      .append("g")
                        .attr("transform", "translate(" + margin1.left + "," + margin1.top + ")");

                    // add the tooltip area to the webpage
                    var tooltip1 = d3.select("body").append("div")
                        .attr("class", "tooltip")
                        .style("opacity", 0)
                        .style("position", "absolute")
                        .style("z-index", "10");

                    // load data
                    d3.csv("effectiveness.csv", function(error, data) {

                      // change string (from CSV) into number format
                      data.forEach(function(d) {
                        d.sponsor_rank = +d.sponsor_rank;
                        d.cosponsor_rank = +d.cosponsor_rank;
                    //    console.log(d);
                      });

                      // don't want dots overlapping axis, so add in buffer to data domain
                      xScale1.domain([d3.min(data, xValue1)-1, d3.max(data.filter(function(d) { return d.chamber == current_chamber & d.congress == current_congress }), xValue1)+1]);
                      yScale1.domain([d3.min(data, yValue1)-1, d3.max(data.filter(function(d) { return d.chamber == current_chamber & d.congress == current_congress }), yValue1)+1]);
                      rScale1.domain([0, d3.max(data.filter(function(d) { return d.chamber == current_chamber & d.congress == current_congress }), sponsorCount)])

                      // x-axis
                      svg1.append("g")
                          .attr("class", "x axis")
                          .attr("transform", "translate(0," + height1 + ")")
                          .call(xAxis1)
                        .append("text")
                          .attr("class", "label")
                          .attr("x", width1)
                          .attr("y", -6)
                          .style("text-anchor", "end")
                          .text("Sponsor Rank");

                      // y-axis
                      svg1.append("g")
                          .attr("class", "y axis")
                          .call(yAxis1)
                        .append("text")
                          .attr("class", "label")
                          .attr("transform", "rotate(-90)")
                          .attr("y", 6)
                          .attr("dy", ".71em")
                          .style("text-anchor", "end")
                          .text("Cosponsor Rank");

                      // draw dots
                      svg1.selectAll(".dot")
                          .data(data)
                        .enter().append("circle")
                        .filter(function(d) { return d.chamber == current_chamber & d.congress == current_congress })
                          .attr("class", "dot")
                          //.attr("r", function(d) {
                          //  if(d.id == current_id) {return 15}
                          //  else if(d.party == current_party) {return 5}
                          //  else {return 3.5};})
                          .attr("r", function(d) {
                              return rScale1(d.sponsor_count);
                          })
                          .attr("cx", xMap1)
                          .attr("cy", yMap1)
                          .style("stroke-width", 1)
                          .style("stroke", "lightgray")
                          
                          .style("fill", function(d) {
                            if (d.party == "R") {return "red"}
                            else {return "blue"};})
                          //.attr('fill-opacity', function(d) {
                          //  if (d.party == current_party) {return 0.9}
                          //  else {return 0.6};})
                          .attr('fill-opacity', function(d) {
                            if (d.id == current_id) {return 0.9}
                            else {return 0.2};})
                          .attr('stroke-opacity', function(d) {
                            if (d.id == current_id) {return 0.9}
                            else {return 0.5};})
                          .on("mouseover", function(d) {
                              tooltip1.transition()
                                   .duration(200)
                                   .style("opacity", .9);
                              tooltip1.html(d["name"] + "<br/><strong><u>sponsorship</u></strong><br />" + sponsorCount(d) + " bills, ranked #" + xValue1(d) 
                                + "<br /><br /><strong><u>cosponsorship</u></strong><br />" + cosponsorCount(d) + " bills, ranked #" + yValue1(d))
                                   .style("left", (d3.event.pageX + 5) + "px")
                                   .style("top", (d3.event.pageY - 28) + "px");
                          })
                          .on("mouseout", function(d) {
                              tooltip1.transition()
                                   .duration(500)
                                   .style("opacity", 0);
                          });
                       svg1.append("text")
                        .attr("x", (width1 / 2))             
                        .attr("y", 0 - (margin1.top / 2))
                        .attr("text-anchor", "middle")  
                        .style("font-size", "16px") 
                        .style('fill', function() {
                            if (current_party == "R") {return "red"}
                            else {return "blue"};})
                        .text("<? echo $focus_name . ' (' . $focus_party . ')'?>");   
                       
                    });

                </script>	
                    
                <div class="content">
					<div class="inner">
						<header>
							<h2><a target="_blank" href="methodology/#effectiveness">Legislative Effectiveness</a></h2>
							<p class="info">How effective is my rep at turning a bill into a law?</p>
						</header>
                        <h3>What am I looking at?</h3>
                        <ul>
                            <li>Each circle represents a <b>person</b></li>
                            <li>The size of the circle represents how many bills he or she has sponsored</strong></li>
                            <li>The color of the circle represents that person's political party</li>
                            <li>The circle with a dark fill color is your selected representative</li>
                            <li>Mouse-over circles for more detailed information</li>
                            <li>Click the names below to change your selection</li>
                            <li>Click this section's title to see more detail about this metric</li>
                        </ul>
						<p>Effectiveness is an indication of how successful members are at writing bills that go on to become law. Being ranked #1 would mean that the member sponsors or cosponsors bills that make it further along in the legislative process, on average, than the rest of the members in his or her caucus. This figure shows the member's effectiveness both as a bill's sponsor (horizontal axis) and cosponsor (vertical axis). Top-right is most effective overall; bottom-left is least effective overall.</p>
                        
                    
                    <!-- Hide buttons if no reps are identified -->
						<ul class="actions">
							<li><a href="?address=<?php echo urlencode($_GET['address']);?>&focus_id=<?php echo $s1_id;?>#vis1" class="button alt"><?php echo $g_reps_array[0]['name'];?></a></li>
                        
                            <li><a href="?address=<?php echo urlencode($_GET['address']);?>&focus_id=<?php echo $s2_id;?>#vis1" class="button alt"><?php echo $g_reps_array[1]['name'];?></a></li>
                        
                            <li><a href="?address=<?php echo urlencode($_GET['address']);?>&focus_id=<?php echo $r_id;?>#vis1" class="button alt"><?php echo $g_reps_array[2]['name'];?></a></li>
						</ul>
                        
					</div>
				</div>
			</article>
            
            
            
		<!-- Two -->
        <a id="vis2"></a>
			<article id="two" class="post invert style1 alt">
				<?if(!empty($_GET['address'])){echo '<div class="image bipart" id="bipart"></div>';}?>
                <script>
                    
                    d3.csv('effectiveness.csv', function(csv){
                        var values = [];
                        var vert_ref = 0
                        var sponsor_count = 0
                        var bi_count = 0
                        csv = csv.filter(function(row) {
                            return row.party == '<? echo $focus_party; ?>' & row.congress == '115' & row.chamber == '<? echo $focus_chamber; ?>';
                        })
                        values = csv.map(function(d) {
                            if(d['id'] == '<? echo $focus_id; ?>'){
                                vert_ref = +d['bi_pct'];
                                sponsor_count = +d['sponsor_count']
                            }
                            
                            return +d['bi_pct']});

                    // Formatters for counts and times (converting numbers to Dates).
                    var formatCount = d3.format(",.0f"),
                        formatPct = d3.format('.0%');

                    var margin = {top: 40, right: 30, bottom: 50, left: 30},
                        width = 600 - margin.left - margin.right,
                        height = 400 - margin.top - margin.bottom;

                    var x = d3.scale.linear()
                        .domain([0, 1])
                        .range([0, width]);

                    // Generate a histogram using twenty uniformly-spaced bins.
                    var data = d3.layout.histogram()
                        .bins(x.ticks(10))
                        (values);

                    var y = d3.scale.linear()
                        .domain([0, d3.max(data, function(d) { return d.y; })])
                        .range([height, 0]);

                    var xAxis = d3.svg.axis()
                        .scale(x)
                        .orient("bottom")
                        .tickFormat(formatPct);

                    var svg2 = d3.select("#bipart").append("svg")
                        .attr("width", width + margin.left + margin.right)
                        .attr("height", height + margin.top + margin.bottom)
                      .append("g")
                        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                    var bar = svg2.selectAll(".bar")
                        .data(data)
                      .enter().append("g")
                        .attr("class", "bar")
                        .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

                    bar.append("rect")
                        .attr("x", 1)
                        .attr("width", x(data[0].dx) - 1)
                        .attr("height", function(d) { return height - y(d.y); })
                        .style('fill', function() {
                            if ("<? echo $focus_party; ?>" == "R") {return "red"}
                            else {return "blue"};})
                        .style('opacity', 0.5)
                    console.log(values)
                    bar.append("text")
                        .attr("dy", ".75em")
                        .attr("y", 6)
                        .attr("x", x(data[0].dx) / 2)
                        .attr("text-anchor", "middle")
                        .style("fill", "white")
                        .text(function(d) { return formatCount(d.y); });

                    svg2.append("g")
                        .attr("class", "x axis")
                        .attr("transform", "translate(0," + height + ")")
                        .call(xAxis);
                        
                    svg2.append("line")
                        .attr("x1", x(vert_ref))
                        .attr("y1", 0)
                        .attr("x2", x(vert_ref))
                        .attr("y2", height)
                        .style("stroke-width", 5)
                        .style("stroke", function() { return ( '<? echo $focus_party; ?>' == 'R' ? "red" : "blue");})
                        .style("fill", "none");
                    
                    svg2.append("text")
                        .attr("x", (width / 2))             
                        .attr("y", 0 - (margin.top / 2))
                        .attr("text-anchor", "middle")  
                        .style("font-size", "16px") 
                        .style('fill', function() { return ( '<? echo $focus_party; ?>' == 'R' ? "red" : "blue");})
                        .text("<? echo $focus_name . ' (' . $focus_party . ')'?>");   
                        
                    svg2.append("text")
                        .attr("x", (width / 2))
                        .attr("y", height + 40)
                        .attr("text-anchor", "middle")
                        .style("font-size", "16px")
                        .text("<? echo $focus_prefix; ?> <? echo $focus_name; ?> received bipartisan cosponsorship for " + d3.format('.0%')(vert_ref) + " of sponsored bills.")
                    })
                </script>
                
				<div class="content">
					<div class="inner">
						<header>
							<h2><a target="_blank" href="methodology/#bipartisanship">Bipartisanship</a></h2>
							<p class="info">Does my rep sponsor bills that gain support from the opposite party?</p>
						</header>
                        <h3>What am I looking at?</h3>
                        <ul>
                            <li>Each bar represents a <b>group</b> of people</li>
                            <li>The position of the bar from left to right indicates the percentage of those people's bills that gain bipartisan cosponsorship</li>
                            <li>The height of the bar represents how many legislators are in that group</li>
                            <li>The color indicates party. In this case, only members of the same party are considered for comparison</li>
                            <li>Click the names below to change your selection</li>
                            <li>Click this section's title to see more detail about this metric</li>
                        </ul>
						<p>This Bipartisanship figure shows how <? echo $focus_prefix; ?> <? echo $focus_name; ?> compares to other members of the same party with respect to getting support from accross the aisle for sponsored legislation. For the purpose of this analysis, we a bill to have bipartisan support if at least 25% of its cosponsors are members of the opposite party.</p>
                    
                        <ul class="actions">
							<li><a href="?address=<?php echo urlencode($_GET['address']);?>&focus_id=<?php echo $s1_id;?>#vis2" class="button alt"><?php echo $g_reps_array[0]['name'];?></a></li>

                            <li><a href="?address=<?php echo urlencode($_GET['address']);?>&focus_id=<?php echo $s2_id;?>#vis2" class="button alt"><?php echo $g_reps_array[1]['name'];?></a></li>

                            <li><a href="?address=<?php echo urlencode($_GET['address']);?>&focus_id=<?php echo $r_id;?>#vis2" class="button alt"><?php echo $g_reps_array[2]['name'];?></a></li>
						</ul>
					</div>
				</div>
			</article>

		<!-- Three -->
        <a id="vis3"></a>
			<article id="three" class="post style1">
                <div class="image effectiveness" id="financial"></div>
                <script>
                var margin2 = {top: 40, right: 20, bottom: 30, left: 40},
                    width2 = 700 - margin2.left - margin2.right,
                    height2 = 500 - margin2.top - margin2.bottom,
                    current_id = "<? echo $focus_id;?>", current_party = "<? echo $focus_party;?>", current_chamber="<? echo $focus_chamber;?>",
                    current_congress = 115;
                    
                /* 
                 * value accessor - returns the value to encode for a given data object.
                 * scale - maps value to a visual display encoding, such as a pixel position.
                 * map function - maps from data value to display value
                 * axis - sets up axis
                 */ 

                // setup x 
                var xValue2 = function(d) { return d['8'];}, // data -> value
                    xScale2 = d3.scale.linear().range([0, width2]), // value -> display
                    xMap2 = function(d) { return xScale2(xValue2(d));}, // data -> display
                    xAxis2 = d3.svg.axis().scale(xScale2).orient("bottom").tickFormat(d3.format(".2s"));

                // setup y
                var yValue2 = function(d) { return d['9'];}, // data -> value
                    yScale2 = d3.scale.linear().range([height2, 0]), // value -> display
                    yMap2 = function(d) { return yScale2(yValue2(d));}, // data -> display
                    yAxis2 = d3.svg.axis().scale(yScale2).orient("left").tickFormat(d3.format(".2s"));

                // add the graph canvas to the body of the webpage
                var svg3 = d3.select("#financial").append("svg")
                    .attr("width", width2 + margin2.left + margin2.right)
                    .attr("height", height2 + margin2.top + margin2.bottom)
                    //.call(d3.behavior.zoom().on("zoom", function () {
                    //    svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
                    //}))
                    .append("g")
                    /*.attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");*/

                // add the tooltip area to the webpage
                var tooltip3 = d3.select("body").append("div")
                    .attr("class", "tooltip")
                    .style("opacity", 0);

                // load data
                d3.csv("fincampaign_w_twitter.csv", function(error, data) {
                  // change string (from CSV) into number format
                  data.forEach(function(d) {
                    d['8'] = +d['8'];
                    d['9'] = +d['9'];
                    //console.log(d);
                  });

                  // don't want dots overlapping axis, so add in buffer to data domain
                  xScale2.domain([d3.min(data, xValue2)-1, d3.max(data, xValue2)+1]);
                  yScale2.domain([d3.min(data, yValue2)-1, d3.max(data, yValue2)+1]);

                  // x-axis
                  svg3.append("g")
                      .attr("class", "x axis")
                      .attr("transform", "translate(0," + height2 + ")")
                      .call(xAxis2)
                    .append("text")
                      .attr("class", "label")
                      .attr("x", width2)
                      .attr("y", -6)
                      .style("text-anchor", "end")
                      .text("Individual Contributions");

                  // y-axis
                  svg3.append("g")
                      .attr("class", "y axis")
                      .call(yAxis2)
                    .append("text")
                      .attr("class", "label")
                      .attr("transform", "rotate(-90)")
                      .attr("y", 6)
                      .attr("dy", ".71em")
                      .style("text-anchor", "end")
                      .text("PAC Contributions");

                  // draw dots
                  svg3.selectAll(".dot")
                      .data(data)
                    .enter().append("circle")
                    //.filter(function(d) { return d.chamber == current_chamber & d.congress == current_congress })
                      .attr("class", "dot")
                      /*.attr("r", function(d) {
                            if(d['0'] == current_id) {return 15}
                            else if(d['4'].charAt(0) == current_party) {return 4}
                            else {return 2};})*/
                      .attr("r", 4)
                      .attr("cx", xMap2)
                      .attr("cy", yMap2)
                      .style("fill", function(d) {
                        if (d['4'] == "REP") {return "red"}
                        else {return "blue"};})
                      /*.style("stroke", function(d) {
                        if (d['4'] == "REP") {return "red"}
                        else {return "blue"};})*/
                      .style("stroke", "lightgray")
                      .attr('stroke-opacity', function(d) {
                            if (d.id == current_id) {return 0.9}
                            else {return 0.5};})
                      .attr('fill-opacity', function(d) {
                            if (d['0'] == current_id) {return 0.9}
                            else {return 0.2};})
                      /*.attr('fill-opacity', function(d) {
                            if(d['0'] == current_id) {return .9}
                            else if (d['4'].charAt(0) == current_party) {return 0.3}
                            else {return 0.1};})  */
                      .on("mouseover", function(d) {
                          tooltip3.transition()
                               .duration(200)
                               .style("opacity", 1);
                          tooltip3.html(d['3'] + "<br/> Individual: " + d3.format('.2s')(xValue2(d)) 
                                + "<br />PAC: " + d3.format('.2s')(yValue2(d)))
                                   .style("left", (d3.event.pageX + 5) + "px")
                                   .style("top", (d3.event.pageY - 28) + "px");})
                      
                      .on("mouseout", function(d) {
                          tooltip3.transition()
                               .duration(500)
                               .style("opacity", 0);
                      });
                       svg3.append("text")
                        .attr("x", (width1 / 2))             
                        .attr("y", 0 - (margin1.top / 2))
                        .attr("text-anchor", "middle")  
                        .style("font-size", "16px") 
                        .style("text-decoration", "underline")  
                        .text("<? echo $focus_name . ' (' . $focus_party . ')'?>");                        
                });
                
                </script>   
				<div class="content">
					<div class="inner">
						<header>
							<h2><a target="_blank" href="methodology/#financial">Campaign Contribution Sources</a></h2>
							<p class="info">How does my rep compare for contributions from individuals and PACs?</p>
						</header>
                        <h3>What am I looking at?</h3>
                        <ul>
                            <li>Each circle represents a <b>person</b></li>
                            <li>The horizontal position shows how much money came from individual donors in the last campaign</li>
                            <li>The vertical position shows how much money came from Political Action Committees in the last campaign</li>
                            <li>The color indicates party</li>
                            <li>The circle with a dark fill color is your selected representative. <i>note: some representatives are missing from the dataset. We apologize for the inconvenience.</i></li>
                            <li>Mouse-over circles for more detailed information</li>
                            <li>Click the names below to change your selection</li>
                            <li>Click this section's title to see more detail about this metric</li>
                        </ul>
						<p>When conducting their campaigns, representatives accept donations from both private individuals as well as Political Action Committees (PACS), organizations that collect financial contributions from their members and use the funds to aid or hinder candidate campaigns, or legislation. This plot shows the dollar amounts members received for both types of sources. There are a few cases of missing data, so if you do not see a large filled-in circle, it means that your selected representative's data is not available.</p>

                    <!-- Hide buttons if no reps are identified -->
						<ul class="actions">
							<li><a href="?address=<?php echo urlencode($_GET['address']);?>&focus_id=<?php echo $s1_id;?>#vis3" class="button alt"><?php echo $g_reps_array[0]['name'];?></a></li>

                            <li><a href="?address=<?php echo urlencode($_GET['address']);?>&focus_id=<?php echo $s2_id;?>#vis3" class="button alt"><?php echo $g_reps_array[1]['name'];?></a></li>

                            <li><a href="?address=<?php echo urlencode($_GET['address']);?>&focus_id=<?php echo $r_id;?>#vis3" class="button alt"><?php echo $g_reps_array[2]['name'];?></a></li>
						</ul>
					</div>
				</div>
			</article>

		<!-- Four -->
			<article id="four" class="post invert style1 alt">
				<div class="image">
					Placeholder for d3 script or some other featured thing.
				</div>
				<div class="content">
					<div class="inner">
						<header>
							<h2><a href="generic.html">Placeholder</a></h2>
							<p class="info">Here's some text</p>
						</header>
						<p>Description of stuff and things</p>
						<ul class="actions">
							<li><a href="generic.html" class="button alt">Hyperlink Button</a></li>
						</ul>
					</div>
				</div>
			</article>

		<!-- Five -->
			<article id="five" class="post style1">
				<div class="image">
					Placeholder for d3 script or some other featured thing.
				</div>
				<div class="content">
					<div class="inner">
						<header>
							<h2><a href="generic.html">Placeholder</a></h2>
							<p class="info">Here's some text</p>
						</header>
						<p>Description of stuff and things</p>
						<ul class="actions">
							<li><a href="generic.html" class="button alt">Hyperlink Button</a></li>
						</ul>
					</div>
				</div>
			</article>

		<!-- Six -->
			<article id="six" class="post invert style1 alt">
				<div class="image">
					Placeholder for d3 script or some other featured thing.
				</div>
				<div class="content">
					<div class="inner">
						<header>
							<h2><a href="generic.html">Placeholder</a></h2>
							<p class="info">Here's some text</p>
						</header>
						<p>Description of stuff and things</p>
						<ul class="actions">
							<li><a href="generic.html" class="button alt">Hyperlink Button</a></li>
						</ul>
					</div>
				</div>
			</article>

        <?php } ?> <!-- Closing tag for the php trick to hide everything if there's no address -->
		<!-- Footer -->
			<footer id="footer">
				
				<div class="copyright">
					&copy; Political Insights. Website layout by <a href="https://templated.co">TEMPLATED</a>.
				</div>
			</footer>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>
            

	</body>
</html>