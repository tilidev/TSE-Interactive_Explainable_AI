<template>
  <div>
    <div :id="'tooltip' + id" class="tooltip"></div>
    <div :id="id" />
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  props: {
    id: String,
    expType: String,
    instance: Object,
    whatif: Boolean,
    detailView: Boolean,
  },
  watch: {
    instance() {
      d3.select("#" + this.id).html(null);
      this.sendExplanationRequest();
    },
    whatif() {
      this.generateTreeMap();
    },
    detailView() {
      this.generateTreeMap();
    },
    expType() {
      d3.select("#" + this.id).html(null);
      this.sendExplanationRequest();
    },
  },
  data() {
    return {
      simpleExpData: {
        name: "Explanation",
        children: [
          { name: "positive", children: [] },
          {
            name: "negative",
            children: [],
          },
        ],
      },
      detailExpData: {
        name: "Explanation",
        children: [
          {
            name: "positive",
            children: [
              { name: "financial", children: [] },
              { name: "personal", children: [] },
              { name: "loan", children: [] },
            ],
          },
          {
            name: "negative",
            children: [
              { name: "financial", children: [] },
              { name: "personal", children: [] },
              { name: "loan", children: [] },
            ],
          },
        ],
      },
    };
  },
  inject: ["attributeData", "apiUrl"],
  mounted() {
    this.sendExplanationRequest();
  },
  methods: {
    saveData(result) {
      (this.simpleExpData = {
        name: "Explanation",
        children: [
          { name: "positive", children: [] },
          {
            name: "negative",
            children: [],
          },
        ],
      }),
        (this.detailExpData = {
          name: "Explanation",
          children: [
            {
              name: "positive",
              children: [
                { name: "financial", children: [] },
                { name: "personal", children: [] },
                { name: "loan", children: [] },
              ],
            },
            {
              name: "negative",
              children: [
                { name: "financial", children: [] },
                { name: "personal", children: [] },
                { name: "loan", children: [] },
              ],
            },
          ],
        });
      for (let obj of result) {
        let childElement = {};
        childElement.name = this.attributeData.labels[obj.attribute];
        childElement.category = this.attributeData.categories[obj.attribute];
        childElement.value = Math.abs(obj.influence);
        childElement.attributeValue = this.instance[obj.attribute];
        let catObj;
        if (obj.influence < 0) {
          for (let category of this.detailExpData.children[0].children) {
            if (
              category.name === this.attributeData.categories[obj.attribute]
            ) {
              catObj = category;
            }
          }
        } else {
          for (let category of this.detailExpData.children[1].children) {
            if (
              category.name === this.attributeData.categories[obj.attribute]
            ) {
              catObj = category;
            }
          }
        }
        catObj.children.push(childElement);
      }
      for (let direction of [0, 1]) {
        for (let category of this.detailExpData.children[direction].children) {
          let sum = 0;
          for (let attribute of category.children) {
            sum += attribute.value;
          }
          this.simpleExpData.children[direction].children.push({
            name: category.name,
            value: sum,
          });
        }
      }
      this.generateTreeMap();
    },
    getResult(href, result) {
      if (!result) {
        const axios = require("axios");
        axios
          .get(this.apiUrl + "explanations/" + this.expType + "?uid=" + href)
          .then((response) => {
            if (response.data.values) {
              result = response.data.values;
              this.saveData(result);
            }
          });
        setTimeout(() => this.getResult(href, result), 1000);
      }
      return result;
    },
    sendExplanationRequest() {
      const axios = require("axios");
      axios
        .post(this.apiUrl + "explanations/" + this.expType, {
          instance: this.instance,
        })
        .then((response) => {
          let href = response.data.href;
          this.getResult(href, null);
        });
    },
    generateTreeMap() {
      d3.select("#" + this.id).html(null);
      const detailView = this.detailView;
      const w = this.whatif ? 640 : 1320;
      const h = 500;
      const hierarchy = d3
          .hierarchy(detailView ? this.detailExpData : this.simpleExpData)
          .sum((d) => d.value) //sums every child values
          .sort((a, b) => b.value - a.value), // and sort them in descending order
        treemap = d3
          .treemap()
          .size([w, h])
          .padding(this.detailView ? 1 : 2),
        root = treemap(hierarchy);

      var colors = ["#15803d", "#b91c1c"],
        colorScale = d3
          .scaleOrdinal() // the scale function
          .domain(["positive", "negative"]) // the data
          .range(colors); // the way the data should be shown

      const tooltip = d3
        .select("#tooltip" + this.id)
        .style("font-size", "16px");

      const svg = d3
        .select("#" + this.id) //make sure there's a svg element in your html file
        .append("svg")
        .attr("width", w)
        .attr("height", h);

      svg
        .selectAll("rect")
        .data(root.leaves())
        .enter()
        .append("rect")
        .attr("x", (d) => d.x0)
        .attr("y", (d) => d.y0)
        .attr("width", (d) => d.x1 - d.x0)
        .attr("height", (d) => d.y1 - d.y0)
        .attr("fill", function (d) {
          return colorScale(
            detailView ? d.parent.parent.data.name : d.parent.data.name
          );
        })
        .attr("fill-opacity", 1.0)
        .on("mouseenter", function (event, d) {
          if (detailView) {
            tooltip
              .append("div")
              .text(
                d.parent.data.name.charAt(0).toUpperCase() +
                  d.parent.data.name.slice(1)
              )
              .attr("class", "tt-category pb-1 text-left");
          }

          tooltip
            .append("div")
            .text(
              d.data.name.charAt(0).toUpperCase() +
                d.data.name.slice(1) +
                (detailView ? ": " + d.data.attributeValue : "")
            )
            .attr("class", "tt-name text-left pb-2 font-bold");
          tooltip
            .append("div")
            .text(Math.round(d.data.value * 10000) / 100 + "%")
            .style(
              "color",
              colorScale(
                detailView ? d.parent.parent.data.name : d.parent.data.name
              )
            )
            .attr("class", "tt-value font-bold text-left");

          tooltip
            .style("opacity", 1)
            .style("margin-top", d.y0 + 8 + "px")
            .style("margin-left", d.x0 + 8 + "px");
        })
        .on("mouseout", function () {
          tooltip.style("opacity", 0).selectAll("div").remove();
        });

      svg
        .selectAll("text")
        .data(root.leaves())
        .enter()
        .append("text")
        .attr("x", (d) => d.x0 + 10)
        .attr("y", (d) => d.y0 + 25)
        .text(function (d) {
          if (d.x1 - d.x0 >= 140 && d.y1 - d.y0 >= 50) {
            return d.data.name.charAt(0).toUpperCase() + d.data.name.slice(1);
          }
        })
        .attr("font-size", "15px")
        .attr("font-weight", "600")
        .attr("fill", "white");

      svg
        .selectAll("vals")
        .data(root.leaves())
        .enter()
        .append("text")
        .attr("x", (d) => d.x0 + 10)
        .attr("y", (d) => d.y0 + 45)
        .text(function (d) {
          if (d.x1 - d.x0 >= 140 && d.y1 - d.y0 >= 50) {
            return Math.round(d.data.value * 10000) / 100 + "%";
          }
        })
        .attr("font-size", "15px")
        .attr("margin-top", "16px")
        .attr("fill", "white");
    },
  },
};
</script>

<style scoped>
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
.tt-name {
  font-size: 1.4rem;
  font-weight: 1200;
}
</style>
<style src="@vueform/toggle/themes/default.css"></style>
