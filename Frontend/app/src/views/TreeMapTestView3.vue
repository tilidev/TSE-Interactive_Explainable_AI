<template>
  <svg class="treemap"></svg>
</template>

<script>
import * as d3 from "d3";


export default{
  components: {},
  name: "App3",

  mounted() {
    this.createMap();
  },
  methods: {
    createMap() {
      // https://github.com/thegoodideaco/visualizing-hierarchies/blob/master/datasets/populations.json
      const url =
        "https://s3-us-west-2.amazonaws.com/s.cdpn.io/1226572/populations.json";

      // This will be used to create the viewbox sizes and the circle/rectangle sizes
      const width = 600;
      const height = 400;

      // Set constants for existing elements

      const svg = d3.select("#treemap");
      svg.attr("viewBox", `0, 0 ${width} ${height}`);

      const tooltip = d3.select("#tooltip");

      // https://github.com/d3/d3-fetch/blob/master/README.md#json
      d3.json(url).then(function (data) {
        const groupOrder = ["region", "subregion"];
        const nestedData = {
          name: "World Population",
          values: nester(groupOrder).entries(data),
        };

        drawVisualization(nestedData);
      });

      function drawVisualization(data) {
        // https://github.com/d3/d3-hierarchy/blob/master/README.md#hierarchy
        let hierarchy = d3.hierarchy(data, (v) => v.values);
        // Totals are used for treemap rectangle sizes
        hierarchy.sum((v) => v.value);
        hierarchy.sort((a, b) => d3.ascending(a.value, b.value));

        // https://github.com/d3/d3-hierarchy/blob/master/README.md#treemap
        const treemap = d3.treemap();
        const treemapData = treemap(hierarchy);
        const subregions = treemapData
          .descendants()
          .filter((d) => d.depth === 2);
        const countries = treemapData
          .descendants()
          .filter((d) => d.depth === 3);

        svg
          .selectAll("rect.subregion")
          // Binds data. https://github.com/d3/d3-selection/blob/v1.4.1/README.md#selection_data
          .data(subregions)
          // Adds elemet for each data point. https://github.com/d3/d3-selection/blob/maater/README.md#selection_enter
          .enter()
          .append("rect")
          .attr("class", "subregion")
          .attr("x", (d) => d.x0 * width)
          .attr("y", (d) => d.y0 * height)
          .attr("width", (d) => (d.x1 - d.x0) * width)
          .attr("height", (d) => (d.y1 - d.y0) * height)
          .attr(
            "fill",
            (d, i) => `hsl(${(360 / subregions.length) * i}, 70%, 50%)`
          )
          .attr("stroke", "rgba(255, 255, 255, .25)");

        svg
          .selectAll("rect.country")
          .data(countries)
          .enter()
          .append("rect")
          .attr("class", "country")
          .attr("x", (d) => d.x0 * width)
          .attr("y", (d) => d.y0 * height)
          .attr("width", (d) => (d.x1 - d.x0) * width)
          .attr("height", (d) => (d.y1 - d.y0) * height)
          .attr("fill", "transparent")
          .attr("stroke", "rgba(255, 255, 255, .25)")

          .on("mouseenter", function (d) {
            // https://github.com/d3/d3-format/blob/master/README.md#format
            const format = d3.format(",");

            d3.select(this)
              .attr("fill", "rgba(0, 0, 0, .25)")
              .attr("stroke", "rgba(255, 255, 255, .5)");

            tooltip
              .append("div")
              .text(`${d.data.subregion} (${d.data.region})`)
              .attr("class", "tt-region");

            tooltip.append("div").text(d.data.key).attr("class", "tt-country");

            tooltip
              .append("div")
              .text(format(d.value))
              .attr("class", "tt-population");

            const tooltipElement = tooltip.node().getBoundingClientRect();
            const { height: elementHeight } = tooltipElement;

            tooltip
              .style("opacity", 1)
              // https://github.com/d3/d3-selection/blob/master/README.md#event
              .style("left", `${d3.event.pageX}px`)
              .style("top", `${d3.event.pageY - elementHeight}px`);
          })
          .on("mouseout", function () {
            d3.select(this)
              .attr("fill", "transparent")
              .attr("stroke", "rgba(255, 255, 255, .25)");

            tooltip.style("opacity", 0).selectAll("div").remove();
          });
      }

      // Create nested data
      function nester(groupOrder) {
        const n = d3.nest();
        groupOrder.forEach((v) => {
          n.key((node) => node[v]);
        });
        return n;
      }
    },
  },
}
</script>



<style scoped>
body {
  width: 100%;
  min-height: 100vh;
  font-family: Verdana, sans-serif;
  color: #333;
}
h1 {
  margin-bottom: 0;
  font-size: 30px;
}
p {
  font-size: 16px;
}
.container {
  max-width: 750px;
  margin: 1rem auto;
  display: flex;
  flex-direction: column;
}
.tooltip {
  position: absolute;
  opacity: 0;
  pointer-events: none;
  transition: all 0.2s ease-in-out;
  max-width: 400px;
  border-radius: 4px;
  background: #fff;
  box-shadow: 0 1px 5px rgba(51, 51, 51, 0.5);
  padding: 1rem;
}
.tt-country {
  font-size: 1.1rem;
  font-weight: 900;
}
</style>
