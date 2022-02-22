<template>
  <svg class="svg"></svg>
</template>

<script>
import * as d3 from "d3";

export default {
  components: {},
  name: "App4",

  mounted() {
    this.generateTreeMap();
  },
  methods: {
    generateTreeMap() {
      
    document.addEventListener('DOMContentLoaded', () =>{
    fetch("https://cdn.freecodecamp.org/testable-projects-fcc/data/tree_map/video-game-sales-data.json")
        .then(res=>res.json())
        .then(res=>{
            drawTreeMap(res);   
        });
    });
    const drawTreeMap = (dataset)=>{  
       const hierarchy = d3.hierarchy(dataset)
                        .sum(d=>d.value)  //sum every child's values
                        .sort((a,b)=>b.value-a.value) // and sort them in descending order 
    
    const treemap = d3.treemap()
                  .size([800, 900]) // width: 400px, height:450px
                  .padding(1);      // set padding to 1
    
    const root = treemap(hierarchy);

    const svg = d3.select("svg"); //make sure there's a svg element in your html file.

              svg.selectAll("rect")
                 .data(root.leaves())
                 .enter()
                 .append("rect")
                 .attr("x", d=>d.x0)   
                 .attr("y", d=>d.y0)
                 .attr("width",  d=>d.x1 - d.x0)
                 .attr("height", d=>d.y1 - d.y0)
                 .attr("fill", "#5AB7A9")
    }
    }
  }
}
</script>