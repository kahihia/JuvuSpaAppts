function DisplayCircle(){};



var options_transitions = {

    clickDis: function() {

		$(".c_dis").appendTo($(".s_canvas"));
	  	d3.select(".c_dis").transition()
	  		.attr("cx", 450)
	  		.attr("cy", 230)
	  		.attr("r", 200)
	  		.attr("fill", first_color)
	  		.duration(1000)
	  		.ease("elastic", 5, 3);
	  	
	  	d3.select(".distance").transition()
	  		.style("left","305px")
	  		.style("top","170px")
	  		.duration(1000)
	  		.ease("elastic", 5, 3);
	  		
	  	d3.select(".dis_form").transition()
	  		.style("display","block")
	  		.style("opacity","1")
	  		.duration(500)
	  		.delay(500);
	  		
	  	d3.select(".c_nei").transition()
	  		.attr("cx", 615)
	  		.attr("cy", 410)
	  		.attr("r", 65)
	  		.duration(1000)
	  		.ease("elastic", 5, 4);
	  		
	  	d3.select(".neighbor").transition()
	  		.style("left"," 442px")
	  		.style("top"," 400px")
	  		.style("display","none")
	  		.style("opacity",0)
	  		.duration(1000)
	  		.ease("elastic", 5, 4);
	  	
	  	d3.select(".nei_form").transition()
	  		.style("display","none")
	  		.style("opacity","0")
	  		.duration(500);
	  	
	  	d3.select(".distance").transition()
	  		.style("display","block")
	  		.style("opacity", 1)
	  		.delay(1000)
	  		.duration(300);
	  	
	  	d3.select(".neighbor").transition()
	  		.style("display","block")
	  		.style("opacity","1")
	  		.delay(1000)
	  		.duration(300)
	  	
	  	d3.select(".where").transition()
	  		.style("display","none")
	  		.style("opacity", 0);
	}

}
