<template>
  <div id="treemap"/>
</template>

<script>
import * as d3 from "d3";

export default {
  components: {},
  name: "App4",

    data() {
    return {
    videoGames: {
    
  "name" : "Lime Expanation",
  "children" : [{
    "name": "positiv",
    "id": "p",
    "children": [{
            "name": "financial",
            "children": [{
                "name": "Balance",
                "category": "financial",
                "value": "0.077"
            },
            {
                "name": "Available Income",
                "category": "financial",
                "value": "0.036"
            },
            {
                "name": "Previous Loans",
                "category": "financial",
                "value": "0.012"
            }
            ]
        },
        {
            "name": "personal",
            "children": [{
                    "name": "Housing",
                    "category": "personal",
                    "value": "0.0038"
                },
                {
                    "name": "Job",
                    "category": "personal",
                    "value": "0.009"
                }
            ]
        },
        {
            "name": "loan",
            "children": [{
                    "name": "Other Debtors",
                    "category": "loan",
                    "value": "0.004"
                },
                {
                    "name": "People Liable",
                    "category": "loan",
                    "value": "0.006"
                }
            ]
        }
    ]
    },
    {
    "name": "negativ",
    "id": "n",
    "children": [{
                "name":"financial",
            "children":[
               {
                  "name":"History",
                  "category":"financial",
                  "value": "0.11"
               },
               {
                  "name":"Savings",
                  "category":"financial",
                  "value": "0.11"
               },
               {
                  "name":"Assets",
                  "category":"financial",
                  "value": "0.05"
               },
               {
                  "name":"Other Loans",
                  "category":"financial",
                  "value": "0.01"
               }
            ]
         },
         {
            "name":"personal",
            "children":[
               {
                  "name":"Employment",
                  "category":"personal",
                  "value": "0.02"
               },
               {
                  "name":"Residence",
                  "category":"personal",
                  "value": "0.003"
               },
               {
                  "name":"Age",
                  "category":"personal",
                  "value": "0.007"
               },
               {
                  "name":"Telephone",
                  "category":"personal",
                  "value": "0.02"
               }
            ]
         },
         {
            "name":"loan",
            "children":[
               {
                  "name":"Duration",
                  "category":"loan",
                  "value": "0.05"
               },
               {
                  "name":"Purpose",
                  "category":"loan",
                  "value": "0.02"
               },
               {
                  "name":"Amount",
                  "category":"loan",
                  "value": "0.03"
               }
            ]
         }
    ]
    }
   ]
  }
};
  },
  mounted() {
    this.generateTreeMap();
  },
  methods: {
    generateTreeMap() {
      const w = 800;
      const h = 500;



    const hierarchy = d3.hierarchy(this.videoGames)
                        .sum(d=>d.value)  //sums every child values
                        .sort((a,b)=>b.value-a.value), // and sort them in descending order 

          treemap = d3.treemap()
                      .size([800, 500])
                      .padding(1),

          root = treemap(hierarchy);

    const categories = this.videoGames.children.map(d=>d.name),      

          colors = ['#1C1832', '#9E999D', '#F2259C', '#347EB4', 
                      '#08ACB6', '#91BB91', '#BCD32F', '#75EDB8',
                      "#89EE4B", '#AD4FE8', '#D5AB61', '#BC3B3A',
                      '#F6A1F9', '#87ABBB', '#412433', '#56B870', 
                      '#FDAB41', '#64624F'],

          colorScale = d3.scaleOrdinal() // the scale function
                        .domain(categories) // the data
                        .range(colors);    // the way the data should be shown             

          

    const svg = d3.select("#treemap") //make sure there's a svg element in your html file
                  .append("svg")
                  .attr("width", w)
                  .attr("height", h);

              svg.selectAll("rect")
                 .data(root.leaves())
                 .enter()
                 .append("rect")
                 .attr("x", d=>d.x0)
                 .attr("y", d=>d.y0)
                 .attr("width",  d=>d.x1 - d.x0)
                 .attr("height", d=>d.y1 - d.y0)
                 .attr("fill", d=>colorScale(d.data.category));
}                    
    }
  }
</script>