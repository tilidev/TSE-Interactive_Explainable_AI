<template>
  <div class="container"></div>
</template>

<script>
import * as d3 from "d3";

export default {
  components: {},
  name: "Home",
  data() {
    return {
      dataset: [5, 10, 15, 20, 25],
    };
  },
  mounted() {
    this.generateCircles();
  },
  methods: {
    generateCircles() {
      const w = 500;
      const h = 400;
      var svg = d3
        .select(".container")
        .append("svg")
        .attr("width", w)
        .attr("height", h);

      svg
        .selectAll("circles")
        .data(this.dataset)
        .enter()
        .append("circle")
        .attr("cx", function (d, i) {
          return i * 50 + d * 2;
        })
        .attr("cy", h / 2)
        .attr("r", function (d) {
          return d;
        })
        .attr("fill", "blue");
    },
  },
};
</script>