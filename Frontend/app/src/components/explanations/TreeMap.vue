<template>
  <div class="bg-white px-8 py-4 my-8">
    <div id="tooltip" class="tooltip"></div>
    <div id="treemap" />
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  components: {},

  data() {
    return {
      expType: "lime",
      detailView: true,
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
      instance: {
        id: 0,
        balance: "no account",
        duration: 6,
        history: "paid back previous loans at this bank",
        purpose: "furniture",
        amount: 1169,
        savings: "above 1000 EUR",
        employment: "more than 7 years",
        available_income: "less than 20%",
        residence: "more than 7 years",
        assets: "real estate",
        age: 67,
        other_loans: "no additional loans",
        housing: "own",
        previous_loans: "2 or 3",
        job: "skilled",
        other_debtors: "none",
        people_liable: "0 to 2",
        telephone: "yes",
        NN_recommendation: "Approve",
        NN_confidence: 0.9382685422897339,
      },
    };
  },
  inject: ["attributeData", "apiUrl"],
  mounted() {
    this.sendExplanationRequest();
  },
  methods: {
    saveData(result) {
      for (let obj of result) {
        let childElement = {};
        childElement.name = this.attributeData.labels[obj.attribute];
        childElement.category = this.attributeData.categories[obj.attribute];
        childElement.value = Math.abs(obj.influence);
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
      const detailView = this.detailView;
      const w = 600;
      const h = 500;
      const hierarchy = d3
          .hierarchy(detailView ? this.detailExpData : this.simpleExpData)
          .sum((d) => d.value) //sums every child values
          .sort((a, b) => b.value - a.value), // and sort them in descending order
        treemap = d3.treemap().size([w, h]).padding(1),
        root = treemap(hierarchy);

      var colors = ["#008000", "#B22222"],
        colorScale = d3
          .scaleOrdinal() // the scale function
          .domain(["positive", "negative"]) // the data
          .range(colors); // the way the data should be shown

      const tooltip = d3.select("#tooltip").style("font-size", "16px");

      const svg = d3
        .select("#treemap") //make sure there's a svg element in your html file
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
              .attr("class", "tt-category");
          }

          tooltip
            .append("div")
            .text(d.data.name.charAt(0).toUpperCase() + d.data.name.slice(1))
            .attr("class", "tt-name")
            .style("font-weight", "600");

          tooltip
            .append("div")
            .text(Math.round(d.data.value * 10000) / 100 + "%")
            .style(
              "color",
              colorScale(
                detailView ? d.parent.parent.data.name : d.parent.data.name
              )
            )
            .attr("class", "tt-value");

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
        .attr("x", (d) => d.x0 + 5)
        .attr("y", (d) => d.y0 + 20)
        .text(function (d) {
          if (d.x1 - d.x0 >= 120 && d.y1 - d.y0 >= 50) {
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
        .attr("x", (d) => d.x0 + 5)
        .attr("y", (d) => d.y0 + 40)
        .text(function (d) {
          if (d.x1 - d.x0 >= 120 && d.y1 - d.y0 >= 40) {
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
